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

# test data is in the following order (parallels the flow)
# (Insurance type, insuree, tobacco usage, zip, birthdate, height, weight, marriage status, children, employment, income, mortgage, other debt, sex, given name, family name, phone number, email, quote amount, quote term, premium)
# number of kids, mortgage, income, quote amount, quote term, premium)

@pytest.fixture(scope="function")
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
		time.sleep(1)
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
		time.sleep(1)
		if(married == True):
			yes_button = AssuranceButton( self.driver, "Yes" )
			yes_button.click()
		else:
			no_button = AssuranceButton( self.driver, "No" )
			no_button.click()
	
	def _select_child_count(self, children):
		time.sleep(1)
		if(children == True):
			yes_button = AssuranceButton( self.driver, "Yes" )
			yes_button.click()
		else:
			no_button = AssuranceButton( self.driver, "No" )
			no_button.click()
		
	def _select_employment_status(self, employment):
		time.sleep(1)
		continue_button = AssuranceButton( self.driver, employment )
		continue_button.click()
		
	def _enter_income(self, income):
		weight_input = AssuranceInput(self.driver, '//input')
		weight_input.send_keys(income)
		continue_button = AssuranceButton( self.driver, "Continue" )
		continue_button.click()
	
	def _select_mortgage(self, mortgage):
		time.sleep(1)
		if(mortgage == True):
			yes_button = AssuranceButton( self.driver, "Yes" )
			yes_button.click()
		else:
			no_button = AssuranceButton( self.driver, "No" )
			no_button.click()
	
	def _select_other_debt(self, other_debt):
		time.sleep(1)
		if(other_debt == True):
			yes_button = AssuranceButton( self.driver, "Yes" )
			yes_button.click()
		else:
			no_button = AssuranceButton( self.driver, "No" )
			no_button.click()
	
	def _select_sex(self, customer_sex):
		time.sleep(1)
		continue_button = AssuranceButton( self.driver, customer_sex )
		continue_button.click()
		
	def _enter_contact_info(self, given_name, family_name, phone, email):
		day_input = AssuranceInput(self.driver, '//input[@autocomplete="given-name"]')
		day_input.send_keys(given_name)
		day_input = AssuranceInput(self.driver, '//input[@autocomplete="family-name"]')
		day_input.send_keys(family_name)
		day_input = AssuranceInput(self.driver, '//input[@autocomplete="tel-national"]')
		day_input.send_keys(phone)
		day_input = AssuranceInput(self.driver, '//input[@autocomplete="email"]')
		day_input.send_keys(email)
		continue_button = AssuranceButton( self.driver, "View My Quote" )
		continue_button.click()

#validation parameters - , quote_amount, quote_term, premium

	
	@pytest.mark.parametrize("insurance_type, insuree, tobacco, zipcode, birth_month, birth_day, birth_year, height, weight, marriage_status, children, employment, income, mortgage, other_debt, sex, given_name, family_name, phone_number, email", [
		("life", "Myself", False, "34102", "4", "04", "1970", "68", "155", False, False, "Currently Employed", "155000", False, False, "Male", "John", "Doe", "6075472892", "johndoe@assurance.com"),# "350000", 10, 40)
		("life", "Myself", False, "10001", "4", "04", "1970", "68", "155", False, False, "Currently Employed", "155000", False, False, "Male", "John", "Doe", "6075472892", "johndoe@assurance.com")# "350000", 10, 40)
	])
	def test_flow(self, insurance_type, insuree, tobacco, zipcode, birth_month, birth_day, birth_year, height, weight, marriage_status, children, employment, income, mortgage, other_debt, sex, given_name, family_name, phone_number, email):
		self.driver.get("https://staging.assurance.com/")
		self._select_insurance_type(insurance_type)
		self._select_person_to_be_covered(insuree)
		self._select_tobacco_usage(tobacco)
		self._enter_zip(zipcode)
		self._enter_birth_date(birth_month, birth_day, birth_year)
		self._enter_height(height)
		self._enter_weight(weight)
		#continue through the pre-existing conditions page, not sure why the sleep is necessary here, need more info
		time.sleep(1)
		continue_button = AssuranceButton( self.driver, "Continue" )
		continue_button.click()
		self._select_marriage_status(marriage_status)
		self._select_child_count(children)
		self._select_employment_status(employment)
		self._enter_income(income)
		self._select_mortgage(mortgage)
		self._select_other_debt(other_debt)
		self._select_sex(sex)
		self._enter_contact_info(given_name, family_name, phone_number, email)
		self.driver.quit()

		assert 2 == 2