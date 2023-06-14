from behave import fixture, use_fixture

from selenium.webdriver import Chrome, DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

@fixture
def selenium_browser_chrome(context):
    # -- HINT: @behave.fixture is similar to @contextlib.contextmanager
    options = Options()
    options.headless = True
    #options.add_argument('--ignore-certificate-errors')
    #options.add_argument('--user-data-dir=/tmp/chrome-data')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--remote-debugging-port=9222")  # this
    options.add_argument("--disable-dev-shm-using")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.set_capability('goog:loggingPrefs', { 'browser':'ALL' })

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
        print("url: ", context.browser.current_url)
        print("page source:")
        print("------")
        print(context.browser.page_source)
        print("------")
        print("console logs:")
        print("------")
        # print console logs
        for entry in context.browser.get_log('browser'):
            print(entry)
