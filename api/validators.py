'''
Name: Dallas Fraser
Date: 2014-07-31
Project: MLSB API
Purpose: Holds data validators
'''
import unittest
import os
HITS = ['S', 'D', 'SS', 'HR', 'K', 'E','FC', 'FO','GO']
def string_validator(value):
    '''
    string_validator
        a general function to validate string parameter
        Parameters:
            value: the passed parameter to validate (str)
        Returns:
            True if valid 
            False otherwise
    '''
    validated = False
    #try to convert to int
    try:
        value = int(value)
    except:
        pass
    try:
        #will be an int if successfully converted other it won't be
        if not isinstance(value, int) and str(value) != "":
            validated = True
    except:
        pass
    return validated

def int_validator(value):
    '''
    int_validator
        a general function to validate integer parameter
        Parameters:
            value: the passed parameter to validate (int)
        Returns:
            True if valid 
            False otherwise
    '''
    validated = False
    try:
        if int(value) >= 0:
            validated = True
    except:
        pass
    return validated

def gender_validator(value):
    '''
    gender_validator
        a function to validate gender parameter
        Parameters:
            value: the passed parameter to validate (str)
        Returns:
            True if valid 
            False otherwise
    '''
    validated = False
    try:
        if str(value) != "" and (value.upper() in "FTM"):
            validated = True
    except:
        pass
    return validated


import datetime
def date_validator(date):
    '''
    date_validator
        a function that validates if date is in proper format (YYYY-MM-DD)
        Parameters:
            date: The date to validate (string)
        Returns:
            True if valid
            False otherwise
    '''
    valid = False
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        valid = True
    except ValueError:
        #raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        pass
    return valid

import time
def time_validator(value):
    '''
    time_validator
        a function that validates if time is in proper format
        Parameters:
            value: The time to validate (string)
        Returns:
            True if valid
            False otherwise
    '''
    try:
        time.strptime(value, '%H:%M')
        return True
    except ValueError:
        return False


def rbi_validator(rbi):
    '''
    rbi_validator
        a function that validates if rbi is valid
        Parameters:
            rbi: the number of runs batted in (int)
        Returns:
            True if valid
            False otherwise
    '''
    valid = False
    if int_validator(rbi):
        if rbi <= 4:
            valid = True
    return valid

def hit_validator(hit):
    '''
    hit_validator
        a function that checks if the hit is valid
        Parameters:
            hit: The classification of the hit
        Returns:
            True is valid
            False otherwise
    '''
    valid = False
    if string_validator(hit):
        if hit in HITS:
            valid = True
    return valid

def inning_validator(inning):
    '''
    inning_validator
        a function that check if the inning is valid
        Parameters:
            inning: the inning (int)
        Returns:
            True if valid
            False otherwise
    '''
    valid = False
    if inning > 0:
        valid = True
    return valid

def validated(x):
    '''
    validated
        a function that awlays returns True
        Parameters:
            x
        Returns:
            True
    '''
    return True

from pprint import PrettyPrinter
class Test(unittest.TestCase):

    def setUp(self):
        self.pp = PrettyPrinter(indent=4)

    def tearDown(self):
        pass

    def testGenderValidator(self):
        #test with a non-number
        test = 1
        self.assertEqual(gender_validator(test), False,
                         'Gender Validator: 1 was a valid Gender')
        #test empty string
        test = ""
        self.assertEqual(gender_validator(test), False,
                         'Gender Validator: "" was a valid Gender')
        #test with non-valid gender
        test = "X"
        self.assertEqual(gender_validator(test), False,
                         'Gender Validator: X was a valid Gender')
        #test fpr ca[senstivty
        test = "f"
        self.assertEqual(gender_validator(test), True,
                         'Gender Validator: f was a invalid Gender')
        #test fpr ca[senstivty
        test = "M"
        self.assertEqual(gender_validator(test), True,
                         'Gender Validator: M was a invalid Gender')

    def testIntValidator(self):
        #test with a string
        test = ""
        self.assertEqual(int_validator(test), False,
                         'Int Validator: "" was a valid int')
        test = "Bob Saget"
        self.assertEqual(int_validator(test), False,
                         'Int Validator: "Bob Saget" was a valid int')
        test = -1
        self.assertEqual(int_validator(test), False,
                         'Int Validator: -1 was a valid int')
        test = 1
        self.assertEqual(int_validator(test), True,
                         'Int Validator: 1 was a invalid int')

    def testStringValidator(self):
        #test with a number
        test = 1
        self.assertEqual(string_validator(test), False,
                         'String Validator: 1 was a valid string')
        #test with an empty string
        test = ""
        self.assertEqual(string_validator(test), False,
                         'String Validator: "" was a valid string')
        test = "Bob Saget"
        self.assertEqual(string_validator(test), True,
                         'String Validator: Bob Saget was a invalid string')

    def testDateValidator(self):
        self.assertEqual(False, date_validator('01-01-2014'),
                         "Date Validator: Invalid Date")
        self.assertEqual(False, date_validator('2014-01-2014'),
                         "Date Validator: Invalid Date")
        self.assertEqual(False, date_validator('2014-13-01'),
                         "Date Validator: Invalid Date")
        self.assertEqual(True, date_validator('2014-12-01'),
                         "Date Validator: Valid Date")

    def testTimeValidator(self):
        self.assertEqual(False, time_validator('25:01'),
                         "Time Validator: Invalid Time")
        self.assertEqual(False, time_validator('24:61'),
                         "Time Validator: Invalid Time")
        self.assertEqual(True, time_validator('23:01'),
                         "Time Validator: Valid Time")

    def testRbiValidator(self):
        #test with a string
        test = ""
        self.assertEqual(rbi_validator(test), False,
                         'rbi Validator: "" was a valid rbi')
        test = "Bob Saget"
        self.assertEqual(rbi_validator(test), False,
                         'rbi Validator: "Bob Saget" was a valid rbi')
        test = -1
        self.assertEqual(rbi_validator(test), False,
                         'rbi Validator: -1 was a valid rbi')
        test = 5
        self.assertEqual(rbi_validator(test), False,
                         'rbi Validator: 5 was a valid rbi')
        test = 1
        self.assertEqual(rbi_validator(test), True,
                         'rbi Validator: 1 was a invalid rbi')

    def testHitValidator(self):
        test = 1
        self.assertEqual(hit_validator(test), False,
                         'Hit Validator: 1 was a valid Hit')
        test = "X"
        self.assertEqual(hit_validator(test), False,
                         'Hit Validator: X was a valid Hit')
        test = "S"
        self.assertEqual(hit_validator(test), True,
                         'Hit Validator: S was a invalid Hit')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()