'''
Name: Dallas Fraser
Date: 2015-11-08
Project: MLSB API
Purpose: Holds a class TeamList that helps imports a team roster
'''
# imports
from sqlalchemy.sql.expression import and_
from api.model import Sponsor, Team, Player
from api import DB
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from api.validators import gender_validator, string_validator
# constants
CREATED = "Created Team (no league was specified"
NO_SPONSOR = "Cannot find sponsor, please ensure spelt correctly or create sponsor"
INVALID_FILE = "File was not given in right format (use template)"
EXAMPLE_FOUND = "First entry contain the templates example, just skipped it"
EMAIL_NAME = "Player {} email was found but had different name"
INVALID_FIELD = "{} had an invalid field"

class TeamList():
    def __init__(self, lines):
        self.success = False
        self.errors = []
        self.warnings = []
        self.lines = lines

    def import_team(self):
        '''
        a method that imports a team list based on a csv template and imports
        Parameters:
            
        Updates:
            success: a boolean if the import was successful (boolean)
            errors: a list of possible error (list)
            warnings: a list of possible warnings (list)
        '''
        if self.lines is not None:
            if self.check_header(self.lines[0:2]):
                sponsor, color, headers = self.parse_header(self.lines[0:2])
                print("Getting Team_id")
                self.team_id = self.get_team_id(sponsor, color)
                print("Got team id")
                self.set_columns_indices(headers)
                print("Got set column indcides")
                if self.team_id is not None:
                    print("selt line")
                    players = self.lines[2:]
                    for player in players:
                        print(player)
                        self.import_player(player)
                        print("Done Import")
                print("here")
            else:
                self.errors.append(INVALID_FILE)
        if len(self.errors) < 1:
            print("Committing")
            # no major errors so commit changes
            DB.session.commit()
        return

    def get_team_id(self, sponsor, color):
        '''
        a function that gets the team id for the corresponding sponsor or color
        if no team id then creates the team, if no sponsor then returns none
        Parameters:
            sponsor: the team's sponsor (str)
            color: the team's color (str)
        Returns:
            id: the id of the team (int) None if no team is found/created
        '''
        id = None
        sponsor = Sponsor.query.filter_by(name=sponsor).first()
        if sponsor is not None:
            sponsor_id = sponsor.id
            team = DB.session.query(Team)
            team = team.filter(Team.sponsor_id==sponsor_id)
            team = team.filter_by(color=color).first()
            # check if a previous team and if not create it
            if team is None:
                team = Team(color=color, sponsor_id=sponsor_id)
                id = DB.session.add(team)
                DB.session.commit()
                self.warnings.append(CREATED)
            id = team.id
        else:
            # cant assume some sponsor so return None
            self.errors.append(NO_SPONSOR)
        print(id)
        return id

    def set_columns_indices(self, headers):
        '''
        a method that set the indices for the column headers
        Parameters:
            headers: the list of headers (list of str)
        Returns:
        '''
        for i in range(0, len(headers)):
            if "email" in headers[i].lower():
                self.email_index = i
            elif "name" in headers[i].lower():
                self.name_index = i
            elif "gender" in headers[i].lower():
                self.gender_index = i
        return

    def import_player(self, info):
        '''
        a method the imports a one player
        Parameters:
            info: the string that contains the information of a player (str)
        Returns:
        '''
        print("1")
        info = info.split(",")
        if (len(info) < self.name_index or 
            len(info) < self.email_index or
            len(info) < self.gender_index):
            return # probably just an empty line
        name = info[self.name_index]
        email = info[self.email_index]
        gender = info[self.gender_index]
        print("2")
        # check if variables meet certain conditions
        if (not string_validator(name) or
            not string_validator(email) or
            not gender_validator(gender)):
            self.errors.append(INVALID_FIELD.format(name +"-"+email))
        else:
            # check if similar to template example just skip if it is
            if ("Dallas Fraser" in name or
                "fras2560@mylaurier.ca" in email):
                self.warnings.append(EXAMPLE_FOUND)
                print("Found example")
            else:
                # else should be good to add player
                #check the player exists already
                search = Player.query.filter_by(email=email).first()
                if search is None:
                    # player does not exist so need to add
                    player = Player(name, email, gender)
                    DB.session.add(player)
                else:
                    # player does exist
                    player = search
                    if search.name != name:
                        self.warnings.append(EMAIL_NAME.format(email))
                team = Team.query.get(self.team_id)
                team.players.append(player)
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
        elif len(header[0].split(",")) < 4 or len(header[1].split(",")) < 4:
            valid = False
        else:
            columns = header[1].lower()
            if "email" not in columns:
                valid = False
            elif "name" not in columns:
                valid = False
            elif "gender" not in columns:  
                valid = False
        return valid
    
    def parse_header(self, header):
        '''
        a method that parses the header
        Parameters:
            header: the header to check (list of str)
        Returns:
            sponsor: the sponsor of the team (str)
            color: the color of the team (str)
            headers: the column headers (list)
        '''
        first = header[0].split(",")
        sponsor = first[1]
        color = first[3]
        headers = header[1].split(",")
        return sponsor, color, headers


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
                     "Sponsor:,SPORTZONE,Color:,Pink",
                     "Player Name,Player Email,Gender (M/F),",
                     "EX. Dallas Fraser,fras2560@mylaurier.ca,M,"]
        self.too_short = ["Sponsor:,EX. SPORTZONE,Color:,Pink"]
        self.too_few_columns = ["Sponsor:,EX. SPORTZONE,Color:,Pink",
                                "Player Name,Player Email,Gender",
                                ]
        self.missing_player_name = [
                                    "Sponsor:,EX. SPORTZONE,Color:,Pink",
                                    ",Player Email,Gender (M/F),",
                                    "EX. Dallas Fraser,fras2560@mylaurier.ca,M,"
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
        self.tl = TeamList(self.test)
        s,c,h = self.tl.parse_header(self.test[0:2])
        self.assertEqual(s ,'EX. SPORTZONE')
        self.assertEqual(c, 'Pink')
        self.assertEqual(h, ['Player Name', 'Player Email', 'Gender (M/F)', ''])

    def testCheckHeader(self):
        # check valid header
        self.tl = TeamList(self.test)
        valid = self.tl.check_header(self.test[0:2])
        self.assertEqual(valid, True)
        # check a header that is too short
        self.tl = TeamList(self.too_short)
        valid = self.tl.check_header(self.too_short[0:2])
        self.assertEqual(valid, False)
        # check a header that has too few columns
        self.tl = TeamList(self.too_few_columns)
        valid = self.tl.check_header(self.too_few_columns[0:2])
        self.assertEqual(valid, False)
        # check a header that is missing a column
        self.tl = TeamList(self.missing_player_name)
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
        self.insertSponsors()
        # team one
        self.teams = [Team(color="Green"),
                      Team(color="Black")
                      ]
        self.teams[0].sponsor_id = self.sponsors[0].id
        self.teams[1].sponsor_id = self.sponsors[1].id
        for t in range(0, len(self.teams)):
            DB.session.add(self.teams[t])
        DB.session.commit()

    def testGetTeamID(self):
        self.insertTeams()
        self.tl = TeamList(self.test)
        team = self.tl.get_team_id("Domus", "Green") 
        self.assertEqual(team, 1)
        self.tl = TeamList(self.test)
        team = self.tl.get_team_id("Domus", "Black") 
        self.assertEqual(team, 3)
        self.assertEqual(self.tl.warnings,
                         [CREATED])
        team = self.tl.get_team_id("No Sponsor", "Black") 
        self.assertEqual(team, None)
        self.assertEqual(self.tl.errors,
                         [NO_SPONSOR])

    def testImportPlayer(self):
        self.insertTeams()
        # add new player to new team
        self.valid_test = [
                     "Sponsor:,Domus,Color:,Green",
                     "Player Name,Player Email,Gender (M/F),",
                     "Marc Gallucci,gall4400@mylaurier.ca,M,"]
        self.tl = TeamList(self.valid_test)
        self.tl.team_id = 1
        self.tl.set_columns_indices(self.valid_test[1].split(","))
        self.tl.import_player(self.valid_test[2])
        self.assertEqual(self.tl.warnings, [])
        self.assertEqual(self.tl.errors, [])
        # add old player to another team
        self.valid_test = [
                     "Sponsor:,Chainsaw,Color:,Black",
                     "Player Name,Player Email,Gender (M/F),",
                     "Marc Gallucci,gall4400@mylaurier.ca,M,"]
        self.tl = TeamList(self.valid_test)
        self.tl.team_id = 2
        self.tl.set_columns_indices(self.valid_test[1].split(","))
        self.tl.import_player(self.valid_test[2])
        self.assertEqual(self.tl.warnings, [])
        self.assertEqual(self.tl.errors, [])

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
                             "Sponsor:,Domus,Color:,Green",
                             "Player Name,Player Email,Gender (M/F),",
                             "Marc Gallucci,gall4400@mylaurier.ca,M,"]
        self.valid_create_test = ["Sponsor:,Domus,Color:,Black",
                                  "Player Name,Player Email,Gender (M/F),",
                                  "Dream Girl,dream@mylaurier.ca,F,"]
        self.invalid_sponsor = [
                             "Sponsor:,Sportzone,Color:,Green",
                             "Player Name,Player Email,Gender (M/F),",
                             "Marc Gallucci,gall4400@mylaurier.ca,M,"]
        self.invalid_players = [
                             "Sponsor:,Domus,Color:,Green",
                             "Player Name,Player Email,Gender (M/F),",
                             "1,gall4400@mylaurier.ca,M,",
                             "t,1,M,",
                             "g,g,X,"]
        self.test_skip_example = ["Sponsor:,Domus,Color:,Green",
                                  "Player Name,Player Email,Gender (M/F),",
                                  "Dallas Fraser,fras2560@mylaurier.ca,M,"]
        self.bad_header = ["Sponsor:,EX. SPORTZONE,Color:,Pink"]
        self.bad_sponsor = ["Sponsor:,No Sponsor,Color:,Green",
                            "Player Name,Player Email,Gender (M/F),",]
        self.bad_player = ["Sponsor:,Domus,Color:,Green",
                             "Player Name,Player Email,Gender (M/F),",
                             "Marc Gallucci,gall4400@mylaurier.ca,M,"]
        self.warning_player = ["Sponsor:,Domus,Color:,Black",
                             "Player Name,Player Email,Gender (M/F),",
                             "Marco Gallucci,gall4400@mylaurier.ca,M,"]
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
        self.insertSponsors()
        # team one
        self.teams = [Team(color="Green"),
                      Team(color="Black")
                      ]
        self.teams[0].sponsor_id = self.sponsors[0].id
        self.teams[1].sponsor_id = self.sponsors[1].id
        for t in range(0, len(self.teams)):
            DB.session.add(self.teams[t])
        DB.session.commit()

    def testValidCases(self):
        self.insertTeams()
        # first test just import player to created team
        self.tl = TeamList(self.valid_test)
        self.tl.import_team()
        self.assertEqual([], self.tl.warnings)
        self.assertEqual([], self.tl.errors)
        # second test import player to a new team
        self.tl = TeamList(self.valid_create_test)
        self.tl.import_team()
        self.assertEqual(['Created Team (no league was specified'],
                         self.tl.warnings)
        self.assertEqual([], self.tl.errors)
        # third test that skips the template example
        self.tl = TeamList(self.test_skip_example)
        self.tl.import_team()
        expect = ['First entry contain the templates example, just skipped it']
        self.assertEqual(expect, self.tl.warnings)
        self.assertEqual([], self.tl.errors)

    def testInvalidCases(self):
        # test bad header
        self.tl = TeamList(self.bad_header)
        self.tl.import_team()
        self.assertEqual(self.tl.warnings, [])
        self.assertEqual(self.tl.errors, [INVALID_FILE])
        # test bad sponsor
        self.tl = TeamList(self.bad_sponsor)
        self.tl.import_team()
        self.assertEqual(self.tl.warnings, [])
        self.assertEqual(self.tl.errors, [NO_SPONSOR])
        # test bad player
        self.tl = TeamList(self.bad_player)
        self.tl.import_team()
        self.assertEqual(self.tl.warnings, [])
        self.assertEqual(self.tl.errors, [NO_SPONSOR])
        # test warning player
        self.tl = TeamList(self.warning_player)
        self.tl.import_team()
        self.assertEqual(self.tl.warnings, [])
        self.assertEqual(self.tl.errors, [NO_SPONSOR])
        print("Done")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()