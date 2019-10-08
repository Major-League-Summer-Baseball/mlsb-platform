'''
@author: Dallas Fraser
@author: 2018-11-05
@organization: MLSB
@summary: The behave steps package holds steps for various classes
'''
import datetime


def current_year():
    return str(datetime.datetime.now().year)
