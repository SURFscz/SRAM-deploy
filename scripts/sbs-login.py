#!/usr/bin/env python

import time
import json
import traceback
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of, title_is, presence_of_element_located
from selenium.webdriver.common.by import By


class CustomChrome(Chrome):
    def get(self, url) -> None:
        print(f"Fetching page '{url}'")
        return super(CustomChrome, self).get(url)


options = Options()
options.headless = True
options.add_argument('ignore-certificate-errors')
browser = CustomChrome(options=options)
wait = WebDriverWait(browser, timeout=2)

send_command = ('POST', '/session/$sessionId/chromium/send_command')
browser.command_executor._commands['SEND_COMMAND'] = send_command

health = 'https://sbs.scz-vm.net/health'
start = 'https://sbs.scz-vm.net/landing'
profile = 'https://sbs.scz-vm.net/profile'

try:
    # Wait for SBS health up
    status = ""
    while status != "UP":
        browser.get(health)
        state = json.loads(browser.find_element(By.XPATH, "//pre").text)
        status = state.get("status")
        time.sleep(1)

    # Get SBS start page, MFA test
    browser.get(start)

    # Wait for login button
    wait.until(presence_of_element_located((By.XPATH, "//a[@href='/Login']")),
               'Timeout waiting for Login button')

    # Click login
    login = browser.find_element(By.XPATH, "//a[@href='/Login']")
    login.click()

    # Wait for login button to disappear
    wait.until(staleness_of(login), 'Timeout waiting for login page')

    # Select ACR = MFA
    browser.find_element(By.ID, 'acr_mfa').click()

    # Login as admin
    browser.find_element(By.ID, 'username').send_keys('admin')
    browser.find_element(By.ID, 'password').send_keys('admin')
    browser.find_element(By.TAG_NAME, 'form').submit()

    # Wait for user profile to appear
    wait.until(presence_of_element_located((By.XPATH, "//label[@for='aup']")), 'Timeout waiting for AUP')

    browser.find_element(By.XPATH, "//label[@for='aup']").click()
    browser.find_element(By.XPATH, "//a[text()='Looks good, onwards']").click()

    # Wait for landing page
    wait.until(presence_of_element_located((By.XPATH, "//div[@class='drop-down ugly']")), 'Timeout waiting for Welcome')

    # Visit Profile
    browser.get(profile)

    # Wait for Profile to load
    wait.until(presence_of_element_located((By.XPATH, "//div[@class='user-profile-tab']")),
               'Timeout waiting for Profile')

    # Test admin attributes
    attributes = browser.find_elements(By.XPATH, "//div[@class='user-profile-tab']/*/*")
    # for a in attributes:
    #     print(f"a.text: {a.text}")
    assert('SCZ Admin' in [a.text for a in attributes]), "No valid admin profile found"

    # Clear all cookies
    browser.execute('SEND_COMMAND',
                    dict(cmd='Network.clearBrowserCookies', params={}))

    # Get SBS start page, non-MFA test
    browser.get(start)

    # Wait for login button
    wait.until(presence_of_element_located((By.XPATH, "//a[@href='/Login']")),
               'Timeout waiting for Login button')

    # Click login
    login = browser.find_element(By.XPATH, "//a[@href='/Login']")
    login.click()

    # Wait for login button to disappear
    wait.until(staleness_of(login), 'Timeout waiting for login page')

    # Select ACR = MFA
    browser.find_element(By.ID, 'acr_password').click()

    # Login as admin
    browser.find_element(By.ID, 'username').send_keys('user1')
    browser.find_element(By.ID, 'password').send_keys('user1')
    browser.find_element(By.TAG_NAME, 'form').submit()

    # Wait for user profile to appear
    wait.until(presence_of_element_located((By.XPATH, "//label[@for='aup']")), 'Timeout waiting for AUP')

    browser.find_element(By.XPATH, "//label[@for='aup']").click()
    browser.find_element(By.XPATH, "//a[text()='Looks good, onwards']").click()

    # Wait for 2fa information
    wait.until(presence_of_element_located((By.XPATH, "//div[@class='information']")), 'Timeout waiting for 2FA')

    # Assert 2fa page
    assert("2fa" in browser.current_url), "Error loading 2FA URL"

    # Close browser
    browser.close()
    print('success')

except Exception as e:
    url = browser.current_url
    print(f"url: {url}")

    tr = traceback.extract_tb(e.__traceback__)[0]
    print(f"error {e.args[0]} on line {tr.lineno} of '{tr.filename}'")
    print("  ", tr.line)

    print("error: ", e.args[0])

    from bs4 import BeautifulSoup
    page = BeautifulSoup(browser.page_source, 'html.parser').prettify()
    print(f"page:")
    print(page)
    with open("page.html", "w") as f:
        f.write(page)

    browser.save_screenshot("screenshot.png")
    browser.close()

    print("", end="", flush=True)
    exit(1)
