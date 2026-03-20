"""
E2E tests for admin panel using Playwright.
Requires the app running at BASE_URL and playwright browsers installed:
    playwright install chromium
"""
import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:8001"
ADMIN_URL = f"{BASE_URL}/admin"


@pytest.fixture(scope="function")
def logged_in_admin(page: Page):
    page.goto(f"{ADMIN_URL}/login/")
    page.fill("input[name='username']", "admin")
    page.fill("input[name='password']", "admin1234")
    page.click("input[type='submit']")
    page.wait_for_url(f"{ADMIN_URL}/")
    return page


class TestAdminLogin:
    def test_login_page_loads(self, page: Page):
        page.goto(f"{ADMIN_URL}/login/")
        expect(page).to_have_title("Log in | Django site admin")

    def test_invalid_credentials_shows_error(self, page: Page):
        page.goto(f"{ADMIN_URL}/login/")
        page.fill("input[name='username']", "wronguser")
        page.fill("input[name='password']", "wrongpass")
        page.click("input[type='submit']")
        expect(page.locator(".errornote")).to_be_visible()

    def test_valid_login_redirects_to_dashboard(self, logged_in_admin: Page):
        expect(logged_in_admin).to_have_url(f"{ADMIN_URL}/")


class TestAdminDashboard:
    def test_dashboard_shows_store_app_models(self, logged_in_admin: Page):
        content = logged_in_admin.content()
        assert "Store_App" in content or "store_app" in content or "Clothing" in content

    def test_logout_works(self, logged_in_admin: Page):
        logged_in_admin.goto(f"{ADMIN_URL}/logout/")
        expect(logged_in_admin).to_have_url(f"{ADMIN_URL}/login/")
