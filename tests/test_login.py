import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from fixtures.driver_setup import driver
import time

# Test case: Open Jira and verify the login popup
def test_jira_login(driver):
    # Open Jira website
    driver.get("https://jira-selenium-test.atlassian.net/jira/your-work") # or https://id.atlassian.com/login?continue=https%3A%2F%2Fid.atlassian.com%2Fjoin%2Fuser-access%3Fresource%3Dari%253Acloud%253Ajira%253A%253Asite%252Fbd4c34f9-3e3e-43c2-b339-982f4295a7ec%26continue%3Dhttps%253A%252F%252Fjira-selenium-test.atlassian.net%252Fjira%252Fyour-work&application=jira

    WebDriverWait(driver, 15).until(
        EC.title_is("Log in to continue - Log in with Atlassian account")
    )
    # Assert - verify on login page
    assert driver.title == "Log in to continue - Log in with Atlassian account", \
        "The login page did not load as expected!"


    # Login
    login_button = driver.find_element(By.CLASS_NAME,"css-1kxou5n")
    login_button.click()
    
    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys("elizabeth.na@hcltech.com" + Keys.ENTER)
    
    time.sleep(3)
    actions = ActionChains(driver)
    actions.send_keys("LizziE2869950." + Keys.ENTER).perform()

    # login_button = driver.find_element(By.CLASS_NAME, "css-1xfynbg") # not needed bc earlier we press ENTER
    # login_button.click()

    # maybe make an IF statement for this
    # time.sleep(7)
    # enable_two_step_verification = WebDriverWait(driver, 10).until( 
    #     EC.presence_of_element_located((By.CLASS_NAME,"css-178ag6o")) 
    # )
    # enable_two_step_verification.click()

    # check correct profile is logged in
    profile_button = WebDriverWait(driver, 5).until( 
        EC.presence_of_element_located((By.ID,"atlassian-navigation.ui.profile.icon")) # this wasn't/doesn't work bc the password field is lowkey the same as the username, but that original one is also stale by this point
    )
    profile_button.click()

    profile = driver.find_element(By.CLASS_NAME, "_vwz4gktf")
    actual_profile = profile.text
    expected_profile = "Elizabeth Na"
    
    assert actual_profile == actual_profile, \
        "Expected profile '{expected_profile}', but '{actual_profile}' is logged in!"
    
    # Testing321! for optional testing profile
