"""
Unit tests for ClothingProduct, Cart, and ProductVariation models.

Risk areas:
  M3 — Cart Management (total_amount property)
  M4 — Product Catalog (model-level field constraints)
  M6 — Data Validation (field and validator correctness)
"""
import pytest
from decimal import Decimal

from store_app.models import (
    GlobalModel,
    CustomColor,
    ClothingProduct,
    Cart,
    ProductVariation,
)


@pytest.mark.django_db
class TestCartTotalAmountWithItems:
    """M3: Cart.total_amount must sum quantity * base_pricing for all variations."""

    def test_cart_total_with_single_variation(self):
        product = ClothingProduct.objects.create(
            name="Cargo Pants", code="CP001", base_pricing=Decimal("25.00")
        )
        color = CustomColor.objects.create(nickname="Navy", code="#001F5B")
        cart = Cart.objects.create(ip_address="10.0.0.1")
        ProductVariation.objects.create(product=product, principal_color=color, quantity=3, cart=cart)
        assert cart.total_amount == Decimal("75.00")

    def test_cart_total_with_multiple_variations(self):
        product_a = ClothingProduct.objects.create(
            name="Linen Shirt", code="LS001", base_pricing=Decimal("40.00")
        )
        product_b = ClothingProduct.objects.create(
            name="Linen Shorts", code="LSH001", base_pricing=Decimal("30.00")
        )
        color = CustomColor.objects.create(nickname="Beige", code="#F5F5DC")
        cart = Cart.objects.create(ip_address="10.0.0.2")
        ProductVariation.objects.create(product=product_a, principal_color=color, quantity=2, cart=cart)
        ProductVariation.objects.create(product=product_b, principal_color=color, quantity=1, cart=cart)
        # 2*40 + 1*30 = 110
        assert cart.total_amount == Decimal("110.00")

    def test_empty_cart_total_is_zero(self):
        cart = Cart.objects.create(ip_address="10.0.0.3")
        assert cart.total_amount == 0


@pytest.mark.django_db
class TestClothingProductFields:
    """M6: ClothingProduct model field defaults and constraints."""

    def test_product_default_tag_is_shirt(self):
        product = ClothingProduct.objects.create(
            name="Default Tag Shirt", code="DT001", base_pricing=Decimal("20.00")
        )
        assert product.tag == "SHIRT"

    def test_product_amount_sold_defaults_to_zero(self):
        product = ClothingProduct.objects.create(
            name="New Arrival", code="NA001", base_pricing=Decimal("35.00")
        )
        assert product.amount_sold == 0

    def test_product_str_contains_name_and_code(self):
        product = ClothingProduct.objects.create(
            name="Classic Blouse", code="CB001", base_pricing=Decimal("55.00")
        )
        s = str(product)
        assert "Classic Blouse" in s
        assert "CB001" in s
