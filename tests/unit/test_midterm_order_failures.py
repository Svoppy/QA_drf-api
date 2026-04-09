"""
Midterm unit tests for high-risk order and payment failure paths.

Targets:
  - M1: Order and Checkout
  - M2: Stripe Payment Integration
"""
from unittest.mock import patch

import pytest
import stripe
from rest_framework.test import APIRequestFactory

from store_app.models import Cart, Order, Payment
from store_app.views import OrderCreateAPIView


def build_order_payload(cart_id):
    return {
        "cart": cart_id,
        "email": "qa-midterm@example.com",
        "phone": "5551234567",
        "first_name": "QA",
        "last_name": "Midterm",
        "shipping_address": {
            "street": "123 Midterm Ave",
            "city": "Miami",
            "usa_state": "Florida",
            "zip_code": "33101",
        },
        "card_num": "4242424242424242",
        "exp_month": "12",
        "exp_year": "2030",
        "cvc": "123",
    }


@pytest.mark.django_db
class TestMidtermOrderPaymentFailures:
    def setup_method(self):
        self.factory = APIRequestFactory()

    def test_tc_mt_ut_m2_01_token_failure_returns_400_and_rolls_back_order(self):
        cart = Cart.objects.create(ip_address="127.0.0.1", token="midterm-token-1")
        payload = build_order_payload(cart.id)
        request = self.factory.post("/store/orders/", payload, format="json")

        with patch(
            "store_app.views.stripe.Token.create",
            side_effect=stripe.error.AuthenticationError("bad stripe auth"),
        ):
            response = OrderCreateAPIView.as_view()(request)

        assert response.status_code == 400
        assert response.data["Result"] == "Authentication error during payment"
        assert Order.objects.count() == 0
        assert Payment.objects.count() == 0

    def test_tc_mt_ut_m2_02_charge_failure_returns_400_and_rolls_back_order(self):
        cart = Cart.objects.create(ip_address="127.0.0.1", token="midterm-token-2")
        payload = build_order_payload(cart.id)
        request = self.factory.post("/store/orders/", payload, format="json")

        with patch("store_app.views.stripe.Token.create", return_value="tok_test_midterm"), patch(
            "store_app.views.stripe.Charge.create",
            side_effect=stripe.error.APIConnectionError("network issue"),
        ):
            response = OrderCreateAPIView.as_view()(request)

        assert response.status_code == 400
        assert response.data["Result"] == "API connection error during payment"
        assert Order.objects.count() == 0
        assert Payment.objects.count() == 0
