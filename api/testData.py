'''
Created on Sep 22, 2015

@author: Dallas
'''
from api import DB
from api.model import Sponsor


DB.session.add(Sponsor("Domus"))
DB.session.add(Sponsor("SBE"))
DB.session.add(Sponsor("GE"))
DB.session.add(Sponsor("Wilfs"))
DB.session.add(Sponsor("Nightschool"))
DB.session.commit()
