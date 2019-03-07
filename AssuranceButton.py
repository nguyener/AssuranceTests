from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AssuranceButton:

	def __init__(self, driver, button_text):
		self.button_element = WebDriverWait(driver, 10).until(
				EC.element_to_be_clickable((By.XPATH, '//button/span[text()="' + button_text + '"]/..')))
	
	def click(self):
		self.button_element.click()