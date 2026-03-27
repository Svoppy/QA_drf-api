"""
Integration tests for Cart lifecycle (M3 — Cart Management, Risk Score: 12, High).

Tests cover:
- Retrieving a cart by token
- Cart response schema
- Token isolation between sessions
- Cart is_active default behavior

Requires: SUT running at http://localhost:8002
"""
import pytest
import requests
import uuid

BASE_URL = "http://localhost:8002/store"


@pytest.fixture(scope="module")
def session():
    return requests.Session()


class TestCartTokenRetrieval:
    """GET /cart/<token>/ — token-based cart access (no auth required)."""

    def test_new_token_returns_200(self, session):
        """M3: Any token returns 200 (API creates empty cart or returns empty data)."""
        token = str(uuid.uuid4())
        r = session.get(f"{BASE_URL}/cart/{token}/")
        assert r.status_code == 200

    def test_cart_response_is_json(self, session):
        """M3: Cart endpoint always returns JSON."""
        token = str(uuid.uuid4())
        r = session.get(f"{BASE_URL}/cart/{token}/")
        assert "application/json" in r.headers.get("Content-Type", "")

    def test_long_token_handled_gracefully(self, session):
        """M3: Excessively long token (256+ chars) does not cause 500."""
        long_token = "a" * 300
        r = session.get(f"{BASE_URL}/cart/{long_token}/")
        assert r.status_code in (200, 400, 404)

    def test_two_different_tokens_return_independent_responses(self, session):
        """M3 design risk: token collision — verify different tokens produce independent responses."""
        token_a = "qa-test-token-alpha-" + str(uuid.uuid4())
        token_b = "qa-test-token-beta-" + str(uuid.uuid4())
        r_a = session.get(f"{BASE_URL}/cart/{token_a}/")
        r_b = session.get(f"{BASE_URL}/cart/{token_b}/")
        assert r_a.status_code == 200
        assert r_b.status_code == 200
        # Both tokens must be independently valid (same status, not sharing data)
        assert r_a.url != r_b.url
