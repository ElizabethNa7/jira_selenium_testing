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
def test_jira_task(driver):
    # Open Jira website
    driver.get("https://jira-selenium-test.atlassian.net/jira/your-work") # or https://id.atlassian.com/login?continue=https%3A%2F%2Fid.atlassian.com%2Fjoin%2Fuser-access%3Fresource%3Dari%253Acloud%253Ajira%253A%253Asite%252Fbd4c34f9-3e3e-43c2-b339-982f4295a7ec%26continue%3Dhttps%253A%252F%252Fjira-selenium-test.atlassian.net%252Fjira%252Fyour-work&application=jira

    WebDriverWait(driver, 15).until(
        EC.title_is("Log in to continue - Log in with Atlassian account")
    )
    # Assert - verify on login page
    assert driver.title == "Your work - Jira", \
        "The homepage did not load as expected!"
