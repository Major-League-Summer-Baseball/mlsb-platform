from time import strptime
from datetime import date, datetime
from api.helper import normalize_string
from api.variables import BATS, FIELDS

NORMALIZED_FIELDS = [field.lower() for field in FIELDS]


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
    return (
        (value is True or value is False) or
        (string_validator(value) and str(value).lower() in ['true', 'false'])
    )


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
    try:
        # try to convert to int
        int(value)
        return False
    except Exception:
        pass
    try:
        # will be an int if successfully converted other it won't be
        if str(value) != "":
            return True
    except Exception:
        return False
    return False


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
    return int_validator(year) and 2014 <= int(year) <= date.today().year


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
    try:
        return int(value) >= 0
    except Exception:
        return False


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
    try:
        return float(value) >= 0
    except Exception:
        return False


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
    return string_validator(value) and str(value).lower() in "ftm"


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
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        # raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        return False


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
        strptime(value, '%H:%M')
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
    return int_validator(rbi) and int(rbi) <= 4


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
    is_eligible = gender is not None and normalize_string(gender) == "f"
    return (
        string_validator(hit) and normalize_string(str(hit)) in BATS and
        (is_eligible or
            (not is_eligible and normalize_string(str(hit)) != "ss")
        )
    )


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
    return int_validator(inning) and int(inning) > 0


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
    return (
        string_validator(field) and
        str(field).strip().lower() in NORMALIZED_FIELDS
    )
