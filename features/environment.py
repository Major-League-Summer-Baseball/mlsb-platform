'''
@author: Dallas Fraser
@author: 2018-11-05
@organization: MLSB
@summary: The environment variables used for creating and tearing down browser
'''

from behave import fixture, use_fixture
from selenium import webdriver
from api import app
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
BASE_URL = "http://localhost:5000"
DELAY = 5

def after_step(context, step):
    if step.status == "failed":
        step_str = step.name
        print("Failed a step, taking a screen shot")
        print(os.getcwd())
        # take a screen shot and save it


@fixture
def selenium_browser_chrome(context):

    # start the browser
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    context.browser = webdriver.Chrome(chrome_options=chrome_options)
    yield context.browser

    # clean up
    context.browser.quit()


@fixture
def selenium_browser_firefox(context):

    # start the browser
    context.browser = webdriver.Firefox()
    yield context.browser

    # clean up
    context.browser.quit()


def before_all(context):
    use_fixture(selenium_browser_chrome, context)