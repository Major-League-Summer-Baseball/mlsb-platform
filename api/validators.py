'''
Name: Dallas Fraser
Date: 2016-04-12
Project: MLSB API
Purpose: Holds data validators
'''
import unittest
import time
import datetime
from datetime import date
from api.variables import BATS, FIELDS


def boolean_validator(value):
    '''
    boolean_validator
        a general function to validate boolean parameter
        Parameters:
            value: the passed parameter to validate (boolean)
        Returns:
            True if valid
            False otherwise
    '''
    validated = False
    if value is True or value is False:
        validated = True
    return validated


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
    # try to convert to int
    try:
        value = int(value)
    except Exception:
        pass
    try:
        # will be an int if successfully converted other it won't be
        if not isinstance(value, int) and str(value) != "":
            validated = True
    except Exception:
        pass
    return validated


def year_validator(year):
    '''
    year_validator
        a general function to validate the year parameter
        Parameters:
            year: the year to validate (int)
        Returns:
            True if valid
            False otherwise
    '''
    validated = False
    if int_validator(year) and year >= 2014 and year <= date.today().year:
        validated = True
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
    except Exception:
        pass
    return validated


def float_validator(value):
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
        if float(value) >= 0:
            validated = True
    except Exception:
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
    except Exception:
        pass
    return validated


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
        # raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        pass
    return valid


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


def hit_validator(hit, gender=None):
    '''
    hit_validator
        a function that checks if the hit is valid
        Parameters:
            hit: The classification of the hit (str)
            gender: the gende of the batter (str)
        Returns:
            True is valid
            False otherwise
    '''
    valid = False
    if string_validator(hit):
        if hit.lower() in BATS:
            valid = True
            if ((gender is None or
                    gender.lower() != "f") and
                    hit.lower() == "ss"):
                valid = False
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


def field_validator(field):
    '''
    field_validator
        a function that check if the field is valid
        Parameters:
            field: the field (str)
        Returns:
            True if valid
            False otherwise
    '''
    valid = False
    if field in FIELDS:
        valid = True
    return valid
