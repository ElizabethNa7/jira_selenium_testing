import pytest 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# Initialize WebDriver (Chrome in this case)
service = Service(executable_path="/Users/elizabeth-na/Downloads/chromedriver-mac-x64/chromedriver") 
driver = webdriver.Chrome(service=service)

# Open a webpage
driver.get("https://jira-selenium-test.atlassian.net/jira/your-work")

# Wait for results to load
time.sleep(10)

# Close the browser
driver.quit()
