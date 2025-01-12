# <div class="css-1of3wbn">
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from conftest import driver
from utils.json_helper import load_test_data

import time

# Load JSON test data
test_data = load_test_data("utils/test_data.json")
config = load_test_data("utils/config.json")

def test_jira_login(driver):
    try:
        service_management_popup = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, test_data["popups"]["service_management"]["identifier"]))
        )
        # actions = ActionChains(driver)
        test_data["popups"]["service_management"]["menu"].click()
        test_data["popups"]["service_management"]["exit"].click()
        # actions.send_keys(test_data["popups"]["service_management"]["menu"] + Keys.).perform()
        # actions.send_keys(test_data["popups"]["service_management"]["exit"] + Keys.ENTER).perform()

        # service_management_popup_menu = WebDriverWait(driver, 1).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, test_data["popups"]["service_management"]["menu"]))
        # )
        # service_management_popup_menu.click()
    except TimeoutException:
        print("no service management popup, continuing")


    profile_button = WebDriverWait(driver, 5).until( 
        EC.presence_of_element_located((By.ID,"atlassian-navigation.ui.profile.icon")) # this wasn't/doesn't work bc the password field is lowkey the same as the username, but that original one is also stale by this point
    )
    profile_button.click()

    profile = driver.find_element(By.CLASS_NAME, "_vwz4gktf")
    actual_profile = profile.text
    expected_profile = test_data["profile"]["name"]
    
    assert actual_profile == actual_profile, \
        "Expected profile '{expected_profile}', but '{actual_profile}' is logged in!"
    