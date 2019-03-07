from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AssuranceInput:

	def __init__(self, driver, xpath):
		self.input_element = WebDriverWait(driver, 10).until(
				EC.element_to_be_clickable((By.XPATH, xpath)))
	
	def send_keys(self, keys_to_send):
		self.input_element.send_keys(keys_to_send)