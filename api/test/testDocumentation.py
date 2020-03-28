'''
@author: Dallas Fraser
@author: 2019-03-13
@organization: MLSB API
@summary: Tests all the advanced fun APIs
'''
from api.routes import Routes
from api.test.BaseTest import TestSetup, SUCCESSFUL_GET_CODE
START_OF_PLATFORM = 2016
YEAR_WITH_NO_DATA = 1992


class TestDocumentation(TestSetup):

    def testStaticDocumetnationFiles(self):
        documentation_routes = ['dindex',
                                'dresponse',
                                'doplayer',
                                'dobat',
                                'dogame',
                                'dosponsor',
                                'doteam',
                                'doteamroster',
                                'doleague',
                                'dofun',
                                'dopagination',
                                'dbplayer',
                                'dbbat',
                                'dbgame',
                                'dbsponsor',
                                'dbteam',
                                'dbteamroster',
                                'dbleague',
                                'dbfun',
                                'dvgame',
                                'dvplayer',
                                'dvteam',
                                'dvfun',
                                'dvplayerLookup',
                                'dvplayerteamLookup',
                                'dvleagueleaders',
                                'dvschedule',
                                'dbotsubmitscore',
                                'dbotcaptain',
                                'dbotupcominggames',
                                'dbottransaction',
                                'dbotcaptaingames',
                                'dbottransaction']
        for route in documentation_routes:
            with self.app.get(Routes[route]) as result:
                error_message = ("Unable to get documentation for {} at {}"
                                 .format(route, Routes[route]))
                self.assertEqual(SUCCESSFUL_GET_CODE,
                                 result.status_code,
                                 error_message)
