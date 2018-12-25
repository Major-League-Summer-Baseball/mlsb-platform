'''
@author: Dallas Fraser
@author: 2018-11-05
@organization: MLSB
@summary: The environment variables used for creating and tearing down browser
'''

from behave import fixture, use_fixture
from selenium import webdriver
from api import app
BASE_URL = "http://localhost:5000"
DELAY = 5


@fixture
def selenium_browser_chrome(context):

    # start the browser
    context.browser = webdriver.Chrome()
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