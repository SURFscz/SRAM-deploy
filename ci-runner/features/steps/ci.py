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

@then('tokens are {file}')
def step_impl(context, file):
    context.wait.until(title_is('Test RP'),
                       'Timeout waiting for RP')

    # Test RP title
    title = context.browser.title
    assert(title == "Test RP"), "Error loading OP return url"

    # Test user attributes
    id_token = json.loads(context.browser.find_element_by_id('id_token').text)
    access_token = json.loads(context.browser.find_element_by_id('access_token').text)
    user_info = json.loads(context.browser.find_element_by_id('user_info').text)

    with open(file) as f:
        user_claims = json.load(f)

    for claim, value in user_claims['id_token'].items():
        if type(value) is list:
            assert(set(id_token[claim]) == set(value)), f"id_token {claim} did not contain {value}"
        else:
            assert(id_token[claim] == value), f"id_token {claim} did not contain {value}"

    for claim, value in user_claims['access_token'].items():
        if type(value) is list:
            assert(set(access_token[claim]) == set(value)), f"access_token {claim} did not contain {value}"
        else:
            assert(access_token[claim] == value), f"access_token {claim} did not contain {value}"

    for claim, value in user_claims['user_info'].items():
        if type(value) is list:
            assert(set(user_info[claim]) == set(value)), f"user_info {claim} did not contain {value}"
        else:
            assert(user_info[claim] == value), f"user_info {claim} did not contain {value}"
