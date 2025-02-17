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


# note Selenium IDE project jira_task_creation (task)

# prob not this
#  <div class="sc-1xw97h-1 kxBhil"><p class="sc-1xw97h-2 dOQnsx" data-testid="deep-dive-card-content--project-name-heading">Selenium Testing</p><p data-testid="deep-dive-card-content--project-type-subheading" class="_11c81vlj _19pkidpf _2hwxidpf _otyridpf _18u0idpf _1reo15vq _18m915vq _syaz1fxt _1bto1l2s _o5721q9c _1p1dglyw">Team-managed software</p></div>
# use this to determine correct project: <p class="sc-1xw97h-2 dOQnsx" data-testid="deep-dive-card-content--project-name-heading">Selenium Testing</p>
# also use the correct "My open issues" dropdown: <p class="sc-1xw97h-7 kkiCXI" data-testid="deep-dive-card-content--dropdown--content--filter-link--tool-tip-container--filter-title">My open issues</p>

# create task button:
# <div role="listitem" data-testid="create-button-wrapper" class="css-1ou36x4"><button id="createGlobalItem" aria-label="Create issue" data-hide-on-smallscreens="true" class="css-1g6jj8c" data-testid="atlassian-navigation--create-button" tabindex="0" type="button"><span class="css-178ag6o">Create</span></button><button aria-label="Create" id="createGlobalItemIconButton" data-hide-on-largescreens="true" class="css-ms9xpr" data-testid="atlassian-navigation--create-icon-button" tabindex="0" type="button"><span class="css-bwxjrz"><span data-vc="icon-undefined" role="img" aria-label="Create" class="css-snhnyn" style="--icon-primary-color: currentColor; --icon-secondary-color: var(--ds-surface, #FFFFFF);"><svg width="24" height="24" viewBox="0 0 24 24" role="presentation"><path fill="currentcolor" fill-rule="evenodd" d="M13 11V7a1 1 0 0 0-2 0v4H7a1 1 0 0 0 0 2h4v4a1 1 0 0 0 2 0v-4h4a1 1 0 0 0 0-2z"></path></svg></span></span></button></div>