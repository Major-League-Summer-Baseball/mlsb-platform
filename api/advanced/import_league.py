'''
Name: Dallas Fraser
Date: 2015-11-08
Project: MLSB API
Purpose: Holds a class TeamList that helps imports a team roster
'''
# imports
from sqlalchemy.sql.expression import and_
from api.model import Sponsor, Team, Player, Game, League
from api import DB
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from api.validators import time_validator, string_validator, date_validator
from datetime import datetime
from api.advanced.import_team import INVALID_FIELD
# constants
CREATED = "Created Team (no league was specified"
NO_LEAGUE = "Cannot find league, please ensure spelt correctly or create the league"
INVALID_FILE = "File was not given in right format (use template)"
EXAMPLE_FOUND = "First entry contain the templates example, just skipped it"
EMAIL_NAME = "Player {} email was found but had different name"
INVALID_FIELD = "{} had an invalid field"
INVALID_TEAM = "{} is not a team in the league"

class LeagueList():
    def __init__(self, lines):
        self.success = False
        self.errors = []
        self.warnings = []
        self.lines = lines

    def import_league(self):
        '''
        a method that imports a bunch of games for a league
        based on a csv template
        Parameters:
            
        Updates:
            success: a boolean if the import was successful (boolean)
            errors: a list of possible error (list)
            warnings: a list of possible warnings (list)
        '''
        if self.lines is not None:
            if self.check_header(self.lines[0:2]):
                league, headers = self.parse_header(self.lines[0:2])
                print("Getting League ID")
                self.league_id = self.get_league_id(league)
                print("Got League id", self.league_id)
                self.set_columns_indices(headers)
                print("Got set column indcides")
                if self.league_id is not None:
                    self.set_teams()
                    games = self.lines[2:]
                    for game in games:
                        print(game)
                        self.import_game(game)
                        print("Done Import")
                print("here")
            else:
                self.errors.append(INVALID_FILE)
        if len(self.errors) < 1:
            print("Committing")
            # no major errors so commit changes
            DB.session.commit()
        return

    def get_league_id(self, league):
        '''
        a method that gets the league id for the name
        Parameters:
            league: the league's name (str)
        Returns:
            id: the id of the team (int) None if no league is found
        '''
        id = None
        league= League.query.filter_by(name=league).first()
        if league is not None:
            id = league.id
        else:
            # cant assume some league so return None
            self.errors.append(NO_LEAGUE)
        print(id)
        return id

    def set_teams(self):
        '''
        a method that sets the teams for the league
        Parameters:
            None
        Updates:
            self.teams: a dictionary with {name:id, etc..}
        '''
        self.teams = {}
        league = League.query.get(self.league_id)
        for team in league.teams:
            self.teams[str(team)] = team.id

    def set_columns_indices(self, headers):
        '''
        a method that set the indices for the column headers
        Parameters:
            headers: the list of headers (list of str)
        Returns:
        '''
        for i in range(0, len(headers)):
            if "home team" in headers[i].lower():
                self.home_index = i
            elif "away team" in headers[i].lower():
                self.away_index = i
            elif "date" in headers[i].lower():
                self.date_index = i
            elif "time" in headers[i].lower():
                self.time_index = i
            elif "field" in headers[i].lower():
                self.field_index = i
            
        return

    def import_game(self, info):
        '''
        a method the imports a one game
        Parameters:
            info: the string that contains the information of a player (str)
        Returns:
        '''
        print("1")
        info = info.split(",")
        print(info)
        if (len(info) < self.away_index or 
            len(info) < self.home_index or
            len(info) < self.time_index or
            len(info) < self.field_index or
            len(info) < self.date_index):
            print(len(info) < self.away_index,
            len(info) < self.home_index,
            len(info) < self.time_index,
            len(info) < self.field_index,
            len(info) < self.date_index)
            return # probably just an empty line
        away = info[self.away_index].strip()
        home = info[self.home_index].strip()
        time = info[self.time_index].strip()
        field = info[self.field_index].strip()
        date = info[self.date_index].strip()
        print("2")
        # check if variables meet certain conditions
        if (not string_validator(away) or
            not string_validator(home) or
            not time_validator(time) or
            not date_validator(date) or
            not string_validator(field)):
            g = away + " vs. " + home + " on " + date
            self.errors.append(INVALID_FIELD.format(g))
        else:
            # else should be good to add game
            away_team = self.teams.get(away, None)
            home_team = self.teams.get(home, None)
            print(home_team, away_team)
            if away_team is None:
                self.errors.append(INVALID_TEAM.format(away))
            if home_team is None:
                self.errors.append(INVALID_TEAM.format(home))
            if away_team is not None and home_team is not None:
                # else should be good to add the game
                date = datetime.strptime(date + "-" +time,
                                              '%Y-%m-%d-%H:%M')
                game = Game(date,
                            home_team,
                            away_team,
                            self.league_id,
                            field=field)
                DB.session.add(game)
        return

    def check_header(self,header):
        '''
        a method that checks if the header is valid
        Parameters:
            header: the header to check (list of str)
        Returns:
            valid: True if the header meets the template (boolean)
        '''
        valid = True 
        if len(header) < 2:
            valid = False
        elif len(header[0].split(",")) < 2 or len(header[1].split(",")) < 5:
            valid = False
        else:
            columns = header[1].lower()
            if "home team" not in columns:
                valid = False
            elif "away team" not in columns:
                valid = False
            elif "date" not in columns:  
                valid = False
            elif "time" not in columns:
                valid = False
            elif "field" not in columns:
                valid = False
        return valid

    def parse_header(self, header):
        '''
        a method that parses the header
        Parameters:
            header: the header to check (list of str)
        Returns:
            league: the mame of the league (str)
            headers: the column headers (list)
        '''
        first = header[0].split(",")
        league = first[1]
        headers = header[1].split(",")
        return league, headers

# the test for this class are not the best might need to be fixed later
import unittest
from pprint import PrettyPrinter
from api import app
import tempfile
class testSubTester(unittest.TestCase):
    # this is just to test the subroutines
    # was having trouble and need to run the test individual of else
    # the one query stalls
    def setUp(self):
        self.show_results = False
        self.pp = PrettyPrinter(indent=4)
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        DB.engine.execute('''   
                            DROP TABLE IF EXISTS roster;
                            DROP TABLE IF EXISTS bat;
                            DROP TABLE IF EXISTS game;
                            DROP TABLE IF EXISTS team;
                            DROP TABLE IF EXISTS player;
                            DROP TABLE IF EXISTS sponsor;
                            DROP TABLE IF EXISTS league;
                            ''')
        DB.create_all()
        self.test = [
                     "League:,Monday and Wednesday,,,",
                     "Home Team,Away Team,Date,Time,Field",
                     "Domus Green,Chainsaw Black,2015-10-01", "12:00", "WP1"]
        self.too_short = ["Home Team,Away Team,Date,Time,Field",]
        self.too_few_columns = ["League:,Monday and Wednesday,,,",
                                "Home Team,Away Team,Date,Time",
                                "Domus Green,Chainsaw Black,2015-10-01", "12:00", "WP1"
                                ]
        self.missing_home_name = [
                                    "League:,Monday and Wednesday,,,",
                                    ",Away Team,Date,Time",
                                    "Domus Green,Chainsaw Black,2015-10-01", "12:00", "WP1"
                                ]

    def tearDown(self):
        print("Teardown")
#         DB.engine.execute('''   
#                             DROP TABLE IF EXISTS roster;
#                             DROP TABLE IF EXISTS bat;
#                             DROP TABLE IF EXISTS game;
#                             DROP TABLE IF EXISTS team;
#                             DROP TABLE IF EXISTS player;
#                             DROP TABLE IF EXISTS sponsor;
#                             DROP TABLE IF EXISTS league;
#                             ''')

    def testParseHeader(self):
        self.tl = LeagueList(self.test)
        l,h = self.tl.parse_header(self.test[0:2])
        self.assertEqual(l, 'Monday and Wednesday')
        self.assertEqual(h, ["Home Team", "Away Team", "Date", "Time", "Field"])

    def testCheckHeader(self):
        # check valid header
        self.tl = LeagueList(self.test)
        valid = self.tl.check_header(self.test[0:2])
        self.assertEqual(valid, True)
        # check a header that is too short
        self.tl = LeagueList(self.too_short)
        valid = self.tl.check_header(self.too_short[0:2])
        self.assertEqual(valid, False)
        # check a header that has too few columns
        self.tl = LeagueList(self.too_few_columns)
        valid = self.tl.check_header(self.too_few_columns[0:2])
        self.assertEqual(valid, False)
        # check a header that is missing a column
        self.tl = LeagueList(self.missing_home_name)
        valid = self.tl.check_header(self.too_few_columns[0:2])
        self.assertEqual(valid, False)

    def insertSponsors(self):
        self.sponsors = [Sponsor("Domus"),
                         Sponsor("Chainsaw")
                         ]
        for s in range(0,len(self.sponsors)):
            DB.session.add(self.sponsors[s])
        DB.session.commit()

    def insertTeams(self):
        self.insertLeague()
        self.insertSponsors()
        # team one
        self.teams = [Team(color="Green", league_id=1),
                      Team(color="Black", league_id=1)
                      ]
        self.teams[0].sponsor_id = self.sponsors[0].id
        self.teams[1].sponsor_id = self.sponsors[1].id
        for t in range(0, len(self.teams)):
            DB.session.add(self.teams[t])
        DB.session.commit()

    def insertLeague(self):
        self.league = League("Monday and Wednesday")
        DB.session.add(self.league)
        DB.session.commit()

    def testGetLeagueID(self):
        self.insertLeague()
        self.tl = LeagueList(self.test)
        team = self.tl.get_league_id("Monday and Wednesday") 
        self.assertEqual(team, 1)
        self.tl = LeagueList(self.test)
        team = self.tl.get_league_id("No League") 
        self.assertEqual(team, None)
        self.assertEqual(self.tl.errors,
                         [NO_LEAGUE])

    def testImportGame(self):
        self.insertTeams()
        # add games to the league
        self.valid_test = [
                           "League:,Monday and Wednesday,,,",
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
        self.assertEqual(self.tl.errors, ["Domus Black is not a team in the league"])
        # some bad field

class testTeamImport(unittest.TestCase):
    def setUp(self):
        self.show_results = False
        self.pp = PrettyPrinter(indent=4)
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        #app.config['TESTING'] = True
        #self.app = app.test_client()
        DB.engine.execute('''   
                            DROP TABLE IF EXISTS roster;
                            DROP TABLE IF EXISTS bat;
                            DROP TABLE IF EXISTS game;
                            DROP TABLE IF EXISTS team;
                            DROP TABLE IF EXISTS player;
                            DROP TABLE IF EXISTS sponsor;
                            DROP TABLE IF EXISTS league;
                            ''')
        DB.create_all()
        self.valid_test = [
                         "League:,Monday and Wednesday,,,",
                         "Home Team,Away Team,Date,Time,Field",
                         "Domus Green,Chainsaw Black,2015-10-01,12:00,WP1"
                         ]
        self.bad_header = [
                         "League:,Monday and Wednesday,,,",
                         "BAD,HEADER,Date,Time,Field",
                         "Domus Green,Chainsaw Black,2015-10-01,12:00,WP1"
                         ]
        self.bad_league = [
                         "League:,Fuck you,,,",
                         "Home Team,Away Team,Date,Time,Field",
                         "Domus Green,Chainsaw Black,2015-10-01,12:00,WP1"
                         ]
        self.bad_game = [
                         "League:,Monday and Wednesday,,,",
                         "Home Team,Away Team,Date,Time,Field",
                         "Domus Green,Chainsaw Black,2015-XX-01,12:00,WP1"
                         ]
        self.bad_team = [
                         "League:,Monday and Wednesday,,,",
                         "Home Team,Away Team,Date,Time,Field",
                         "XX,Chainsaw Black,2015-10-01,12:00,WP1"
                         ]

    def tearDown(self):
        pass
#         DB.engine.execute('''   
#                             DROP TABLE IF EXISTS roster;
#                             DROP TABLE IF EXISTS bat;
#                             DROP TABLE IF EXISTS game;
#                             DROP TABLE IF EXISTS team;
#                             DROP TABLE IF EXISTS player;
#                             DROP TABLE IF EXISTS sponsor;
#                             DROP TABLE IF EXISTS league;
#                             ''')

    def insertSponsors(self):
        self.sponsors = [Sponsor("Domus"),
                         Sponsor("Chainsaw")
                         ]
        for s in range(0,len(self.sponsors)):
            DB.session.add(self.sponsors[s])
        DB.session.commit()

    def insertTeams(self):
        self.insertLeague()
        self.insertSponsors()
        # team one
        self.teams = [Team(color="Green", league_id=1),
                      Team(color="Black", league_id=1)
                      ]
        self.teams[0].sponsor_id = self.sponsors[0].id
        self.teams[1].sponsor_id = self.sponsors[1].id
        for t in range(0, len(self.teams)):
            DB.session.add(self.teams[t])
        DB.session.commit()

    def insertLeague(self):
        self.league = League("Monday and Wednesday")
        DB.session.add(self.league)
        DB.session.commit()

    def testValidCases(self):
        self.insertTeams()
        # import  a set of good games
        self.tl = LeagueList(self.valid_test)
        self.tl.import_league()
        self.assertEqual([], self.tl.warnings)
        self.assertEqual([], self.tl.errors)

    def testInvalidCases(self):
        self.insertTeams()
        # test bad header
        self.tl = LeagueList(self.bad_header)
        self.tl.import_league()
        self.assertEqual(self.tl.warnings, [])
        self.assertEqual(self.tl.errors, [INVALID_FILE])
        # test bad league
        self.tl = LeagueList(self.bad_league)
        self.tl.import_league()
        self.assertEqual(self.tl.warnings, [])
        self.assertEqual(self.tl.errors, [NO_LEAGUE])
        # test bad game
        self.tl = LeagueList(self.bad_game)
        self.tl.import_league()
        self.assertEqual(self.tl.warnings, [])
        expect = "Chainsaw Black vs. Domus Green on 2015-XX-01"
        self.assertEqual(self.tl.errors, [INVALID_FIELD.format(expect)])
        # test bad team in game
        self.tl = LeagueList(self.bad_team)
        self.tl.import_league()
        self.assertEqual(self.tl.warnings, [])
        self.assertEqual(self.tl.errors, [INVALID_TEAM.format("XX")])
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()