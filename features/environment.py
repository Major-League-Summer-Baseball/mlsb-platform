'''
@author: Dallas Fraser
@author: 2018-11-05
@organization: MLSB
@summary: The environment variables used for creating and tearing down browser
'''

from behave import fixture, use_fixture
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import os
BASE_URL = "http://localhost:8080"
DELAY = 5


def after_step(context, step):
    if step.status == "failed":

        # take a screen shot and save it
        if not os.path.exists("failed_scenarios_screenshots"):
            os.makedirs("failed_scenarios_screenshots")
        context.browser.save_screenshot(
            os.path.join(os.getcwd(),
                         "failed_scenarios_screenshots",
                         step.name + "_failed.png"))
        print("Failed a step, taking a screen shot")
        print(os.getcwd())


def after_scenario(context, scenario):
    if scenario.status == "failed":
        if not os.path.exists("failed_scenarios_screenshots"):
            os.makedirs("failed_scenarios_screenshots")
        context.browser.save_screenshot(
            os.path.join(os.getcwd(),
                         "failed_scenarios_screenshots",
                         scenario.name + "_failed.png"))


@fixture
def selenium_browser_chrome(context):

    # start the browser
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--window-size=1920,1080")

    
    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['acceptSslCerts'] = True 
    capabilities['acceptInsecureCerts'] = True

    context.browser = webdriver.Chrome(chrome_options=chrome_options,
                                       desired_capabilities=capabilities)
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
