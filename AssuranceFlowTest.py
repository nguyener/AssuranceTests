#! ~/.pyenv/shims/python
import pytest
from selenium import webdriver
from selenium.webdriver.support.select import Select

# test data is in the following order
# (zip, tobacco usage, birthdate, height, weight, sex, employment,
# number of kids, mortgage, income, quote amount, quote term, premium)

test_data = [
	("life", 34102, False, "04/04/1970", 68, 155, "male", True, 0, False, 155000, 350000, 10, 40),
	("life", 10001, False, "04/04/1970", 68, 155, "male", True, 0, False, 155000, 350000, 10, 40)
]
	

@pytest.fixture(scope="class")
def chrome_driver_init(request):
	u"""chrome driver initialization"""
    chrome_driver = webdriver.Chrome()
    request.cls.driver = chrome_driver
    yield
    chrome_driver.close()

@pytest.mark.usefixtures("chrome_driver_init")
class Test_Assurance_Flow:

	def _select_insurance_type(self, insurance_type):
		u"""Coverage selection page entry and click"""
		dropdown = Select(self.driver.find_element_by_class_name("select-loi"))
		dropdown.select_by_value(insurance_type)
		self.driver.find_element_by_link_text("Calculate your coverage").click()

#	@pytest.mark.parameterize("zip, tobacco, birthdate, height, weight, sex, employment, kids, mortgage, income, quote_amount, quote_term, premium", test_data)
	def test_base(self):
		u"""Parameterized test for the Assurance web flow"""
		self.driver.get("https://staging.assurance.com/")
		self._select_insurance_type("life")
		assert 2 == 2
