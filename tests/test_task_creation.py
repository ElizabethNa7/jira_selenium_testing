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

@pytest.mark.dependency(depends=["login"])
@pytest.fixture(scope="session")
def test_create_task(driver):
    assert "Your work - Jira" in driver.title, "Not on 'Your work - Jira' homepage"