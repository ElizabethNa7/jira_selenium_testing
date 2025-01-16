import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from utils.json_helper import load_test_data
import time

test_data = load_test_data("utils/test_data.json")
config = load_test_data("utils/config.json")

# Pytest fixture for browser setup, to be used across multiple tests
@pytest.fixture(scope="session")
def driver():
    # Set up Chrome WebDriver
    service = Service(executable_path="/Users/elizabeth-na/Downloads/chromedriver-mac-x64/chromedriver") 
    
    # Open a webpage
    driver = webdriver.Chrome(service=service)
    # driver.maximize_window()
    yield driver  # Provide the driver to the test
    driver.quit()  # Quit the browser after the test


@pytest.fixture(scope="session")
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

    # if driver.title != "Log in to continue - Log in with Atlassian account":
    #     pytest.fail("Error: Page failed to load or an account is already logged in.")
    # else:
    login_button = driver.find_element(By.CLASS_NAME,"css-1kxou5n")
    login_button.click()
    
    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys(test_data["login"]["valid_user"]["username"] + Keys.ENTER)
    time.sleep(2)
    actions = ActionChains(driver)
    actions.send_keys(test_data["login"]["valid_user"]["password"] + Keys.ENTER).perform()

    # check for/handle two step verification page
    # https://id.atlassian.com/login/security-screen?token=eyJraWQiOiJtaWNyb3MvaWQtYXV0aGVudGljYXRpb24vOGdpdGJubjY1cDkzMzNydiIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJtaWNyb3MvaWQtYXV0aGVudGljYXRpb24iLCJjb250YWluZXJUeXBlIjoiZ2xvYmFsIiwiaXNzIjoibWljcm9zL2lkLWF1dGhlbnRpY2F0aW9uIiwicHJvdmlkZWRGYWN0b3JzIjpbIlBhc3N3b3JkIl0sInRyYW5zYWN0aW9uSWQiOiJ1cy13ZXN0LTJ8NmE4Njk2OWItMjUwZC00N2ZiLTljYWMtMWFhNzA4NjEzYjg5IiwiYWNjb3VudElkIjoiNzEyMDIwOjk1YThkMmMyLTM4MDQtNDUyZS1hOTQ5LWNhMzI0OWU3YjM3MCIsImF1ZCI6ImlkLWF1dGhlbnRpY2F0aW9uIiwibmJmIjoxNzM2OTA2MDQ3LCJzY29wZSI6Ik1mYVByb21vdGUiLCJleHAiOjE3MzY5MDY2NDcsImlhdCI6MTczNjkwNjA0NywianRpIjoidXMtd2VzdC0yfDU2MTFkOWM0LWE1MTUtNGRiNC04YWI1LWViZGYxNmZjZmEyYSIsImhhc2hlZENzcmZUb2tlbiI6IjQwOTJlN2M4MTQ3MjRhMGExZmZjOWIwMmRjZmViNGM4ZmRhMGU4NTQ1NTE0NzllZTA4ODljZWNlN2M0YzJlNzkifQ.jXuNv9LgF0Jn5DhAYdB_Byq1TPuDVoRTdpWG5OiUdO_W-VP0kfE8IrqikY0k1lYcjMapeSCMgw-DQLIQsqo4zT_ldWcccP_j8XuqX8RXfSMVyCrH535M5E3Z4p8AlaeVyKahFRz4E8ahpuqO6efmGxpyAgrD7KLCMcGeQJ-6h4ptyXO438kOUZjDVDpdRt1LdBEfsAaALYQ0T-EaCNHoUE61P4PF4bU4WwsDSw70JbzGu2LiORsHDiyZhb-4A9huoWQrfCvFD7ptkAg6QRXNV2cSX-RMTFJITzo7SoQg9u3Ifj4CrDBpnKtffkMZ5XJaRqAn0UvNU19ev7XKDtXytQ&continue=https%3A%2F%2Fid.atlassian.com%2Fjoin%2Fuser-access%3Fresource%3Dari%253Acloud%253Ajira%253A%253Asite%252Fbd4c34f9-3e3e-43c2-b339-982f4295a7ec%26continue%3Dhttps%253A%252F%252Fjira-selenium-test.atlassian.net%252Fjira%252Fyour-work
    try:
        two_step_verification_page = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "css-15r1rym"))
        )
        continue_without = driver.find_element(By.CLASS_NAME, "css-o54qoe")
        continue_without.click()
    except TimeoutException:
        print("no two-step verification page, continuing...")

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
        
        # return driver