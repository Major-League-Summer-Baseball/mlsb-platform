'''
@author: Dallas Fraser
@author: 2019-02-04
@organization: MLSB API
@summary: Tests all the validators functions
'''
import unittest
from pprint import PrettyPrinter
from api.validators import gender_validator, boolean_validator,\
                           int_validator, string_validator,\
                           date_validator, time_validator,\
                           rbi_validator, hit_validator,\
                           field_validator

class Test(unittest.TestCase):

    def setUp(self):
        self.pp = PrettyPrinter(indent=4)

    def tearDown(self):
        pass

    def testGenderValidator(self):
        # test with a non-number
        test = 1
        self.assertEqual(gender_validator(test), False,
                         'Gender Validator: 1 was a valid Gender')
        # test empty string
        test = ""
        self.assertEqual(gender_validator(test), False,
                         'Gender Validator: "" was a valid Gender')
        # test with non-valid gender
        test = "X"
        self.assertEqual(gender_validator(test), False,
                         'Gender Validator: X was a valid Gender')
        # test fpr ca[senstivty
        test = "f"
        self.assertEqual(gender_validator(test), True,
                         'Gender Validator: f was a invalid Gender')
        # test fpr ca[senstivty
        test = "M"
        self.assertEqual(gender_validator(test), True,
                         'Gender Validator: M was a invalid Gender')

    def testBooleanValidator(self):
        test = ""
        self.assertEqual(boolean_validator(test), False,
                         'Boolean Validator: "" was a valid boolean')
        test = 1
        self.assertEqual(boolean_validator(test), False,
                         'Boolean Validator: 1 was a valid boolean')
        test = True
        self.assertEqual(boolean_validator(test), True,
                         'Boolean Validator: True was not a valid boolean')
        test = False
        self.assertEqual(boolean_validator(test), True,
                         'Boolean Validator: False was not a valid boolean')

    def testIntValidator(self):
        # test with a string
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
        # test with a number
        test = 1
        self.assertEqual(string_validator(test), False,
                         'String Validator: 1 was a valid string')
        # test with an empty string
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
        # test with a string
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
        test = "ss"
        self.assertEqual(hit_validator(test), False,
                         'Hit Validator:' +
                         'SS was a valid Hit for a non-specified gender')
        test = "ss"
        self.assertEqual(hit_validator(test, gender='f'), True,
                         'Hit Validator:' +
                         'SS was a invalid Hit for a girl')
        test = "ss"
        self.assertEqual(hit_validator(test, gender="m"), False,
                         'Hit Validator: SS was a invalid Hit for a guy')
        test = "hr"
        self.assertEqual(hit_validator(test, gender="m"), True,
                         'Hit Validator: HR was a invalid Hit for a guy')

    def testFieldValidator(self):
        test = 1
        self.assertEqual(field_validator(test), False,
                         'Field Validator: 1 was a valid Field')
        test = "X"
        self.assertEqual(field_validator(test), False,
                         'Field Validator: X was a valid Field')
        test = "WP1"
        self.assertEqual(field_validator(test), True,
                         'Field Validator: WP1 was not a valid Field')


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()