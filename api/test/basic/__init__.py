from unittest import TestLoader, TextTestRunner
from api.test.basic import testBasicBat
from api.test.basic import testBasicEspsy
from api.test.basic import testBasicFun
from api.test.basic import testBasicGame
from api.test.basic import testBasicLeague
from api.test.basic import testBasicPlayer
from api.test.basic import testBasicSponsor
from api.test.basic import testBasicTeam


if __name__ == "__main__":
    # run all the test suites
    TextTestRunner().run(TestLoader().loadTestsFromModule(testBasicBat))
    TextTestRunner().run(TestLoader().loadTestsFromModule(testBasicEspsy))
    TextTestRunner().run(TestLoader().loadTestsFromModule(testBasicFun))
    TextTestRunner().run(TestLoader().loadTestsFromModule(testBasicGame))
    TextTestRunner().run(TestLoader().loadTestsFromModule(testBasicLeague))
    TextTestRunner().run(TestLoader().loadTestsFromModule(testBasicPlayer))
    TextTestRunner().run(TestLoader().loadTestsFromModule(testBasicSponsor))
    TextTestRunner().run(TestLoader().loadTestsFromModule(testBasicTeam))
