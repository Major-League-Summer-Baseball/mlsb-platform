'''
@author: Dallas Fraser
@date: 2016-04-12
@organization: MLSB API
@summary: Tests all the imports classes
'''
from api.model import Team, Game, Player
from api import DB
from api.BaseTest import TestSetup
from api.advanced.import_league import LeagueList
from api.advanced.import_team import TeamList
from api.errors import InvalidField, SponsorDoesNotExist, LeagueDoesNotExist
import unittest
import logging
import datetime


class MockSession():
    def __init__(self, tester):
        self.tester = tester

    def add(self, obj):
        if (type(obj) == Game):
            self.tester.games_to_delete.append(obj)
        elif (type(obj) == Player):
            self.tester.players_to_delete.append(obj)
        elif (type(obj) == Team):
            self.tester.teams_to_delete.append(obj)
        DB.session.add(obj)

    def commit(self):
        DB.session.commit()


class TestImportTeam(TestSetup):
    def testColumnsIndives(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(message)s')
        logger = logging.getLogger(__name__)
        importer = TeamList([], logger=logger, session=MockSession(self))
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
        # add a league and a sponsor
        color = "Pink"
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(message)s')
        logger = logging.getLogger(__name__)
        lines = ["Sponsor:,{},".format("Test Import Sponsor"),
                 "Color:,{},".format(color),
                 "Captain:,Test Captain,",
                 "League:,{},".format("Test Import League"),
                 "Player Name,Player Email,Gender (M/F)"
                 "Laura Visentin,vise3090@mylaurier.ca,F",
                 "Test Captain,testcaptainimport@mlsb.ca,M",
                 "Test Girl,testgirlimport@mlsb.ca,F",
                 "Test Boy,testboyimport@mlsb.ca,M"]
        importer = TeamList(lines, logger=logger, session=MockSession(self))

        # test a invalid sponsor
        try:
            importer.import_headers()
            self.assertEqual(True, False, "Sponsor does not exist")
        except SponsorDoesNotExist as __:
            pass

        # add the sponsor
        self.add_sponsor("Test Import Sponsor")
        importer = TeamList(lines, logger=logger, session=MockSession(self))

        # test a invalid league
        try:
            importer.import_headers()
            self.assertEqual(True, False, "League does not exist")
        except LeagueDoesNotExist as __:
            pass

        # add the league
        self.add_league("Test Import League")
        importer.import_headers()
        self.assertEqual(importer.captain_name,
                         "Test Captain",
                         "Captain name not set")
        self.assertNotEqual(importer.team, None, "Team no set properly")

    def testImportPlayers(self):
        # add a league and a sponsor
        sponsor = self.add_sponsor("Test Import Sponsor")
        league = self.add_league("Test Import League")
        color = "Pink"
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(message)s')
        logger = logging.getLogger(__name__)
        lines = ["Sponsor:,{},".format(sponsor['sponsor_name']),
                 "Color:,{},".format(color),
                 "Captain:,Test Captain,",
                 "League:,{},".format(league['league_name']),
                 "Player Name,Player Email,Gender (M/F)"
                 "Laura Visentin,vise3090@mylaurier.ca,F",
                 "Test Captain,testcaptainimport@mlsb.ca,M",
                 "Test Girl,testgirlimport@mlsb.ca,F",
                 "Test Boy,testboyimport@mlsb.ca,M"]
        importer = TeamList(lines, logger=logger, session=MockSession(self))

        # mock the first half
        team_id = self.add_team(color, sponsor, league)['team_id']
        team = DB.session.query(Team).get(team_id)
        importer.team = team
        importer.captain_name = "Test Captain"
        importer.email_index = 1
        importer.name_index = 0
        importer.gender_index = 2

        # if no errors are raised then golden
        importer.import_players(5)

    def testAddTeam(self):
        # add a league and a sponsor
        sponsor = self.add_sponsor("Test Import Sponsor")
        league = self.add_league("Test Import League")
        color = "Pink"

        # set the logger
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(message)s')
        logger = logging.getLogger(__name__)
        lines = ["Sponsor:,{},".format(sponsor['sponsor_name']),
                 "Color:,{},".format(color),
                 "Captain:,Test Captain,",
                 "League:,{},".format(league['league_name']),
                 "Player Name,Player Email,Gender (M/F)"
                 "Laura Visentin,vise3090@mylaurier.ca,F",
                 "Test Captain,testcaptainimport@mlsb.ca,M",
                 "Test Girl,testgirlimport@mlsb.ca,F",
                 "Test Boy,testboyimport@mlsb.ca,M"]
        importer = TeamList(lines, logger=logger, session=MockSession(self))

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
        self.tl = LeagueList(TestImportGames.TEST, session=MockSession(self))
        l, h = self.tl.parse_header(TestImportGames.TEST[0: 2])
        self.assertEqual(l, 'Monday and Wednesday')
        self.assertEqual(h,
                         ["Home Team", "Away Team", "Date", "Time", "Field"])

    def testCheckHeader(self):
        # check valid header
        self.tl = LeagueList(TestImportGames.TEST,
                             session=MockSession(self))
        valid = self.tl.check_header(TestImportGames.TEST[0:2])
        self.assertEqual(valid, True)
        # check a header that is too short
        self.tl = LeagueList(TestImportGames.TOO_SHORT,
                             session=MockSession(self))
        valid = self.tl.check_header(TestImportGames.TOO_SHORT[0:2])
        self.assertEqual(valid, False)
        # check a header that has too few columns
        self.tl = LeagueList(TestImportGames.TOO_FEW_COLUMNS,
                             session=MockSession(self))
        valid = self.tl.check_header(TestImportGames.TOO_FEW_COLUMNS[0:2])
        self.assertEqual(valid, False)
        # check a header that is missing a column
        self.tl = LeagueList(TestImportGames.MISSING_HOME_NAME,
                             session=MockSession(self))
        valid = self.tl.check_header(TestImportGames.TOO_FEW_COLUMNS[0:2])
        self.assertEqual(valid, False)

    def testGetLeagueID(self):
        league_name = "Test Import Fake League"
        league = self.add_league(league_name)
        self.tl = LeagueList(TestImportGames.TEST,
                             session=MockSession(self))
        league_id = self.tl.get_league_id(league_name)
        self.assertEqual(league['league_id'], league_id)
        self.tl = LeagueList(TestImportGames.TEST,
                             session=MockSession(self))
        try:
            self.tl.get_league_id("No League")
            self.assertEqual(True, False,
                             "League does not exist error should be raised")
        except Exception:
            pass

    def testImportGame(self):
        # add a league, sponsor and two teams
        league_name = "Test Import Fake League"
        league = self.add_league(league_name)
        sponsor = self.add_sponsor("Import Test Sponsor")
        t1 = self.add_team("Green", sponsor, league)
        t2 = self.add_team("Black", sponsor, league)

        # a valid request to add a game
        day = datetime.date.today().strftime("%Y-%m-%d")
        game_entry = "{},{},{},12:00,WP1".format(t1['team_name'],
                                                 t2['team_name'],
                                                 day)
        self.valid_test = ["League:,{},,,".format(league_name),
                           "Home Team,Away Team,Date,Time,Field",
                           game_entry]
        self.tl = LeagueList(self.valid_test,
                             session=MockSession(self))
        self.tl.league_id = league['league_id']
        self.tl.set_columns_indices(self.valid_test[1].split(","))
        self.tl.set_teams()
        self.tl.import_game(self.valid_test[2])
        self.assertEqual(self.tl.warnings, [])
        self.assertEqual(self.tl.errors, [])

        # an invalid request - one team not in the league
        game_entry = "{},{},{},12:00,WP1".format("NOT A TEAM",
                                                 t2['team_name'],
                                                 day)
        self.valid_test = ["League:,{},,,".format(league_name),
                           "Home Team,Away Team,Date,Time,Field",
                           game_entry]
        self.tl = LeagueList(self.valid_test,
                             session=MockSession(self))
        self.tl.league_id = league['league_id']
        self.tl.set_columns_indices(self.valid_test[1].split(","))
        self.tl.set_teams()
        self.tl.import_game(self.valid_test[2])
        self.assertEqual(self.tl.warnings, [])
        self.assertEqual(self.tl.errors,
                         ["NOT A TEAM is not a team in the league"])

    def testValidCases(self):
        # add a league, sponsor and two teams
        league_name = "Test Import Fake League"
        league = self.add_league(league_name)
        sponsor = self.add_sponsor("Import Test Sponsor")
        t1 = self.add_team("Green", sponsor, league)
        t2 = self.add_team("Black", sponsor, league)

        # import  a set of good games
        day = datetime.date.today().strftime("%Y-%m-%d")
        game_entry = "{},{},{},12:00,WP1".format(t1['team_name'],
                                                 t2['team_name'],
                                                 day)
        self.valid_test = ["League:,{},,,".format(league_name),
                           "Home Team,Away Team,Date,Time,Field",
                           game_entry]
        self.tl = LeagueList(self.valid_test,
                             session=MockSession(self))
        self.tl.import_league()
        self.assertEqual([], self.tl.warnings)
        self.assertEqual([], self.tl.errors)

    def testInvalidCases(self):
        # add a league, sponsor and two teams
        league_name = "Test Import Fake League"
        league = self.add_league(league_name)
        sponsor = self.add_sponsor("Import Test Sponsor")
        t1 = self.add_team("Green", sponsor, league)
        t2 = self.add_team("Black", sponsor, league)

        # test bad header
        # import  a set of good games
        day = datetime.date.today().strftime("%Y-%m-%d")
        game_entry = "{},{},{},12:00,WP1".format(t1['team_name'],
                                                 t2['team_name'],
                                                 day)

        self.bad_header = ["League:,{},,,".format(league_name),
                           "Home Team,Away Team,Date,Time,asjdl9798u",
                           game_entry]
        self.tl = LeagueList(self.bad_header)
        self.tl.import_league()

        # test bad league
        self.bad_league = ["Leaguex:,{}xas,,,".format(league_name),
                           "Home Team,Away Team,Date,Time,Field",
                           game_entry]
        self.tl = LeagueList(self.bad_league,
                             session=MockSession(self))
        try:
            self.tl.import_league()
        except LeagueDoesNotExist:
            pass

        # test bad game
        game_entry = "{},{},2015-XX-01,12:00,WP1".format(t1['team_name'],
                                                         t2['team_name'])
        self.bad_game = ["League:,{},,,".format(league_name),
                         "Home Team,Away Team,Date,Time,Field",
                         game_entry]
        self.tl = LeagueList(self.bad_game,
                             session=MockSession(self))
        try:
            self.tl.import_league()
            self.assertEqual(True, False, "should raise error")
        except InvalidField:
            pass

        # test bad team in game
        bad_team = "xaasdasd3"
        game_entry = "{},{},{},12:00,WP1".format(bad_team,
                                                 t2['team_name'],
                                                 day)
        self.bad_team = ["League:,{},,,".format(league_name),
                         "Home Team,Away Team,Date,Time,Field",
                         game_entry]

        self.tl = LeagueList(self.bad_team,
                             session=MockSession(self))
        self.tl.import_league()
        self.assertEqual(self.tl.warnings, [])
        self.assertEqual(['{} is not a team in the league'.format(bad_team)],
                         self.tl.errors)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
