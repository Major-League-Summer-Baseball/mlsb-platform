'''
Name: Dallas Fraser
Date: 2014-08-23
Project: MLSB API
Purpose: Some random helper functions
'''
import unittest
from json import loads as loader
def loads(data):
    try:
        data = loader(data)
    except:
        data = loader(data.decode('utf-8'))
    return data


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testLoads(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testLoads']
    unittest.main()