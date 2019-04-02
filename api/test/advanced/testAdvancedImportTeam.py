'''
@author: Dallas Fraser
@author: 2019-03-31
@organization: MLSB API
@summary: Tests the importing of team csv
'''
from datetime import date
from base64 import b64encode
from api.advanced.import_team import parse_lines, BACKGROUND, HEADERS,\
                                     INVALID_ROW, extract_player_information,\
                                     extract_players,\
                                     extract_column_indices_lookup
from api.test.BaseTest import TestSetup, ADMIN, PASSWORD, KIK, KIKPW
from api.errors import InvalidField
headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' +
                                                  PASSWORD, "utf-8")
                                            ).decode("ascii")
}
kik = {
    'Authorization': 'Basic %s' % b64encode(bytes(KIK + ':' +
                                                  KIKPW, "utf-8")
                                            ).decode("ascii")
}
VALID_YEAR = date.today().year
INVALID_YEAR = 100

class TestTeamImportParseLines(TestSetup):

    def testParseLines(self):
        """Test a a valid file in the standard format"""
        sponsor = "Test Import Sponsor"
        color = "Blue"
        captain = "Test Captain"
        league = "Test Import League"
        lines = ["{}:,{},".format(BACKGROUND['sponsor_name'], sponsor),
                 "{}:,{},".format(BACKGROUND['team_color'], color),
                 "{}:,{},".format(BACKGROUND['captain_name'], captain),
                 "{}:,{},".format(BACKGROUND['league_name'], league),
                 "{},{},{}".format(HEADERS['name'],
                                   HEADERS['email'],
                                   HEADERS['gender']),
                 "Test Captain,testcaptainimport@mlsb.ca,M",
                 "Test Girl,testgirlimport@mlsb.ca,F",
                 "Test Boy,testboyimport@mlsb.ca,M"]

        # parse the lines
        result = parse_lines(lines)

        # expecting no warnings
        self.assertEqual(result['warnings'], [], "Expected no warnings")
        

        # check background
        expected_background = {'sponsor': sponsor,
                               'color': color,
                               'captain': captain,
                               'league': league}
        error = "Failed parsing background"
        self.output(result['background'])
        self.output(expected_background)
        self.assertEqual(result['background'], expected_background, error)

        # check header
        expected_header = [HEADERS['name'],
                           HEADERS['email'],
                           HEADERS['gender']]
        error = "Failed parsing header"
        self.output(result['header'])
        self.output(expected_header)
        self.assertEqual(result['header'], expected_header, error)

        # check the players
        expected_players = [player.split(",") for player in lines[-3:]]
        self.assertEqual(result['players'],
                         expected_players,
                         "Players not returned")

    def testParseLinesOrder(self):
        """Test that the order of a valid file does not matter"""
        sponsor = "Test Import Sponsor"
        color = "Blue"
        captain = "Test Captain"
        league = "Test Import League"
        lines = [
                 "{},{},{}".format(HEADERS['name'],
                                   HEADERS['email'],
                                   HEADERS['gender']),
                 "{}:,{},".format(BACKGROUND['league_name'], league),
                 "Test Captain,testcaptainimport@mlsb.ca,M",
                 "{}:,{},".format(BACKGROUND['captain_name'], captain),
                 "Test Girl,testgirlimport@mlsb.ca,F",
                 "{}:,{},".format(BACKGROUND['team_color'], color),
                 "Test Boy,testboyimport@mlsb.ca,M",
                 "{}:,{},".format(BACKGROUND['sponsor_name'], sponsor)
                 ]
        # parse the lines
        result = parse_lines(lines)

        # expecting no warnings
        self.assertEqual(result['warnings'], [], "Expected no warnings")
        

        # check background
        expected_background = {'sponsor': sponsor,
                               'color': color,
                               'captain': captain,
                               'league': league}
        error = "Failed parsing background"
        self.output(result['background'])
        self.output(expected_background)
        self.assertEqual(result['background'], expected_background, error)

        # check header
        expected_header = [HEADERS['name'],
                           HEADERS['email'],
                           HEADERS['gender']]
        error = "Failed parsing header"
        self.output(result['header'])
        self.output(expected_header)
        self.assertEqual(result['header'], expected_header, error)

        # check the players
        expected_players = [["Test Captain","testcaptainimport@mlsb.ca","M"],
                            ["Test Girl","testgirlimport@mlsb.ca","F"],
                            ["Test Boy","testboyimport@mlsb.ca","M"]]
        self.assertEqual(result['players'],
                         expected_players,
                         "Players not returned")

    def testParseLinesDelimter(self):
        """Test using a different delimiter"""
        sponsor = "Test Import Sponsor"
        color = "Blue"
        captain = "Test Captain"
        league = "Test Import League"
        lines = ["{}:|{}|".format(BACKGROUND['sponsor_name'], sponsor),
                 "{}:|{}|".format(BACKGROUND['team_color'], color),
                 "{}:|{}|".format(BACKGROUND['captain_name'], captain),
                 "{}:|{}|".format(BACKGROUND['league_name'], league),
                 "{}|{}|{}".format(HEADERS['name'],
                                   HEADERS['email'],
                                   HEADERS['gender']),
                 "Test Captain|testcaptainimport@mlsb.ca|M",
                 "Test Girl|testgirlimport@mlsb.ca|F",
                 "Test Boy|testboyimport@mlsb.ca|M"]

        # parse the lines
        result = parse_lines(lines, delimiter="|")

        # expecting no warnings
        self.assertEqual(result['warnings'], [], "Expected no warnings")
        

        # check background
        expected_background = {'sponsor': sponsor,
                               'color': color,
                               'captain': captain,
                               'league': league}
        error = "Failed parsing background"
        self.output(result['background'])
        self.output(expected_background)
        self.assertEqual(result['background'], expected_background, error)

        # check header
        expected_header = [HEADERS['name'],
                           HEADERS['email'],
                           HEADERS['gender']]
        error = "Failed parsing header"
        self.output(result['header'])
        self.output(expected_header)
        self.assertEqual(result['header'], expected_header, error)

        # check the players
        expected_players = [player.split("|") for player in lines[-3:]]
        self.assertEqual(result['players'],
                         expected_players,
                         "Players not returned")

    def testParseLinesWarnings(self):
        """Test a a valid file in the standard format"""
        sponsor = "Test Import Sponsor"
        color = "Blue"
        captain = "Test Captain"
        league = "Test Import League"
        lines = ["{}:,{},".format(BACKGROUND['sponsor_name'], sponsor),
                 "{}:,{},".format(BACKGROUND['team_color'], color),
                 "WARNING,WARNING",
                 "{}:,{},".format(BACKGROUND['captain_name'], captain),
                 "{}:,{},".format(BACKGROUND['league_name'], league),
                 "{},{},{}".format(HEADERS['name'],
                                   HEADERS['email'],
                                   HEADERS['gender']),
                 "WARNING,WARNING",
                 "Test Captain,testcaptainimport@mlsb.ca,M",
                 "Test Girl,testgirlimport@mlsb.ca,F",
                 "WARNING,WARNING",
                 "Test Boy,testboyimport@mlsb.ca,M"]

        # parse the lines
        result = parse_lines(lines)

        # check that there four warnings
        expected_warnings = [INVALID_ROW.format("WARNING,WARNING"),
                             INVALID_ROW.format("WARNING,WARNING"),
                             INVALID_ROW.format("WARNING,WARNING")]
        self.output(result['warnings'])
        self.output(expected_warnings)
        self.assertEqual(result['warnings'],
                         expected_warnings,
                         "Warnings were not returned")

        # check background
        expected_background = {'sponsor': sponsor,
                               'color': color,
                               'captain': captain,
                               'league': league}
        error = "Failed parsing background"
        self.output(result['background'])
        self.output(expected_background)
        self.assertEqual(result['background'], expected_background, error)

        # check header
        expected_header = [HEADERS['name'],
                           HEADERS['email'],
                           HEADERS['gender']]
        error = "Failed parsing header"
        self.output(result['header'])
        self.output(expected_header)
        self.assertEqual(result['header'], expected_header, error)

        # check the players
        expected_players = [["Test Captain","testcaptainimport@mlsb.ca","M"],
                            ["Test Girl","testgirlimport@mlsb.ca","F"],
                            ["Test Boy","testboyimport@mlsb.ca","M"]]
        self.assertEqual(result['players'],
                         expected_players,
                         "Players not returned")

class TestTeamImportExtracingFunction(TestSetup):
    def testExtractPlayerInformation(self):
        # the test date
        name = "Test Import Parse PlayerCaptain"
        email = "testImportParsePlayer@mlsb.ca"
        gender = "M"
        info = [name, email, gender]

        # parse the information using the lookup
        lookup = {"email": 1, "name": 0, "gender": 2}
        result = extract_player_information(info, lookup)

        # expecting the player to not be found but data parsed
        self.assertEqual(result['player_id'],
                         None,
                         "Player id set for non-existent player")
        self.assertEqual(result['name'],
                         name,
                         "Player name was not extracted")
        self.assertEqual(result['email'],
                         email,
                         "Player email was not extracted")
        self.assertEqual(result['gender'],
                         gender,
                         "Player gender was not extracted")

        # now again with player in database
        player = self.add_player(name, email, gender, "", True)
        result = extract_player_information(info, lookup)

        # expecting the player to not be found but data parsed
        self.assertEqual(result['player_id'],
                         player['player_id'],
                         "Player id not set for existing player")
        self.assertEqual(result['name'],
                         name,
                         "Player name was not extracted")
        self.assertEqual(result['email'],
                         email,
                         "Player email was not extracted")
        self.assertEqual(result['gender'],
                         gender,
                         "Player gender was not extracted")

    def testExtractPlayers(self):
        # player data to extract
        player_one = {'name': "p1",
                      'email': "testImportPlayersOne@mlsb.ca",
                      'gender': "M"}
        player_two = {'name': "p2",
                      'email': "testImportPlayersTwo@mlsb.ca",
                      'gender': "F"}
        players = [[player_one['email'],
                    player_one['name'],
                    player_one['gender']],
                   [player_two['email'],
                    player_two['name'],
                    player_two['gender']]]

        # extract the two players
        lookup = {"email": 0, "name": 1, "gender": 2}
        result = extract_players(players, lookup)

        # should have two players
        self.assertEqual(len(result['player_info']),
                         2,
                         "Some player was not extracted")

        # should have no warnings
        self.assertEqual(len(result['warnings']),
                         0,
                         "Unexpected wanring when extracting players")

        # check player one
        self.assertEqual(result['player_info'][0]['player_id'],
                         None,
                         "Player id set for non-existent player")
        self.assertEqual(result['player_info'][0]['name'],
                         player_one['name'],
                         "Player name was not extracted")
        self.assertEqual(result['player_info'][0]['email'],
                         player_one['email'],
                         "Player email was not extracted")
        self.assertEqual(result['player_info'][0]['name'],
                         player_one['name'],
                         "Player name was not parsed")

        # check player two
        self.assertEqual(result['player_info'][1]['player_id'],
                         None,
                         "Player id set for non-existent player")
        self.assertEqual(result['player_info'][1]['name'],
                         player_two['name'],
                         "Player name was not extracted")
        self.assertEqual(result['player_info'][1]['email'],
                         player_two['email'],
                         "Player email was not extracted")
        self.assertEqual(result['player_info'][1]['name'],
                         player_two['name'],
                         "Player name was not parsed")

    def testExtractPlayersWarnings(self):
                # player data to extract
        player_one = {'name': "ex. p1",
                      'email': "testImportPlayersOne@mlsb.ca",
                      'gender': "M"}
        player_two = {'name': "p2",
                      'email': "testImportPlayersTwo@mlsb.ca",
                      'gender': "F"}
        players = [[player_one['email'],
                    player_one['name'],
                    player_one['gender']],
                   [player_two['email'],
                    player_two['name'],
                    player_two['gender'],
                    "Extra Row"]]

        # extract the two players
        lookup = {"email": 0, "name": 1, "gender": 2}
        result = extract_players(players, lookup)

        # should have two players
        self.assertEqual(len(result['player_info']),
                         0,
                         "Some player was not extracted")

        # should have no warnings
        self.assertEqual(len(result['warnings']),
                         2,
                         "Unexpected wanring when extracting players")

    def testExtractColumnIndicesLookup(self):
        # simple working example
        header = ["Email", "name", "GeNdEr"]
        lookup = extract_column_indices_lookup(header)
        self.assertEqual(0, lookup['email'], "Did not extract email header")
        self.assertEqual(1, lookup['name'], "Did not extract name header")
        self.assertEqual(2, lookup['gender'], "Did not extract gender header")

        try:
            header = ["Email", "name"]
            lookup = extract_column_indices_lookup(header)
            self.assertTrue(False, "Should have raised exception")
        except InvalidField:
            pass

        try:
            header = ["Email", "gender"]
            lookup = extract_column_indices_lookup(header)
            self.assertTrue(False, "Should have raised exception")
        except InvalidField:
            pass

        try:
            header = ["name", "gender"]
            lookup = extract_column_indices_lookup(header)
            self.assertTrue(False, "Should have raised exception")
        except InvalidField:
            pass