import json

from behave import *
from selenium.webdriver.support.expected_conditions import staleness_of, title_is, presence_of_element_located
from selenium.webdriver.common.by import By

@given('we visit {url}')
def step_impl(context, url):
    context.last_sub = None
    context.browser.get(url)

@given('we choose {idp}')
def step_impl(context, idp):
    # Wait for DS to load
    context.wait.until(title_is('SURF Research Access Management (Acceptance environment)'),
                       'Timeout waiting for landing page')

    # Click "Add another institution"
    add_button = context.browser.find_element(By.ID, 'add_button')
    if add_button.is_displayed():
        add_button.click()

    # Search IdP
    search = context.browser.find_element(By.ID, 'searchinput')
    search.send_keys(idp)

    # Wait for IdP to appear
    search = context.wait.until(presence_of_element_located(
        (By.XPATH, "//ul[@id='ds-search-list']/a[contains(@class,'identityprovider')]")),
        'Timeout waiting for result')

    context.browser.find_element(By.XPATH, f"//div[@class='text-truncate label primary' and text()='{idp}']").click()
    context.wait.until(staleness_of(search))

@given('we arrive at {url}')
def step_impl(context, url):
    # Wait for IdP to load
    assert(url in context.browser.current_url), "Error loading URL"

@when('we login as {user}')
def step_impl(context, user):
    # Login as user
    context.wait.until(presence_of_element_located(
        (By.XPATH, f"//form")),
        'Timeout waiting for result')
    test = user.split(':')
    username = test[0]
    password = test[1]
    context.browser.find_element_by_id('username').send_keys(username)
    context.browser.find_element_by_id('password').send_keys(password)
    context.browser.find_element_by_xpath('//button[@type="submit"]').click()

@then('sub is {sub}')
def step_impl(context, sub):
    context.wait.until(title_is('Test RP'),
                       'Timeout waiting for RP')

    # Test RP title
    title = context.browser.title
    assert(title == "Test RP"), "Error loading OP return url"

    # Test user attributes
    output = json.loads(context.browser.find_element_by_id('id_token').text)

    token_sub = output.get('sub', None)
    assert(token_sub == sub), "No valid identifier found"

