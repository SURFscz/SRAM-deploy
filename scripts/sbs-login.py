#!/usr/bin/env python
# -*- coding: future_fstrings -*-

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of, title_is, presence_of_element_located
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

options = Options()
options.headless = True
options.add_argument('ignore-certificate-errors')
browser = Chrome(executable_path='./scripts/chromedriver', options=options)
wait = WebDriverWait(browser, timeout=2)

start = 'https://sbs.scz-vm.net/landing'

try:
    # Start browser
    browser.get(start)

    # Wait for SBS to load
    wait.until(title_is('Research Access Management'), 'Timeout waiting for landing page')

    # Click login
    login = browser.find_element_by_xpath("//a[@href='/login' and text()='Login']")
    login.click()

    # Wait for login button to disappear
    wait.until(staleness_of(login), 'Timeout waiting for login page')

    # Login as admin
    browser.find_element_by_id('username').send_keys('admin')
    browser.find_element_by_id('password').send_keys('admin')
    browser.find_element_by_tag_name('form').submit()

    # Wait for user profile to appear
    wait.until(presence_of_element_located((By.XPATH, "//li[@class='user-profile']")), 'Timeout waiting for user profile')

    # Test SBS title
    title = browser.title
    assert(title == "Research Access Management"), "Error loading SBS return url"

    # Click profile dropdown
    profile = browser.find_element_by_xpath("//li[@class='user-profile']/a/span").click()

    # Test admin attributes
    attributes = browser.find_elements_by_xpath("//ul[@class='user-profile']/li/span[@class='value']")
    assert('admin' in [a.text for a in attributes]), "No valid admin profile found"

    # Close browser
    browser.close()
    print('success')

except Exception as e:
    url = browser.current_url
    print(f"url: {url}")
    page = browser.page_source
    print(f"page: {page}")
    browser.close()
    exit(e)

