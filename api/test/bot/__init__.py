'''
@author: Dallas Fraser
@date: 2016-04-12
@organization: MLSB API
@summary: Test suite that runs all the advanced APIs
'''
from unittest import TestLoader, TextTestRunner
from api.test.bot import testBotAuthenticateCaptain
from api.test.bot import testBotCaptainGames
from api.test.bot import testBotSubmitScores
from api.test.bot import testBotUpcomingGames

if __name__ == "__main__":
    # run all the test suites
    (TextTestRunner().run(TestLoader()
                          .loadTestsFromModule(testBotAuthenticateCaptain)))
    (TextTestRunner().run(TestLoader()
                          .loadTestsFromModule(testBotCaptainGames)))
    (TextTestRunner().run(TestLoader()
                          .loadTestsFromModule(testBotSubmitScores)))
    (TextTestRunner().run(TestLoader()
                          .loadTestsFromModule(testBotUpcomingGames)))
