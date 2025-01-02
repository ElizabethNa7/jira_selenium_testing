import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Define a Pytest fixture for browser setup
@pytest.fixture
def driver():
    # Set up Chrome WebDriver
    service = Service(executable_path="/Users/elizabeth-na/Downloads/chromedriver-mac-x64/chromedriver") 
    
    # Open a webpage
    driver = webdriver.Chrome(service=service)
    # driver.maximize_window()
    yield driver  # Provide the driver to the test
    driver.quit()  # Quit the browser after the test
