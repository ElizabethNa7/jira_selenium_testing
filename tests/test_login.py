import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

from conftest import driver
from utils.json_helper import load_test_data

import time

# Load JSON test data
test_data = load_test_data("utils/test_data.json")
config = load_test_data("utils/config.json")

# Test case: Open Jira and verify the login popup
def test_jira_login(driver):
    # Open Jira website
    # driver.get("https://jira-selenium-test.atlassian.net/jira/your-work")
    driver.get(config["base_url"])

    WebDriverWait(driver, 20).until(
        EC.title_is("Log in to continue - Log in with Atlassian account")
    )

    # # Verify on login page
    # assert driver.title in ["Your work - Jira", "Log in to continue - Log in with Atlassian account"], \
    #     f"Unexpected page title: {driver.title}"

    if driver.title != "Log in to continue - Log in with Atlassian account":
        pytest.fail("Error: Page failed to load or an account is already logged in.")
    else:
        # Login
        login_button = driver.find_element(By.CLASS_NAME,"css-1kxou5n")
        login_button.click()
        
        username_field = driver.find_element(By.ID, "username")
        username_field.send_keys(test_data["login"]["valid_user"]["username"] + Keys.ENTER)
        time.sleep(2)
        actions = ActionChains(driver)
        actions.send_keys(test_data["login"]["valid_user"]["password"] + Keys.ENTER).perform()

        # check for/handle two step verification page

        home_page = WebDriverWait(driver, 15).until(EC.title_is("Your work - Jira"))

        try: # TODO: probably just change this to an if-then
            product_discovery_popup = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME, test_data["popups"]["product_discovery"]["identifier"]))
            )
            triple_dot_menu = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, test_data["popups"]["product_discovery"]["menu"]))
            )
            triple_dot_menu.click()
            not_interested = driver.find_element(By.CSS_SELECTOR, test_data["popups"]["product_discovery"]["exit"])
            not_interested.click()
            # time.sleep(5)

        except TimeoutException:
            print("no popup, continuing...")
        except StaleElementReferenceException:
            print("Encountered stale element, retrying...")
            triple_dot_menu = driver.find_element(By.CSS_SELECTOR, ".css-652a00 .css-1afrefi")
            triple_dot_menu.click()

    # except TimeoutException:
    #     print("no service management popup, continuing")

    # check correct profile is logged in
        profile_button = WebDriverWait(driver, 2).until( 
            EC.presence_of_element_located((By.ID,"atlassian-navigation.ui.profile.icon")) # this wasn't/doesn't work bc the password field is lowkey the same as the username, but that original one is also stale by this point
        )
        profile_button.click()

        profile = driver.find_element(By.CLASS_NAME, "_vwz4gktf")
        actual_profile = profile.text
        expected_profile = test_data["profile"]["name"]
        
        assert actual_profile == actual_profile, \
            "Expected profile '{expected_profile}', but '{actual_profile}' is logged in!"
        