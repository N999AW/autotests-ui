from xml.sax.xmlreader import Locator

from playwright.sync_api import Page

class BaseElement:
    def __init__(self, page: Page, locator: str, name: str):
        self.page = page
        self.name = name
        self.locator = locator

    def get_locator(self, **kwargs):
        locator = self.locator.format(**kwargs)
        return self.page.get_by_test_id(locator)
