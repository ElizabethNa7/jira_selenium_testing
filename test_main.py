from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# Initialize WebDriver (Chrome in this case)
service = Service(executable_path="/Users/elizabeth-na/Downloads/chromedriver-mac-x64/chromedriver") 
driver = webdriver.Chrome(service=service)

# Open a webpage
driver.get("https://www.google.com/")

# Find the search box, type a query, and hit Enter
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Selenium Python")
search_box.submit()

# Wait for results to load
time.sleep(5)

# Close the browser
driver.quit()
