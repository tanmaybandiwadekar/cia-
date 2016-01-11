# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from pyvirtualdisplay import Display
import logging

logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('myapp.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

class ButtonClick(unittest.TestCase):
    def setUp(self):
        self.display = Display(visible=0, size=(1900, 1200))
        self.display.start()
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost:8000/simple/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_button_click(self):
        try:
            driver = self.driver
            driver.get(self.base_url + "/simple/")
            driver.find_element_by_id("button1").click()
            self.assertEqual("Button 1 Clicked", driver.find_element_by_id("button1text").text)
            # driver.find_element_by_id("button2").click()
            #  self.assertEqual("Button 2 Clicked", driver.find_element_by_id("button2text").text)
            logger.info("Test Passed")
        except Exception as e:
            logger.error("Test Failed")
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
	self.display.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
