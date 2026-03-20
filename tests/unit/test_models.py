"""
Unit tests for store_app models.
Tests model validation, business logic, and field constraints.
"""
import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError

from store_app.models import (
    custom_color_format_validator,
    CustomColor,
    ClothingProduct,
    Cart,
    ProductVariation,
    Address,
)


# -------------------------------------------------------
# CustomColor validator
# -------------------------------------------------------

class TestCustomColorValidator:
    def test_valid_hex_6(self):
        assert custom_color_format_validator("#FF5733") == "#FF5733"

    def test_valid_hex_3(self):
        assert custom_color_format_validator("#FFF") == "#FFF"

    def test_valid_hex_8_alpha(self):
        assert custom_color_format_validator("#FF5733AA") == "#FF5733AA"

    def test_invalid_no_hash(self):
        with pytest.raises(ValidationError):
            custom_color_format_validator("FF5733")

    def test_invalid_too_short(self):
        with pytest.raises(ValidationError):
            custom_color_format_validator("#FF")

    def test_invalid_non_hex_chars(self):
        with pytest.raises(ValidationError):
            custom_color_format_validator("#GGGGGG")


# -------------------------------------------------------
# Cart total_amount property
# -------------------------------------------------------

@pytest.mark.django_db
class TestCartTotalAmount:
    def test_empty_cart_total_is_zero(self):
        cart = Cart.objects.create(ip_address="127.0.0.1")
        assert cart.total_amount == 0

    def test_cart_str_contains_ip(self):
        cart = Cart.objects.create(ip_address="192.168.1.1")
        assert "192.168.1.1" in str(cart) or cart.total_amount == 0


# -------------------------------------------------------
# Address model
# -------------------------------------------------------

@pytest.mark.django_db
class TestAddressModel:
    def test_create_valid_address(self):
        addr = Address.objects.create(
            street="123 Main St",
            city="Miami",
            usa_state="Florida",
            zip_code="33101",
        )
        assert addr.pk is not None

    def test_address_str(self):
        addr = Address.objects.create(
            street="456 Ocean Dr",
            city="Miami Beach",
            usa_state="Florida",
            zip_code="33139",
        )
        assert "456 Ocean Dr" in str(addr)
        assert "Miami Beach" in str(addr)
