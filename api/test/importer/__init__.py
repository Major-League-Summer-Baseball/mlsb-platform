from unittest import TestLoader, TextTestRunner
from api.test.importer import testAdvancedImportLeague
from api.test.importer import testAdvancedImportTeam

if __name__ == "__main__":
    # run all the test suites
    (TextTestRunner().run(TestLoader()
                          .loadTestsFromModule(testAdvancedImportLeague)))
    (TextTestRunner().run(TestLoader()
                          .loadTestsFromModule(testAdvancedImportTeam)))
