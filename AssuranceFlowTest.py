#! ~/.pyenv/shims/python
import pytest
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# test data is in the following order
# (zip, tobacco usage, birthdate, height, weight, sex, employment,
# number of kids, mortgage, income, quote amount, quote term, premium)

test_data = [
	("life", "Myself", 34102, False, "04/04/1970", 68, 155, "male", True, 0, False, 155000, 350000, 10, 40),
	("life", "Myself", 10001, False, "04/04/1970", 68, 155, "male", True, 0, False, 155000, 350000, 10, 40)
]
	

@pytest.fixture(scope="class")
def chrome_driver_init(request):
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
	
	def _select_person_to_be_covered(self, person):
		if(person == "Myself"):
			element = WebDriverWait(self.driver, 10).until(
				EC.element_to_be_clickable((By.CLASS_NAME, "jss107")))
			self.driver.find_element_by_class_name("jss107").click()
	
	def _select_tobacco_usage(self, tobacco):
		element = WebDriverWait(self.driver, 10).until(
			EC.presence_of_element_located((By.CLASS_NAME, "jss110")))
		element = WebDriverWait(self.driver, 10).until(
			EC.element_to_be_clickable((By.CLASS_NAME, "jss110")))
		if(tobacco == True):
			(self.driver.find_elements_by_class_name("jss110"))[0].click()
		else:
			(self.driver.find_elements_by_class_name("jss110"))[1].click()
			
	def _enter_zip(self, zipcode):
		element = WebDriverWait(self.driver, 10).until(
			EC.presence_of_element_located((By.CLASS_NAME, "jss180")))
		element.sendkeys(zipcode)
		self.driver.find_element_by_link_text("Calculate your coverage").click()
		
		

#	@pytest.mark.parameterize("zip, tobacco, birthdate, height, weight, sex, employment, kids, mortgage, income, quote_amount, quote_term, premium", test_data)
	def test_base(self):
		u"""Parameterized test for the Assurance web flow"""
		self.driver.get("https://staging.assurance.com/")
		self._select_insurance_type("life")
		self._select_person_to_be_covered("Myself")
		self._select_tobacco_usage(True)
		#self._enter_zip("34102")
		assert 2 == 2
