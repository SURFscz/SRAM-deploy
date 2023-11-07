#!/usr/bin/env python

import time
import json
import traceback
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of, presence_of_element_located
from selenium.webdriver.common.by import By


class CustomChrome(Chrome):
    def get(self, url) -> None:
        print(f"Fetching page '{url}'")
        return super(CustomChrome, self).get(url)


options = Options()
options.add_argument('--headless')
options.add_argument('ignore-certificate-errors')
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

browser = CustomChrome(options=options)
wait = WebDriverWait(browser, timeout=3)

send_command = ('POST', '/session/$sessionId/chromium/send_command')
browser.command_executor._commands['SEND_COMMAND'] = send_command

health = 'https://sbs.scz-vm.net/health'
start = 'https://sbs.scz-vm.net/landing'
profile = 'https://sbs.scz-vm.net/profile'

xpath_login_button = '//button[span[text()="Log in"]]'
xpath_logo = '//a[@class="logo"]//span[text()="Research Access Management"]'

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
    wait.until(presence_of_element_located((By.XPATH, xpath_login_button)),
               'Timeout waiting for Login button')

    # Click login
    login = browser.find_element(By.XPATH, xpath_login_button)
    login.click()
    print(" - pressed login")

    # Wait for login button to disappear
    wait.until(staleness_of(login), 'Timeout waiting for login page')

    # Select ACR = MFA
    browser.find_element(By.ID, 'acr_mfa').click()

    # Login as admin
    browser.find_element(By.ID, 'username').send_keys('admin')
    browser.find_element(By.ID, 'password').send_keys('admin')
    browser.find_element(By.TAG_NAME, 'form').submit()
    print(" - logged in as admin")

    # Wait for user profile to appear
    wait.until(presence_of_element_located((By.XPATH, "//label[@for='aup']")), 'Timeout waiting for AUP')

    browser.find_element(By.XPATH, "//label[@for='aup']").click()
    browser.find_element(By.XPATH, "//button[span[text()='Onwards']]").click()
    print(" - accepted AUP")

    # Wait for landing page
    wait.until(presence_of_element_located((By.XPATH, xpath_logo)),
               'Timeout waiting for logo')
    print(" - landing page")

    time.sleep(1)

    # Visit Profile
    browser.get(profile)

    # Wait for Profile to load
    wait.until(presence_of_element_located((By.XPATH, "//h2[text()='Your profile']")),
               'Timeout waiting for Profile')

    # Test admin attributes
    attributes = browser.find_elements(By.XPATH, "//table[@class='my-attributes']/*/*/*")
    # for a in attributes:
    #     print(f"a.text: {a.text}")
    assert ('SCZ Admin' in [a.text for a in attributes]), "No valid admin profile found"
    print(" - profile ok")

    # Clear all cookies
    browser.execute('SEND_COMMAND',
                    dict(cmd='Network.clearBrowserCookies', params={}))

    # Get SBS start page, non-MFA test
    browser.get(start)

    # Wait for login button
    wait.until(presence_of_element_located((By.XPATH, xpath_login_button)),
               'Timeout waiting for Login button')

    # Click login
    login = browser.find_element(By.XPATH, xpath_login_button)
    login.click()
    print(" - pressed login")

    # Wait for login button to disappear
    wait.until(staleness_of(login), 'Timeout waiting for login page')

    # Select ACR = MFA
    browser.find_element(By.ID, 'acr_password').click()

    # Login as admin
    browser.find_element(By.ID, 'username').send_keys('user1')
    browser.find_element(By.ID, 'password').send_keys('user1')
    browser.find_element(By.TAG_NAME, 'form').submit()
    print(" - logged in as user1")

    # Wait for user profile to appear
    wait.until(presence_of_element_located((By.XPATH, "//label[@for='aup']")), 'Timeout waiting for AUP')

    browser.find_element(By.XPATH, "//label[@for='aup']").click()
    browser.find_element(By.XPATH, "//button[span[text()='Onwards']]").click()
    print(" - accepted AUP")

    # Wait for next page
    wait.until(presence_of_element_located(
        (By.XPATH, xpath_logo)),
        'Timeout waiting for 2FA')
    print(" - reached next page")

    # Assert 2fa page
    # assert ("2fa" in browser.current_url), "Error loading 2FA URL"
    # print(" - reached 2FA page")

    # Close browser
    browser.close()
    print('success')

except Exception as e:
    url = browser.current_url
    print(f"url: {url}")

    tr = traceback.extract_tb(e.__traceback__)[0]
    print(f"error {type(e).__name__} on line {tr.lineno} of '{tr.filename}'")
    print("  ", tr.line)

    from bs4 import BeautifulSoup
    page = BeautifulSoup(browser.page_source, 'html.parser').prettify()
    with open("page.html", "w") as f:
        f.write(page)

    with open("console.txt", "w") as f:
        for entry in browser.get_log('browser'):
            f.write(str(entry) + "\n")

    browser.save_screenshot("screenshot.png")
    browser.close()

    print("", end="", flush=True)
    exit(1)
