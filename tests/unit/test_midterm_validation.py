"""
Midterm unit tests for validation and detectability gaps.

Targets:
  - M6: Data Validation
"""
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from store_app.models import GlobalModel
from store_app.serializers import AddressSerializer


@pytest.mark.django_db
class TestMidtermValidation:
    def test_tc_mt_ut_m6_01_address_serializer_rejects_zip_code_longer_than_five(self):
        serializer = AddressSerializer(
            data={
                "street": "123 Validation St",
                "city": "Miami",
                "usa_state": "Florida",
                "zip_code": "123456",
            }
        )

        assert serializer.is_valid() is False
        assert "zip_code" in serializer.errors

    def test_tc_mt_ut_m6_02_negative_currency_values_fail_model_validation(self):
        global_config = GlobalModel(
            active=True,
            mx_value=Decimal("-1.0000"),
            us_sales_taxes=Decimal("0.0700"),
        )

        with pytest.raises(ValidationError) as exc:
            global_config.full_clean()

        assert "mx_value" in exc.value.message_dict
