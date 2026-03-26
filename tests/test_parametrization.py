import pytest
from _pytest.fixtures import SubRequest

@pytest.mark.parametrize("number", [1, 2, 3, -1])
def test_numbers(number: int):
    assert number > 0

@pytest.mark.parametrize("os", ["macos", "windows", "linux", "debian"])
@pytest.mark.parametrize('browser', ['chromium', 'webkit', 'firefox'])
def test_multiplication_of_numbers(os: str, browser: str):
    assert len(os + browser) > 0

@pytest.fixture(params=['chromium', 'webkit', 'firefox'])
def browser(request: SubRequest):
    return request.param

def test_open_browser(browser: str):
    print(f'Running test on browser: {browser}')


@pytest.mark.parametrize('user', ['Alice', 'Zara'])
class TestOperations:

    def test_user_with_operations(self, user: str):
        print("")

    def test_user_without_operations(self, user: str):
         ...
        