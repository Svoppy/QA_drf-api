"""
Unit tests for GlobalModel tax and currency calculation logic.

Risk area: M8 — Tax & Currency Calculation (Risk Score: 12, High)
Design risk: GlobalModel.objects.get(active=True) crashes on 0 or 2+ active records.
"""
import pytest
from decimal import Decimal
from django.core.exceptions import MultipleObjectsReturned

from store_app.models import GlobalModel, ClothingProduct, CustomColor, Cart, ProductVariation


@pytest.mark.django_db
class TestGlobalModelPricingWithTax:
    """Tests for ClothingProduct.pricing_with_tax() — depends on single active GlobalModel."""

    def test_no_active_model_raises_does_not_exist(self):
        """M8 critical: zero active GlobalModel records → DoesNotExist crash on any pricing call."""
        product = ClothingProduct.objects.create(
            name="Shirt NX1", code="NX001", base_pricing=Decimal("100.00")
        )
        with pytest.raises(GlobalModel.DoesNotExist):
            product.pricing_with_tax()

    def test_single_active_model_calculates_correctly(self):
        """M8: base_pricing * (1 + us_sales_taxes) with 10% tax."""
        GlobalModel.objects.create(
            active=True, mx_value=Decimal("18.0000"), us_sales_taxes=Decimal("0.1000")
        )
        product = ClothingProduct.objects.create(
            name="Shirt TX1", code="TX001", base_pricing=Decimal("100.00")
        )
        assert product.pricing_with_tax() == Decimal("110.0000")

    def test_zero_tax_rate_returns_base_price(self):
        """M8 boundary: us_sales_taxes=0 → pricing equals base_pricing."""
        GlobalModel.objects.create(
            active=True, mx_value=Decimal("18.0000"), us_sales_taxes=Decimal("0.0000")
        )
        product = ClothingProduct.objects.create(
            name="Shirt TX2", code="TX002", base_pricing=Decimal("50.00")
        )
        assert product.pricing_with_tax() == Decimal("50.0000")

    def test_pricing_mx_multiplies_by_mx_value(self):
        """M8: MX pricing = base_pricing * mx_value (no tax)."""
        GlobalModel.objects.create(
            active=True, mx_value=Decimal("18.0000"), us_sales_taxes=Decimal("0.1000")
        )
        product = ClothingProduct.objects.create(
            name="Shirt MX1", code="MX001", base_pricing=Decimal("10.00")
        )
        assert product.pricing_mx() == Decimal("180.0000")

    def test_pricing_with_tax_mx_combines_tax_and_conversion(self):
        """M8: MX price with tax = base * (1 + tax) * mx_value → 10 * 1.10 * 18 = 198."""
        GlobalModel.objects.create(
            active=True, mx_value=Decimal("18.0000"), us_sales_taxes=Decimal("0.1000")
        )
        product = ClothingProduct.objects.create(
            name="Shirt MX2", code="MX002", base_pricing=Decimal("10.00")
        )
        assert product.pricing_with_tax_mx() == Decimal("198.0000")

    def test_multiple_active_models_raises_multiple_objects_returned(self):
        """M8 design risk: two active GlobalModel rows → get() raises MultipleObjectsReturned."""
        GlobalModel.objects.create(
            active=True, mx_value=Decimal("18.0000"), us_sales_taxes=Decimal("0.1000")
        )
        GlobalModel.objects.create(
            active=True, mx_value=Decimal("19.0000"), us_sales_taxes=Decimal("0.1200")
        )
        product = ClothingProduct.objects.create(
            name="Shirt MX3", code="MX003", base_pricing=Decimal("100.00")
        )
        with pytest.raises(MultipleObjectsReturned):
            product.pricing_with_tax()
