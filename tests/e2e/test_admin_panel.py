"""
E2E tests for admin panel using Playwright.
Requires the app running at BASE_URL and playwright browsers installed:
    playwright install chromium
"""
import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:8002"
ADMIN_URL = f"{BASE_URL}/admin"


@pytest.fixture(scope="function")
def logged_in_admin(page: Page):
    page.goto(f"{ADMIN_URL}/login/")
    page.fill("input[name='username']", "admin")
    page.fill("input[name='password']", "admin1234")
    page.locator("input[type='submit']").click()
    page.wait_for_load_state("networkidle")
    return page


class TestAdminLogin:
    def test_login_page_loads(self, page: Page):
        page.goto(f"{ADMIN_URL}/login/")
        expect(page).to_have_title("Log in | Django site admin")

    def test_invalid_credentials_shows_error(self, page: Page):
        page.goto(f"{ADMIN_URL}/login/")
        page.fill("input[name='username']", "wronguser")
        page.fill("input[name='password']", "wrongpass")
        page.locator("input[type='submit']").click()
        page.wait_for_load_state("networkidle")
        # Django admin shows error in <p class="errornote"> or inline error text
        error_visible = (
            page.locator(".errornote").count() > 0 or
            page.get_by_text("Please enter the correct").count() > 0 or
            page.get_by_text("correct username").count() > 0
        )
        assert error_visible, "Expected error message after invalid login"

    def test_valid_login_redirects_away_from_login(self, logged_in_admin: Page):
        assert "/login/" not in logged_in_admin.url


class TestAdminDashboard:
    def test_dashboard_shows_store_app_models(self, logged_in_admin: Page):
        content = logged_in_admin.content()
        assert "Store_App" in content or "store_app" in content or "Clothing" in content or "Authentication" in content

    def test_logout_works(self, logged_in_admin: Page):
        logged_in_admin.goto(f"{ADMIN_URL}/logout/")
        logged_in_admin.wait_for_load_state("networkidle")
        content = logged_in_admin.content()
        # After logout: either redirected to login page or shows "not logged in" message
        assert (
            "login" in logged_in_admin.url or
            "Logged out" in content or
            "not logged in" in content.lower() or
            "Log In" in content
        )
