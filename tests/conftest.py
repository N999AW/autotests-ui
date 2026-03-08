import pytest
from playwright.sync_api import sync_playwright, Page, Playwright


@pytest.fixture
def chromium_page(playwright: Playwright) -> Page:
        browser = playwright.chromium.launch(headless=False)
        yield browser.new_page()
        browser.close()

@pytest.fixture
def initialize_browser_state(playwright: Playwright):
    chromium_page.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/registration")

    email_input = chromium_page.get_by_test_id('registration-form-email-input').locator('input')
    email_input.fill("usertest.name@gmail.com")

    username_input = chromium_page.get_by_test_id('registration-form-username-input').locator('input')
    username_input.fill("usernametest")

    password_input = chromium_page.get_by_test_id("registration-form-password-input").locator('input')
    password_input.fill("password")

    registration_button = chromium_page.get_by_test_id("registration-page-registration-button")
    registration_button.click()

    context.storage_state(path='browser_state.json')

@pytest.fixture
def chromium_page_with_state():
    context = browser.new_context(storage_state='browser_state.json')