"""
Integration tests for store_app REST API endpoints.
Requires the app to be running at BASE_URL (docker compose up).
"""
import pytest
import requests

BASE_URL = "http://localhost:8002/store"


@pytest.fixture(scope="module")
def session():
    s = requests.Session()
    return s


class TestProductListAPI:
    """GET /clothing-products/<page>/"""

    def test_returns_200(self, session):
        r = session.get(f"{BASE_URL}/clothing-products/1/")
        assert r.status_code == 200

    def test_response_is_json(self, session):
        r = session.get(f"{BASE_URL}/clothing-products/1/")
        assert r.headers["Content-Type"].startswith("application/json")

    def test_pagination_fields_present(self, session):
        r = session.get(f"{BASE_URL}/clothing-products/1/")
        data = r.json()
        assert "results" in data or isinstance(data, list)

    def test_invalid_page_returns_404_or_empty(self, session):
        r = session.get(f"{BASE_URL}/clothing-products/99999/")
        assert r.status_code in (200, 404)


class TestProductDetailAPI:
    """GET /clothing-products/items/<id>/"""

    def test_nonexistent_product_returns_404(self, session):
        r = session.get(f"{BASE_URL}/clothing-products/items/999999/")
        assert r.status_code == 404


class TestCollectionsAPI:
    """GET /clothing-collections/"""

    def test_returns_200(self, session):
        r = session.get(f"{BASE_URL}/clothing-collections/")
        assert r.status_code == 200

    def test_returns_list(self, session):
        r = session.get(f"{BASE_URL}/clothing-collections/")
        data = r.json()
        assert isinstance(data, list)


class TestCategoriesAPI:
    """GET /categories/"""

    def test_returns_200(self, session):
        r = session.get(f"{BASE_URL}/categories/")
        assert r.status_code == 200

    def test_each_category_has_title(self, session):
        r = session.get(f"{BASE_URL}/categories/")
        for cat in r.json():
            assert "title" in cat


class TestCartAPI:
    """GET /cart/<token>/"""

    def test_unknown_token_returns_200_or_404(self, session):
        # RISK NOTE: API returns 200 for unknown tokens (creates empty cart or returns empty data).
        # This is a known design concern — no 404 on missing cart token.
        r = session.get(f"{BASE_URL}/cart/invalidtoken123/")
        assert r.status_code in (200, 404)

    def test_cart_response_is_json(self, session):
        r = session.get(f"{BASE_URL}/cart/invalidtoken123/")
        assert "application/json" in r.headers.get("Content-Type", "")


class TestOrderCreateAPI:
    """POST /orders/"""

    def test_empty_payload_returns_400(self, session):
        r = session.post(f"{BASE_URL}/orders/", json={})
        assert r.status_code in (400, 422)

    def test_missing_email_returns_400(self, session):
        r = session.post(f"{BASE_URL}/orders/", json={
            "first_name": "John",
            "last_name": "Doe",
        })
        assert r.status_code in (400, 422)
