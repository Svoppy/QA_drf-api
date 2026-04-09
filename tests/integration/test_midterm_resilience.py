"""
Midterm integration tests for resilience and invalid behavior on high-risk modules.

Targets:
  - M1: Order and Checkout
  - M3: Cart Management
"""
from concurrent.futures import ThreadPoolExecutor
import uuid

import pytest
import requests

BASE_URL = "http://localhost:8002/store"


@pytest.fixture(scope="module")
def session():
    return requests.Session()


class TestMidtermResilience:
    def test_tc_mt_it_m1_01_orders_endpoint_rejects_malformed_json_without_500(self, session):
        response = session.post(
            f"{BASE_URL}/orders/",
            data='{"broken_json": ',
            headers={"Content-Type": "application/json"},
            timeout=5,
        )

        assert response.status_code in (400, 415), (
            f"Expected controlled client error for malformed JSON, got {response.status_code}"
        )

    def test_tc_mt_it_m3_01_parallel_cart_requests_same_token_do_not_crash(self, session):
        token = "midterm-parallel-" + str(uuid.uuid4())

        def fetch_cart():
            return session.get(f"{BASE_URL}/cart/{token}/", timeout=5)

        with ThreadPoolExecutor(max_workers=5) as executor:
            responses = list(executor.map(lambda _: fetch_cart(), range(5)))

        status_codes = [response.status_code for response in responses]
        assert all(code in (200, 404) for code in status_codes), status_codes
        assert 500 not in status_codes
