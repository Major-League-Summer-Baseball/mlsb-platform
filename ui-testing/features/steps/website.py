'''
@author: Dallas Fraser
@author: 2018-11-05
@organization: MLSB
@summary: The steps for various website pages
'''
from selenium.webdriver.common.by import By
from environment import BASE_URL
from api.routes import Routes
from behave import given, when, then
from steps import current_year
from steps.utilities import wait_until_loaded


@given('I navigate to the "{page}" page')
def navigate_to_page(context, page):
    route = Routes[page + "page"]
    page_url = BASE_URL + route + "/" + current_year()
    if (page_url != context.browser.current_url):
        context.browser.get(BASE_URL + route + "/" + current_year())
        print("Page has loaded:" + page + "-" + page_url)
    else:
        print("Already Loaded page"+ page + "-" + page_url)
    print(context)


@when('I click on "{tab_name}" tab')
def click_on_tab(context, tab_name):
    tab_name = tab_name.replace('"', '')
    xpath = "//a[contains(text(), '" + tab_name +"')]"
    element = context.browser.find_element_by_xpath(xpath)
    element.click()
    print("Click Event Button: " + tab_name)
    print("Xpath click:" + xpath)


@when('I click on "{event_name}" event button')
def click_on_event_page(context, event_name):
    event_name = event_name.replace('"', '')
    xpath = "//a[contains(text(), '" + event_name +"')]"
    element = context.browser.find_element_by_xpath(xpath)
    element.click()
    print("Click Event Button: " + event_name)
    print("Xpath click:" + xpath)


@then('I see a paragraph containing "{text_sample}"')
@then('I see a event paragraph containing "{text_sample}"')
def assert_sample_text(context, text_sample):
    text_sample = text_sample.replace('"', '')
    xpath = "//p[contains(text(), '" + text_sample + "')]"
    context.browser.find_element_by_xpath(xpath)


