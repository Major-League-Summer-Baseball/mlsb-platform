'''
@author: Dallas Fraser
@date: 2019-03-13
@organization: MLSB API
@summary: Test suite that runs all the advanced APIs
'''
import datetime
from unittest import TestLoader, TextTestRunner
from api.test.advanced import testAdvancedFun
from api.test.advanced import testAdvancedGame
from api.test.advanced import testAdvancedLeagueLeaders
from api.test.advanced import testAdvancedPlayer
from api.test.advanced import testAdvancedPlayerLookup
from api.test.advanced import testAdvancedPlayerTeamLookup
from api.test.advanced import testAdvancedSchedule
from api.test.advanced import testAdvancedTeam
from api.test.advanced import testAdvancedTeamRoster


if __name__ == "__main__":
    # run all the test suites
    TextTestRunner().run(TestLoader().loadTestsFromModule(testAdvancedFun))
    TextTestRunner().run(TestLoader().loadTestsFromModule(testAdvancedGame))
    (TextTestRunner().run(TestLoader()
                          .loadTestsFromModule(testAdvancedLeagueLeaders)))
    TextTestRunner().run(TestLoader().loadTestsFromModule(testAdvancedPlayer))
    (TextTestRunner().run(TestLoader()
                          .loadTestsFromModule(testAdvancedPlayerLookup)))
    (TextTestRunner().run(TestLoader()
                          .loadTestsFromModule(testAdvancedPlayerTeamLookup)))
    (TextTestRunner().run(TestLoader()
                          .loadTestsFromModule(testAdvancedSchedule)))
    TextTestRunner().run(TestLoader().loadTestsFromModule(testAdvancedTeam))
    (TextTestRunner().run(TestLoader()
                          .loadTestsFromModule(testAdvancedTeamRoster)))