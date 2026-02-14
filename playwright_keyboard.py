from playwright.sync_api import sync_playwright


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/login")

    email_input = page.get_by_test_id('login-form-email-input').locator('input')
    email_input.focus()

    for char in "user@gmail.com":
        page.keyboard.type(char, delay=200)

    registration_button = page.get_by_test_id('login-page-registration-link')
    registration_button.hover()

    page.wait_for_timeout(5000)