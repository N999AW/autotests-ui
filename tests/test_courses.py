from playwright.sync_api import sync_playwright, expect, Page
import pytest

@pytest.mark.courses
@pytest.mark.regression
def test_empty_courses_list(chromium_page_with_state):
        page = chromium_page_with_state
        page.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/courses")
        H6 = page.get_by_test_id("courses-list-toolbar-title-text")
        expect(H6).to_have_text("Courses")
        H62 = page.get_by_test_id("courses-list-empty-view-title-text")
        expect(H62).to_have_text("There is no results")
        Icon = page.get_by_test_id("courses-list-empty-view-icon")
        expect(Icon).to_be_attached()
        lower_text = page.get_by_test_id("courses-list-empty-view-description-text")
        expect(lower_text).to_have_text("Results from the load test pipeline will be displayed here")
        page.wait_for_timeout(5000)