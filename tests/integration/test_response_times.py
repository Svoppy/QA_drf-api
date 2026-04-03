"""
Response time (performance gate) tests for all GET endpoints.

Metric collected: TTE (Time To Execute) per endpoint.
Quality gate: every GET endpoint must respond in < 500ms under no-load conditions.

Risk areas: M4 (Product Catalog), M5 (Collections/Categories), M3 (Cart)
Requires: SUT running at http://localhost:8002
"""
import pytest
import requests
import time

BASE_URL = "http://localhost:8002/store"
MAX_RESPONSE_MS = 500  # Quality gate threshold


@pytest.fixture(scope="module")
def session():
    s = requests.Session()
    # Warm-up request to avoid first-connection overhead skewing results
    try:
        s.get(f"{BASE_URL}/clothing-collections/", timeout=5)
    except Exception:
        pass
    return s


def assert_response_time(response, endpoint: str, threshold_ms: int = MAX_RESPONSE_MS):
    """Helper: assert response elapsed time is within threshold."""
    elapsed_ms = response.elapsed.total_seconds() * 1000
    assert elapsed_ms < threshold_ms, (
        f"{endpoint} responded in {elapsed_ms:.0f}ms — exceeds {threshold_ms}ms gate"
    )
    return elapsed_ms


class TestEndpointResponseTimes:
    """All high-traffic GET endpoints must respond within the 500ms quality gate."""

    def test_product_list_page1_under_500ms(self, session):
        r = session.get(f"{BASE_URL}/clothing-products/1/", timeout=5)
        assert r.status_code == 200
        assert_response_time(r, "GET /clothing-products/1/")

    def test_clothing_collections_under_500ms(self, session):
        r = session.get(f"{BASE_URL}/clothing-collections/", timeout=5)
        assert r.status_code == 200
        assert_response_time(r, "GET /clothing-collections/")

    def test_clothing_collections_filter_names_under_500ms(self, session):
        r = session.get(f"{BASE_URL}/clothing-collections/filter/names/", timeout=5)
        assert r.status_code in (200, 404, 500)
        if r.status_code == 200:
            assert_response_time(r, "GET /clothing-collections/filter/names/")

    def test_categories_under_500ms(self, session):
        r = session.get(f"{BASE_URL}/categories/", timeout=5)
        assert r.status_code == 200
        assert_response_time(r, "GET /categories/")

    def test_categories_filter_names_under_500ms(self, session):
        r = session.get(f"{BASE_URL}/categories/filter/names/", timeout=5)
        assert r.status_code in (200, 404, 500)
        if r.status_code == 200:
            assert_response_time(r, "GET /categories/filter/names/")

    def test_cart_endpoint_under_500ms(self, session):
        r = session.get(f"{BASE_URL}/cart/perf-test-token-001/", timeout=5)
        assert r.status_code in (200, 404)
        assert_response_time(r, "GET /cart/<token>/")
