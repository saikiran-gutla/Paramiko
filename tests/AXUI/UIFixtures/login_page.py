import time
import unittest

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

user_name = 'mark@patchsimple.com'
user_pass = 'markmark'


class LoginPage():

    def setUp(self):
        self.browser = webdriver.Chrome()

    @pytest.fixture(name="login_page", scope='session')
    def login_page(self):
        self.browser.get("https://console.stg.automox-dev.com/login")
        wait = WebDriverWait(self.browser, 15)  # 15 is max time
        self.browser.find_element(By.XPATH, '//*[@id="username"]').send_keys(user_name)
        self.browser.find_element(By.XPATH, '//*[@id="next"]').click()
        self.browser.implicitly_wait(5)  # seconds
        # element = wait.until(
        #     expected_conditions.presence_of_element_located((By.ID, 'password')))
        # expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="password"]')))
        # wait.until(expected_conditions.element_to_be_clickable(By.XPATH('//*[@id="password"]')))

        self.browser.find_element(By.XPATH, '//*[@id="password"]').send_keys(user_pass)
        self.browser.find_element(By.XPATH, '//*[@id="login"]').click()
        wait.until(
            expected_conditions.presence_of_element_located((By.XPATH,
                                                             '/html/body/div[1]/div[7]/div/div/div[2]/div[2]/div/div[4]/div[2]/div/div/div[2]')))
        # self.assertTrue(next_button.is_displayed())
        # time.sleep(90)
