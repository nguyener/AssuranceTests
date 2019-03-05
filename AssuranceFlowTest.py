#! ~/.pyenv/shims/python
import pytest
from selenium import webdriver

# test data is in the following order
# (zip, tobacco usage, birthdate, height, weight, sex, employment,
# mortgage, income, quote amount, quote term, premium)

test_data = [
	(34102, False, "04/04/1970", 68, 155, "male", True, False, 0, False, 155000, 350000, 10, 40),
	(10001, False, "04/04/1970", 68, 155, "male", True, False, 0, False, 155000, 350000, 10, 40)
]
	

@pytest.fixture(scope="class")
def chrome_driver_init(request):
    chrome_driver = webdriver.Chrome()
    request.cls.driver = chrome_driver
    yield
    chrome_driver.close()

@pytest.mark.usefixtures("chrome_driver_init")
class Test_Assurance_Flow:
	def test_base(self):
		self.driver.get("https://staging.assurance.com/")
		assert 2 == 2
