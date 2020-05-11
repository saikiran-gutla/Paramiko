import time
import datetime
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from AwsInstances.aws_create_instance import create_aws_instance
from AwsLoggers.aws_loggers import get_logger
from UserExceptions.userexception import exception_device_not_found
from installation.install_agent import agent_install

from tests.AXUI.conftest import REALM, org_id

__my_logger = get_logger("UI_tests")


@pytest.mark.create_add_agent
def test_create_instance_add_agent():
    # Instance Name Should be give as win8,win10,win12,win16
    machines_to_create = ['win8', 'win10', 'win16']
    subnet = 'qe'
    realm = 'stg'
    machine_to_add = create_aws_instance(machines_to_create, subnet)
    time.sleep(150)
    device_key = '7061fed0-d08c-441d-9dfd-2cece8036e23'
    for instance in machine_to_add:
        agent_install(instance['ip_address'], instance['username'], instance['password'], realm, device_key)


@pytest.mark.exception_check
def test_exception_check(devices_page):
    driver = devices_page
    wait = WebDriverWait(driver, 15)  # 15 is max time
    # Takes the first available device and navigates to device details page
    ip_address = driver.find_element(By.XPATH, '//*[@id="devicesTable"]/tbody/tr[1]/td[7]').text
    __my_logger.info(f"IP ADDRESS : {ip_address}")
    driver.find_element(By.XPATH, '//*[@id="devicesTable"]/tbody/tr[1]/td[3]/span').click()
    __my_logger.debug('Open Device Details Page : PASSED')
    wait.until(
        expected_conditions.presence_of_element_located((By.XPATH,
                                                         '//*[@id="select2-chosen-2"]')))
    time.sleep(10)
    driver.find_element(By.XPATH,
                        "//div[contains(@class,'switch-wrapper')]//"
                        "label//div[contains(@class,'slider round')]").click()
    __my_logger.debug('Exception Toggle Click : PASSED')

    # clicking on dashboard page
    driver.find_element(By.XPATH, "/html/body/div[1]/div[7]/div/div/div[1]/nav/ul/li[1]/a/div").click()
    # wait until dashboard gets loaded
    wait.until(
        expected_conditions.presence_of_element_located((By.XPATH,
                                                         '//*[@id="alerts"]/div/button/span[1]')))
    driver.find_element(By.XPATH, "/html/body/div[1]/div[7]/div/div/div[2]/div[2]/div/div[4]/div[6]/div/div").click()
    __my_logger.debug('Click on Exception Devices Tile : PASSED')

    # get table rows and check device is available in the table or not
    time.sleep(10)
    number_of_devices = driver.find_elements_by_xpath(
        "//table[contains(@id,'devicesTable')]//tbody//tr//td[7]")
    exception_devices = []
    for row in number_of_devices:
        col = row.text
        __my_logger.info(f" Device Ip : {col}")
        __my_logger.info(f"Exception Device Ip : {col}")
        exception_devices.append(col)
    __my_logger.debug(f"Exception Devices List : {exception_devices}")
    if ip_address not in exception_devices:
        __my_logger.error(f'Device not found in the Exceptions list')
        raise exception_device_not_found(f'Device not found in the Exceptions list')
    time.sleep(20)


@pytest.mark.create_org
def test_create_org(login_page):
    driver = login_page
    wait = WebDriverWait(driver, 15)
    driver.find_element(By.XPATH, '//*[@id="userMenu"]/div[1]/a').click()
    time.sleep(5)
    # 2) Scroll Until the Element found in the page
    create_org = driver.find_element(By.LINK_TEXT, 'Create New Organization')
    driver.execute_script("arguments[0].scrollIntoView();", create_org)
    driver.find_element(By.XPATH, '//*[@id="createOrganization"]').click()
    __my_logger.info('Clicked on Create New Org')

    # Wait until Create organization button appears
    wait.until(
        expected_conditions.presence_of_element_located((By.XPATH,
                                                         '//*[@id="buttonCreateOrg"]')))
    date_time = datetime.datetime.now()
    month = date_time.strftime("%b")
    date = date_time.strftime("%d")
    org_name = 'Manual-Regression-' + month + date + '-script'

    # Creates the org
    driver.find_element(By.XPATH, '//*[@id="newOrgName"]').send_keys(org_name)
    driver.find_element(By.XPATH, '//*[@id="buttonCreateOrg"]').click()
    __my_logger.debug(f'Org Created With Name : {org_name}')
    time.sleep(10)
    driver.find_element(By.XPATH, '//*[@id="userMenu"]/div[1]/a/span[1]').click()
    time.sleep(5)

    # Scroll Until the Element with Created Org Name found in the page
    element = driver.find_element(By.LINK_TEXT, org_name)
    driver.execute_script("arguments[0].scrollIntoView();", element)
    __my_logger.info(f'Org {org_name} found in the orgs list')
    driver.find_element(By.LINK_TEXT, org_name).click()
    time.sleep(50)


@pytest.mark.dashboard_page
def test_dashboard_page(login_page):
    driver = login_page
    wait = WebDriverWait(driver, 15)  # 15 is max time
    driver.get(
        f'https://console.{REALM}.automox-dev.com/settings?o={org_id}')
    wait.until(
        expected_conditions.presence_of_element_located((By.XPATH,
                                                         '//*[@id="settingTabUserProfile"]/div[2]/div[2]/div[1]')))
    driver.find_element(By.XPATH, '/html/body/div[1]/div[7]/div/div/div[2]/div/div/div[2]/div/ul/li[2]/a').click()
    time.sleep(20)
    return driver


def tearDown(self):
    self.browser.close()
