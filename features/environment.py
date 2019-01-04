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