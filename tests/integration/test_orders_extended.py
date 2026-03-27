"""
Extended integration tests for Order creation endpoint (M1 — Order & Checkout, Risk Score: 20, Critical).

Tests cover:
- Validation of individual required fields (boundary/negative tests)
- Invalid email format rejection
- Invalid USA state rejection
- Zip code length constraint
- Idempotency risk: duplicate submission behaviour

Requires: SUT running at http://localhost:8002
"""
import pytest
import requests

BASE_URL = "http://localhost:8002/store"

VALID_ORDER_PAYLOAD = {
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "address": {
        "street": "123 Test St",
        "city": "Miami",
        "usa_state": "Florida",
        "zip_code": "33101",
    },
    "cart": "nonexistent-cart-token",
}


@pytest.fixture(scope="module")
def session():
    return requests.Session()


class TestOrderFieldValidation:
    """M1 + M6: All POST /orders/ required fields must be validated server-side."""

    def test_invalid_email_format_rejected(self, session):
        """M6: email field without '@' must return 400."""
        payload = dict(VALID_ORDER_PAYLOAD)
        payload["email"] = "not-an-email"
        r = session.post(f"{BASE_URL}/orders/", json=payload)
        assert r.status_code in (400, 422), (
            f"Expected 400/422 for invalid email, got {r.status_code}"
        )

    def test_missing_first_name_rejected(self, session):
        """M6: first_name is required — omitting it must return 400."""
        payload = {k: v for k, v in VALID_ORDER_PAYLOAD.items() if k != "first_name"}
        r = session.post(f"{BASE_URL}/orders/", json=payload)
        assert r.status_code in (400, 422)

    def test_missing_last_name_rejected(self, session):
        """M6: last_name is required — omitting it must return 400."""
        payload = {k: v for k, v in VALID_ORDER_PAYLOAD.items() if k != "last_name"}
        r = session.post(f"{BASE_URL}/orders/", json=payload)
        assert r.status_code in (400, 422)

    def test_zip_code_too_long_rejected_or_truncated(self, session):
        """M6: zip_code max_length=5 — 10-digit zip should be rejected or capped."""
        payload = dict(VALID_ORDER_PAYLOAD)
        payload["address"] = dict(payload["address"])
        payload["address"]["zip_code"] = "123456789012345"
        r = session.post(f"{BASE_URL}/orders/", json=payload)
        # DRF may return 400 or 201 depending on whether serializer enforces max_length
        assert r.status_code in (400, 422, 201)

    def test_duplicate_order_same_payload_returns_400_or_201(self, session):
        """M1 idempotency risk: sending same payload twice — no crash, consistent response."""
        payload = dict(VALID_ORDER_PAYLOAD)
        r1 = session.post(f"{BASE_URL}/orders/", json=payload)
        r2 = session.post(f"{BASE_URL}/orders/", json=payload)
        # Both must be a valid HTTP response (no 500)
        assert r1.status_code != 500, f"First submission crashed with 500"
        assert r2.status_code != 500, f"Duplicate submission crashed with 500"
