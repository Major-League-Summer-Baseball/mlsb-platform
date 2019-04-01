'''
@author: Dallas Fraser
@author: 2019-03-31
@organization: MLSB API
@summary: Tests the importing of team csv
'''
from datetime import date
from base64 import b64encode
from api.advanced.import_team import parse_lines, BACKGROUND, HEADERS,\
                                     INVALID_ROW
from api.test.BaseTest import TestSetup, ADMIN, PASSWORD, KIK, KIKPW
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


