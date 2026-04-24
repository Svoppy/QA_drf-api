"""
Midterm E2E tests for restricted dashboard access.

Targets:
  - M8: Global configuration dashboard access
  - M1: Order dashboard access
"""
# SEARCH TAGS:
# MIDTERM TEST
# E2E TEST
# PLAYWRIGHT TEST
# ACCESS CONTROL TEST
# SECURITY BEHAVIOR TEST
# INVALID USER BEHAVIOR TEST
import pytest
from playwright.sync_api import Page


BASE_URL = "http://localhost:8002"
DASHBOARD_LOGIN_URL = f"{BASE_URL}/dashboard/accounts/login/"


class TestMidtermDashboardAccess:
    # SEARCH TAG: MIDTERM TEST / E2E TEST / ACCESS CONTROL TEST

    def test_tc_mt_e2e_m8_01_anonymous_user_is_redirected_from_global_configs(self, page: Page):
        # SEARCH TAG: MIDTERM TEST / ACCESS CONTROL TEST / ANONYMOUS REDIRECT
        page.goto(f"{BASE_URL}/dashboard/global-configs/")
        page.wait_for_load_state("networkidle")

        assert page.url.startswith(DASHBOARD_LOGIN_URL)
        assert "login" in page.url.lower()

    def test_tc_mt_e2e_m1_01_anonymous_user_is_redirected_from_orders(self, page: Page):
        # SEARCH TAG: MIDTERM TEST / ACCESS CONTROL TEST / ANONYMOUS REDIRECT
        page.goto(f"{BASE_URL}/dashboard/orders/")
        page.wait_for_load_state("networkidle")

        assert page.url.startswith(DASHBOARD_LOGIN_URL)
        assert "login" in page.url.lower()
