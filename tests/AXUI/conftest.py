import pytest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from AwsLoggers.aws_loggers import get_logger

my_logger = get_logger("UI_tests")
user_name = 'mark@patchsimple.com'
user_pass = 'markmark'
REALM = 'stg'
org_id = 18722


@pytest.fixture(name="setUp", scope='session')
def setUp():
    browser = webdriver.Chrome()
    my_logger.info("Chrome WebDriver Setup Successfull")
    return browser


@pytest.fixture(name="login_page", scope='session')
def login_page(setUp):
    """
    This fixture will login the user and takes you to the dashboard page
    Args:
        setUp: Fixture to setup the chrome driver

    Returns:

    """
    browser = setUp
    my_logger.debug('loading.....')
    browser.get(f"https://console.{REALM}.automox-dev.com/login")
    wait = WebDriverWait(browser, 5000)  # 15 is max time
    wait.until(expected_conditions.presence_of_element_located((By.ID, 'next')))
    browser.find_element(By.XPATH, '//*[@id="username"]').send_keys(user_name)
    browser.find_element(By.XPATH, '//*[@id="next"]').click()
    my_logger.debug('something is clicked')
    browser.implicitly_wait(5)
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys(user_pass)
    browser.find_element(By.XPATH, '//*[@id="login"]').click()
    # Wait until notification appears in the dashboard page
    wait.until(
        expected_conditions.presence_of_element_located((By.XPATH,
                                                         '//*[@id="alerts"]/div/button/span[1]')))
    return browser


@pytest.fixture(name="devices_page", scope='session')
def devices_page(login_page):
    driver = login_page
    wait = WebDriverWait(driver, 3000)  # 15 is max time
    driver.get(
        f'https://console.{REALM}.automox-dev.com/devices?o=' + str(
            org_id) + '&limit=25&order_by=display_name&sort_dir=asc')
    # Wait until the select pagination appears in the devices page
    wait.until(
        expected_conditions.presence_of_element_located((By.XPATH,
                                                         '//*[@id="select2-chosen-2"]')))
    return driver


@pytest.fixture(name="dashboard", scope='session')
def test_dashboard_page(setUp):
    driver = setUp
    wait = WebDriverWait(driver, 15)  # 15 is max time
    driver.get(
        f'https://console.{REALM}.automox-dev.com/dashboard?o={org_id}')
    wait.until(
        expected_conditions.presence_of_element_located((By.XPATH,
                                                         '//*[@id="alerts"]/div/button/span[1]')))
    return driver
