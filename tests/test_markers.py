import pytest

@pytest.mark.smoke
def test_smoke_case():
    ...


@pytest.mark.regression
def test_regression_case():
    ...
@pytest.mark.smoke
class TestSuite:
    def test_case1(self):
        print("линарчик")


    def test_case2(self):
        ...
