import json
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def playwright_browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        # Load cookies into Playwright context
        try:
            with open("cookies.json", "r") as cookie_file:
                cookies = json.load(cookie_file)
                context.add_cookies(cookies)
        except FileNotFoundError:
            pytest.fail("Error: Cookies file not found. Run the Selenium login test (tests/test_login.py) first.")

        yield context
        browser.close()

def test_post_login_navigation(playwright_browser):
    page = playwright_browser.new_page()
    page.goto("https://jira-selenium-test.atlassian.net/jira/your-work")  # Example URL

    # Perform UI interactions with Playwright starting from the logged-in state
    assert page.title() == "Your work - Jira", "Failed to reach the Jira homepage!"

    # Example: Locate an element on the homepage
    home_page = WebDriverWait(driver, 15).until(EC.title_is("Your work - Jira"))
    assert home_page.is_visible(), "Expected element is not visible!"
