'''
Created on Sep 19, 2018

@author: dfraser
'''
import unittest

class TestImportTeam(TestSetup):
    def testColumnsIndives(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(message)s')
        logger = logging.getLogger(__name__)
        importer = TeamList([], logger=logger)
        try:
            importer.set_columns_indices("asd,asd,asd".split(","))
            self.assertEqual(True, False,
                             "Should have raised invalid field error")
        except InvalidField as __:
            pass
        # if it runs then should be good
        importer.set_columns_indices("Player Name,Player Email,Gender (M/F)"
                                     .split(","))
        self.assertEqual(importer.name_index, 0,
                         "Name index not set properly")
        self.assertEqual(importer.email_index, 1,
                         "Email index not set properly")
        self.assertEqual(importer.gender_index, 2,
                         "Gender index not set properly")

    def testImportHeaders(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(message)s')
        logger = logging.getLogger(__name__)
        lines = ["Sponsor:,Domus,",
                 "Color:,Pink,",
                 "Captain:,Dallas Fraser,",
                 "League:,Monday & Wedneday,",
                 "Player Name,Player Email,Gender (M/F)"]
        importer = TeamList(lines, logger=logger)
        # test a invalid sponsor
        try:
            importer.import_headers()
            self.assertEqual(True, False, "Sponsor does not exist")
        except SponsorDoesNotExist as __:
            pass
        self.addSponsors()
        importer = TeamList(lines, logger=logger)
        # test a invalid league
        try:
            importer.import_headers()
            self.assertEqual(True, False, "League does not exist")
        except LeagueDoesNotExist as __:
            pass
        self.addLeagues()
        importer.import_headers()
        self.assertEqual(importer.captain_name,
                         "Dallas Fraser",
                         "Captain name not set")
        self.assertNotEqual(importer.team, None, "Team no set properly")

    def testImportPlayers(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(message)s')
        logger = logging.getLogger(__name__)
        lines = ["Sponsor:,Domus,",
                 "Color:,Pink,",
                 "Captain:,Dallas Fraser,",
                 "League:,Monday & Wedneday,",
                 "Player Name,Player Email,Gender (M/F)"
                 "Laura Visentin,vise3090@mylaurier.ca,F",
                 "Dallas Fraser,fras2560@mylaurier.ca,M",
                 "Mitchell Ellul,ellu6790@mylaurier.ca,M",
                 "Mitchell Ortofsky,orto2010@mylaurier.ca,M",
                 "Adam Shaver,shav3740@mylaurier.ca,M",
                 "Taylor Takamatsu,taka9680@mylaurier.ca,F",
                 "Jordan Cross,cros7940@mylaurier.ca,M",
                 "Erin Niepage,niep3130@mylaurier.ca,F",
                 "Alex Diakun,diak1670@mylaurier.ca,M",
                 "Kevin Holmes,holm4430@mylaurier.ca,M",
                 "Kevin McGaire,kevinmcgaire@gmail.com,M",
                 "Kyle Morrison,morr1090@mylaurier.ca,M",
                 "Ryan Lackey,lack8060@mylaurier.ca,M",
                 "Rory Landy,land4610@mylaurier.ca,M",
                 "Claudia Vanderholst,vand6580@mylaurier.ca,F",
                 "Luke MacKenzie,mack7980@mylaurier.ca,M",
                 "Jaron Wu,wuxx9824@mylaurier.ca,M",
                 "Tea Galli,gall2590@mylaurier.ca,F",
                 "Cara Hueston ,hues8510@mylaurier.ca,F",
                 "Derek Schoenmakers,scho8430@mylaurier.ca,M",
                 "Marni Shankman,shan3500@mylaurier.ca,F",
                 "Christie MacLeod ,macl5230@mylaurier.ca,F"
                 ]
        importer = TeamList(lines, logger=logger)
        # mock the first half
        self.addTeams()
        importer.team = self.teams[0]
        importer.captain_name = "Dakkas Fraser"
        importer.email_index = 1
        importer.name_index = 0
        importer.gender_index = 2
        # if no errors are raised then golden
        importer.import_players(5)

    def testAddTeam(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(message)s')
        logger = logging.getLogger(__name__)
        lines = ["Sponsor:,Domus,",
                 "Color:,Pink,",
                 "Captain:,Dallas Fraser,",
                 "League:,Monday & Wedneday,",
                 "Player Name,Player Email,Gender (M/F)"
                 "Laura Visentin,vise3090@mylaurier.ca,F",
                 "Dallas Fraser,fras2560@mylaurier.ca,M",
                 "Mitchell Ellul,ellu6790@mylaurier.ca,M",
                 "Mitchell Ortofsky,orto2010@mylaurier.ca,M",
                 "Adam Shaver,shav3740@mylaurier.ca,M",
                 "Taylor Takamatsu,taka9680@mylaurier.ca,F",
                 "Jordan Cross,cros7940@mylaurier.ca,M",
                 "Erin Niepage,niep3130@mylaurier.ca,F",
                 "Alex Diakun,diak1670@mylaurier.ca,M",
                 "Kevin Holmes,holm4430@mylaurier.ca,M",
                 "Kevin McGaire,kevinmcgaire@gmail.com,M",
                 "Kyle Morrison,morr1090@mylaurier.ca,M",
                 "Ryan Lackey,lack8060@mylaurier.ca,M",
                 "Rory Landy,land4610@mylaurier.ca,M",
                 "Claudia Vanderholst,vand6580@mylaurier.ca,F",
                 "Luke MacKenzie,mack7980@mylaurier.ca,M",
                 "Jaron Wu,wuxx9824@mylaurier.ca,M",
                 "Tea Galli,gall2590@mylaurier.ca,F",
                 "Cara Hueston ,hues8510@mylaurier.ca,F",
                 "Derek Schoenmakers,scho8430@mylaurier.ca,M",
                 "Marni Shankman,shan3500@mylaurier.ca,F",
                 "Christie MacLeod ,macl5230@mylaurier.ca,F"
                 ]
        importer = TeamList(lines, logger=logger)
        self.addLeagues()
        self.addSponsors()
        # no point checking for errors that were tested above
        importer.add_team()
        self.assertEqual(importer.warnings, ['Team was created'],
                         "Should be no warnings")


class TestImportGames(TestSetup):
    TEST = [
                 "League:,Monday and Wednesday,,,",
                 "Home Team,Away Team,Date,Time,Field",
                 "Domus Green,Chainsaw Black,2015-10-01", "12:00", "WP1"]
    TOO_SHORT = ["Home Team,Away Team,Date,Time,Field"]
    TOO_FEW_COLUMNS = ["League:,Monday and Wednesday,,,",
                       "Home Team,Away Team,Date,Time",
                       "Domus Green,Chainsaw Black,2015-10-01", "12:00", "WP1"
                       ]
    MISSING_HOME_NAME = [
                         "League:,Monday and Wednesday,,,",
                         ",Away Team,Date,Time",
                         "Domus Green,Chainsaw Black,2015-10-01",
                         "12:00",
                         "WP1"
                            ]

    def testParseHeader(self):
        self.tl = LeagueList(TestImportGames.TEST)
        l, h = self.tl.parse_header(TestImportGames.TEST[0: 2])
        self.assertEqual(l, 'Monday and Wednesday')
        self.assertEqual(h,
                         ["Home Team", "Away Team", "Date", "Time", "Field"])

    def testCheckHeader(self):
        # check valid header
        self.tl = LeagueList(TestImportGames.TEST)
        valid = self.tl.check_header(TestImportGames.TEST[0:2])
        self.assertEqual(valid, True)
        # check a header that is too short
        self.tl = LeagueList(TestImportGames.TOO_SHORT)
        valid = self.tl.check_header(TestImportGames.TOO_SHORT[0:2])
        self.assertEqual(valid, False)
        # check a header that has too few columns
        self.tl = LeagueList(TestImportGames.TOO_FEW_COLUMNS)
        valid = self.tl.check_header(TestImportGames.TOO_FEW_COLUMNS[0:2])
        self.assertEqual(valid, False)
        # check a header that is missing a column
        self.tl = LeagueList(TestImportGames.MISSING_HOME_NAME)
        valid = self.tl.check_header(TestImportGames.TOO_FEW_COLUMNS[0:2])
        self.assertEqual(valid, False)

    def testGetLeagueID(self):
        self.addLeagues()
        self.tl = LeagueList(TestImportGames.TEST)
        team = self.tl.get_league_id("Monday & Wedneday")
        self.assertEqual(team, 1)
        self.tl = LeagueList(TestImportGames.TEST)
        try:
            team = self.tl.get_league_id("No League")
            self.assertEqual(True, False,
                             "League does not exist error should be raised")
        except Exception:
            pass

    def testImportGame(self):
        self.addTeamWithLegaue()
        # add games to the league
        self.valid_test = [
                           "League:,Monday & Wednesday,,,",
                           "Home Team,Away Team,Date,Time,Field",
                           "Domus Green,Chainsaw Black,2015-10-01,12:00,WP1"]
        self.tl = LeagueList(self.valid_test)
        self.tl.league_id = 1
        self.tl.set_columns_indices(self.valid_test[1].split(","))
        self.tl.set_teams()
        self.tl.import_game(self.valid_test[2])
        self.assertEqual(self.tl.warnings, [])
        self.assertEqual(self.tl.errors, [])
        # not a team in the league
        self.valid_test = [
                           "League:,Monday and Wednesday,,,",
                           "Home Team,Away Team,Date,Time,Field",
                           "Domus Black,Chainsaw Black,2015-10-01,12:00, WP1"]
        self.tl = LeagueList(self.valid_test)
        self.tl.league_id = 1
        self.tl.set_columns_indices(self.valid_test[1].split(","))
        self.tl.set_teams()
        self.tl.import_game(self.valid_test[2])
        self.assertEqual(self.tl.warnings, [])
        self.assertEqual(self.tl.errors,
                         ["Domus Black is not a team in the league"])

    def testValidCases(self):
        self.addTeamWithLegaue()
        # import  a set of good games
        self.valid_test = [
                           "League:,Monday & Wedneday,,,",
                           "Home Team,Away Team,Date,Time,Field",
                           "Domus Green,Chainsaw Black,2015-10-01,12:00,WP1"]
        self.tl = LeagueList(self.valid_test)
        self.tl.import_league()
        self.assertEqual([], self.tl.warnings)
        self.assertEqual([], self.tl.errors)

    def testInvalidCases(self):
        self.addTeamWithLegaue()
        # test bad header
        self.bad_header = [
                           "League:,Monday & Wedneday,,,",
                           "Home Team,Away Team,Date,Time,sdjfkhskdj",
                           "Domus Green,Chainsaw Black,2015-10-01,12:00,WP1"]
        self.tl = LeagueList(self.bad_header)
        self.tl.import_league()
        # test bad league
        self.bad_league = [
                           "Leaguex:,Monday & Wedneday,,,",
                           "Home Team,Away Team,Date,Time,Field",
                           "Domus Green,Chainsaw Black,2015-10-01,12:00,WP1"]
        self.tl = LeagueList(self.bad_league)
        try:
            self.tl.import_league()
        except LeagueDoesNotExist:
            pass
        # test bad game
        self.bad_game = [
                           "League:,Monday & Wedneday,,,",
                           "Home Team,Away Team,Date,Time,Field",
                           "Domus Green,Chainsaw Black,2015-xx-01,12:00,WP1"]
        self.tl = LeagueList(self.bad_game)
        try:
            self.tl.import_league()
            self.assertEqual(True, False, "should raise error")
        except InvalidField:
            pass
        self.bad_team = [
                           "League:,Monday & Wedneday,,,",
                           "Home Team,Away Team,Date,Time,Field",
                           "X Green,Chainsaw Black,2015-10-01,12:00,WP1"]
        # test bad team in game
        self.tl = LeagueList(self.bad_team)
        self.tl.import_league()
        self.assertEqual(self.tl.warnings, [])
        self.assertEqual(['X Green is not a team in the league'],
                         self.tl.errors)


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()