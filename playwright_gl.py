from playwright.sync_api import sync_playwright, expect

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://re-store.ru/")
    page.get_by_text("New")

    page.wait_for_timeout(50000)