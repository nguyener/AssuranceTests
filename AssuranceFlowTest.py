#! ~/.pyenv/shims/python
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from AssuranceButton import AssuranceButton
from AssuranceInput import AssuranceInput

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
		myself_button = AssuranceButton( self.driver, person )
		myself_button.click()
	
	def _select_tobacco_usage(self, tobacco):
		if(tobacco == True):
			yes_button = AssuranceButton( self.driver, "Yes" )
			yes_button.click()
		else:
			no_button = AssuranceButton( self.driver, "No" )
			no_button.click()
			
	def _enter_zip(self, zipcode):
		zip_input = AssuranceInput(self.driver, '//input')
		zip_input.send_keys(zipcode)
		element = WebDriverWait(self.driver, 10).until(
				EC.element_to_be_clickable((By.XPATH, "//input")))
		element.send_keys(zipcode)
		continue_button = AssuranceButton( self.driver, "Continue" )
		continue_button.click()
		
	def _enter_birth_date(self, month, day, year):
		# The custom drop down doesn't play nice with selenium. The sleeps help because I think
		# the animations are part of the hiccup.
		time.sleep(1)
		dropdown = WebDriverWait(self.driver, 10).until(
				EC.element_to_be_clickable((By.XPATH, '//div[@aria-haspopup="true"]')))
		dropdown.click()
		time.sleep(1)
		dropdown_item = WebDriverWait(self.driver, 10).until(
				EC.element_to_be_clickable((By.XPATH, '//li[@data-value="' + month + '"]')))
		dropdown_item.click()
		time.sleep(1)
		day_input = AssuranceInput(self.driver, '//div[@label="Day"]/input')
		day_input.send_keys(day)
		year_input = AssuranceInput(self.driver, '//div[@label="Year"]/input')
		year_input.send_keys(year)
		continue_button = AssuranceButton( self.driver, "Continue" )
		continue_button.click()
		
	def _enter_height(self, height):
		# The custom drop down doesn't play nice with selenium. The sleeps help because I think
		# the animations are part of the hiccup.
		time.sleep(1)
		dropdown = WebDriverWait(self.driver, 10).until(
				EC.element_to_be_clickable((By.XPATH, '//div[@aria-haspopup="true"]')))
		dropdown.click()
		time.sleep(1)
		dropdown_item = WebDriverWait(self.driver, 10).until(
				EC.element_to_be_clickable((By.XPATH, '//li[@data-value="' + height + '"]')))
		dropdown_item.click()
		time.sleep(1)
		continue_button = AssuranceButton( self.driver, "Continue" )
		continue_button.click()
		
	def _enter_weight(self, weight):
		weight_input = AssuranceInput(self.driver, '//input')
		weight_input.send_keys(weight)
		continue_button = AssuranceButton( self.driver, "Continue" )
		continue_button.click()
	
	def _select_marriage_status(self, married):
		if(married == True):
			yes_button = AssuranceButton( self.driver, "Yes" )
			yes_button.click()
		else:
			no_button = AssuranceButton( self.driver, "No" )
			no_button.click()
	
	def _select_child_count(self, married):
		if(married == True):
			yes_button = AssuranceButton( self.driver, "Yes" )
			yes_button.click()
		else:
			no_button = AssuranceButton( self.driver, "No" )
			no_button.click()

		
		

#	@pytest.mark.parameterize("zip, tobacco, birthdate, height, weight, sex, employment, kids, mortgage, income, quote_amount, quote_term, premium", test_data)
	def test_base(self):
		u"""Parameterized test for the Assurance web flow"""
		self.driver.get("https://staging.assurance.com/")
		self._select_insurance_type("life")
		self._select_person_to_be_covered("Myself")
		self._select_tobacco_usage(False)
		self._enter_zip("34102")
		self._enter_birth_date("4", "04", "1970")
		self._enter_height("68")
		self._enter_weight("155")
		#continue through the pre-existing conditions page
		continue_button = AssuranceButton( self.driver, "Continue" )
		continue_button.click()
		self._select_marriage_status(True)
		self._select_child_count(False)
		assert 2 == 2
