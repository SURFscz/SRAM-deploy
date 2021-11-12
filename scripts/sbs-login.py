#!/usr/bin/env python

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

start = 'https://sbs.scz-vm.net/landing'

try:
    # Start browser
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
    wait.until(presence_of_element_located((By.XPATH, "//div[@class='user']/span")), 'Timeout waiting for SBS')

    '''
    browser.find_element_by_id('aup').click()
    browser.find_element_by_xpath("//a[text()='Store decision and continue']").click()

    # Test SBS title
    title = browser.title
    assert(title == "Research Access Management"), "Error loading SBS return url"

    # Find profile
    #profile = browser.find_element_by_xpath("//li[@class='user-profile']/a/span").click()
    '''

    # Test admin attributes
    attributes = browser.find_elements(By.XPATH, "//div[@class='user']/span")
    assert('SCZ Admin' in [a.text for a in attributes]), "No valid admin profile found"

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

