from behave import fixture, use_fixture

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

@fixture
def selenium_browser_chrome(context):
    # -- HINT: @behave.fixture is similar to @contextlib.contextmanager
    options = Options()
    options.headless = True
    #options.add_argument('--ignore-certificate-errors')
    #options.add_argument('--user-data-dir=/tmp/chrome-data')
    context.browser = Chrome(options=options)
    context.browser.implicitly_wait(3)
    context.wait = WebDriverWait(context.browser, timeout=3)
    send_command = ('POST', '/session/$sessionId/chromium/send_command')
    context.browser.command_executor._commands['SEND_COMMAND'] = send_command
    # Halts all tests on error
    context.config.stop = True
    yield context.browser
    # -- CLEANUP-FIXTURE PART:
    context.browser.quit()

def before_feature(context, feature):
    use_fixture(selenium_browser_chrome, context)

def before_scenario(context, scenario):
    context.browser.execute('SEND_COMMAND', dict(cmd='Network.clearBrowserCookies', params={}))

def after_step(context, step):
    if step.status == "failed":
        print(context.browser.current_url)
        #print(context.browser.page_source)
