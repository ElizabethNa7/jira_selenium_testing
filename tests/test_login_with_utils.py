import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from conftest import driver
from utils.json_helper import load_test_data

import time

# Load JSON test data
test_data = load_test_data("utils/test_data.json")
config = load_test_data("utils/config.json")
print(f"test_data: {test_data} and config: {config}")

# Test case: Open Jira and verify the login popup
def test_jira_task(driver):
    # Open Jira website
    # driver.get("https://jira-selenium-test.atlassian.net/jira/your-work")
    driver.get(config["base_url"])

    WebDriverWait(driver, 15).until(
        EC.any_of(
            EC.title_is("Your work - Jira"),
            EC.title_is("Log in to continue - Log in with Atlassian account")
        )
    )
    # Assert - verify on login page
    assert driver.title == "Your work - Jira" or "Log in to continue - Log in with Atlassian account", \
        "The homepage did not load as expected!"

    # Login
    login_button = driver.find_element(By.CLASS_NAME,"css-1kxou5n")
    login_button.click()
    
    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys(test_data["login"]["valid_user"]["username"] + Keys.ENTER)
    time.sleep(2)
    actions = ActionChains(driver)
    actions.send_keys(test_data["login"]["valid_user"]["password"] + Keys.ENTER).perform()

   # check correct profile is logged in
    profile_button = WebDriverWait(driver, 5).until( 
        EC.presence_of_element_located((By.ID,"atlassian-navigation.ui.profile.icon")) # this wasn't/doesn't work bc the password field is lowkey the same as the username, but that original one is also stale by this point
    )
    profile_button.click()

    profile = driver.find_element(By.CLASS_NAME, "_vwz4gktf")
    actual_profile = profile.text
    expected_profile = test_data["profile"]["name"]
    
    assert actual_profile == actual_profile, \
        "Expected profile '{expected_profile}', but '{actual_profile}' is logged in!"
    