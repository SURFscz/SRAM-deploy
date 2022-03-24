#!/usr/bin/env python

import time
import json
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of, title_is, presence_of_element_located
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

options = Options()
options.headless = True
options.add_argument('ignore-certificate-errors')
browser = Chrome(options=options)
wait = WebDriverWait(browser, timeout=2)

health = 'https://sbs.scz-vm.net/landing'
start = 'https://sbs.scz-vm.net/landing'
profile = 'https://sbs.scz-vm.net/profile'

try:
    # Wait for SBS health up
    status = ""
    while status != "UP":
        browser.get(health)
        state = json.loads(browser.page_source)
        status = state.get("status")
        time.sleep(1)

    browser.get(start)

    # Wait for SBS to load
    wait.until(title_is('Research Access Management'), 'Timeout waiting for landing page')

    # Click login
    login = browser.find_element(By.XPATH, "//a[@href='/Login' and text()='Login']")
    login.click()

    # Wait for login button to disappear
    wait.until(staleness_of(login), 'Timeout waiting for login page')

    # Login as admin
    browser.find_element(By.ID, 'username').send_keys('admin')
    browser.find_element(By.ID, 'password').send_keys('admin')
    browser.find_element(By.TAG_NAME, 'form').submit()

    # Wait for user profile to appear
    wait.until(presence_of_element_located((By.XPATH, "//label[@for='aup']")), 'Timeout waiting for AUP')

    browser.find_element(By.XPATH, "//div[@class='checkbox']").click()
    browser.find_element(By.XPATH, "//a[text()='Looks good, onwards']").click()

    # Wait for landing page
    wait.until(presence_of_element_located((By.XPATH, "//div[@class='drop-down ugly']")), 'Timeout waiting for Welcome')

    # Visit Profile
    browser.get(profile)

    # Wait for Profile to load
    wait.until(presence_of_element_located((By.XPATH, "//div[@class='user-profile-tab']")), 'Timeout waiting for Profile')

    # Test admin attributes
    attributes = browser.find_elements(By.XPATH, "//div[@class='user-profile-tab']/*/*")
    # for a in attributes:
    #     print(f"a.text: {a.text}")
    assert('SCZ Admin' in [a.text for a in attributes]), "No valid admin profile found"

    # Close browser
    browser.close()
    print('success')

except Exception as e:
    url = browser.current_url
    print(f"url: {url}")
    page = browser.page_source
    print(f"page: {page}")
    browser.save_screenshot("screenshot.png")
    browser.close()
    exit(e)
