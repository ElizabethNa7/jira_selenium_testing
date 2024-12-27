import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

import time

# Define a Pytest fixture for browser setup
@pytest.fixture
def driver():
    # Set up Chrome WebDriver
    service = Service(executable_path="/Users/elizabeth-na/Downloads/chromedriver-mac-x64/chromedriver") 
    
    # Open a webpage
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver  # Provide the driver to the test
    driver.quit()  # Quit the browser after the test


# Test case: Open Jira and verify the login popup
def test_open_jira_login(driver):
    # Open Jira website
    driver.get("https://jira-selenium-test.atlassian.net/jira/your-work") # or https://id.atlassian.com/login?continue=https%3A%2F%2Fid.atlassian.com%2Fjoin%2Fuser-access%3Fresource%3Dari%253Acloud%253Ajira%253A%253Asite%252Fbd4c34f9-3e3e-43c2-b339-982f4295a7ec%26continue%3Dhttps%253A%252F%252Fjira-selenium-test.atlassian.net%252Fjira%252Fyour-work&application=jira
    time.sleep(3)

    # Click the "Login" button to open the login page/popup
    login_button = driver.find_element(By.CLASS_NAME,"css-1kxou5n")
    login_button.click()
    
    # input_element.clear() # used to just clear the element (the search bar in this case) in case it has anything in it already
    username_field = WebDriverWait(driver, 10).until(  # 10-second timeout
        EC.presence_of_element_located((By.ID, "username"))
    )
    username_field.send_keys("elizabeth.na@hcltech.com" + Keys.ENTER)

    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element_value((By.ID, "username"), "elizabeth.na@hcltech.com")
    )
    
    # Verify that the login form is displayed
    assert username_field.is_displayed(), "Login form did not load!"
