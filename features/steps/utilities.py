'''
@author: Dallas Fraser
@author: 2018-11-05
@organization: MLSB
@summary: Common utilities for various steps
'''
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from environment import DELAY
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def wait_until_loaded(browser, element, delay=DELAY):
    try:
        (WebDriverWait(browser, delay)
            .until(EC.presence_of_element_located(element)))
    except TimeoutException:
        print("Timeout Exception has been raised")
        raise TimeoutException()
