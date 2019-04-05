'''
@author: Dallas Fraser
@author: 2019-03-31
@organization: MLSB API
@summary: Tests the importing of team csv
'''
from sqlalchemy import func
from datetime import date
from base64 import b64encode
from api.model import Team
from api.advanced.import_team import parse_lines, BACKGROUND, HEADERS,\
                                     INVALID_ROW, extract_player_information,\
                                     extract_players,\
                                     extract_column_indices_lookup,\
                                     extract_background, TeamList
from api.test.BaseTest import TestSetup, ADMIN, PASSWORD, KIK, KIKPW
from api.errors import InvalidField, SponsorDoesNotExist, LeagueDoesNotExist
from api.test.importer.testImportMockSession import TestImportMockSession
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
        expected_players = [["Test Captain", "testcaptainimport@mlsb.ca", "M"],
                            ["Test Girl", "testgirlimport@mlsb.ca", "F"],
                            ["Test Boy", "testboyimport@mlsb.ca", "M"]]
        self.assertEqual(result['players'],
                         expected_players,
                         "Players not returned")

    def testParseLinesDelimiter(self):
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
        expected_players = [["Test Captain", "testcaptainimport@mlsb.ca", "M"],
                            ["Test Girl", "testgirlimport@mlsb.ca", "F"],
                            ["Test Boy", "testboyimport@mlsb.ca", "M"]]
        self.assertEqual(result['players'],
                         expected_players,
                         "Players not returned")


class TestTeamImportExtracingFunction(TestSetup):
    def testExtractPlayerInformation(self):
        """Test extract player information"""
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
        """Test extracting a list of players"""
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
        """Test extract list of players that have warnings"""
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
        """Test extracting the lookup for fields to columns indices"""
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


class TestTeamImportExtractBackground(TestSetup):
    def testExtractBackgroundErrors(self):
        """Test that errors are raised for incomplete background """

        # some date to use through out test
        sponsor = "TTIEB Non-existent sponsor"
        color = "Some Color"
        captain = "TTIEB Non-existent player"
        league = "TTIEB Non-existent league"

        # missing background values
        try:
            extract_background({})
            self.assertTrue(False, "Expecting exception raised")
        except InvalidField:
            pass

        # given league example
        background = {'sponsor': sponsor,
                      'color': color,
                      'captain': captain,
                      'league': "ex. League Example"}
        try:
            extract_background(background)
            self.assertTrue(False, "Expecting exception raised")
        except InvalidField:
            pass

        # given captain example
        background = {'sponsor': sponsor,
                      'color': color,
                      'captain': "ex. captain",
                      'league': league}
        try:
            extract_background(background)
            self.assertTrue(False, "Expecting exception raised")
        except InvalidField:
            pass

        # given color example
        background = {'sponsor': sponsor,
                      'color': "ex. color",
                      'captain': captain,
                      'league': league}
        try:
            extract_background(background)
            self.assertTrue(False, "Expecting exception raised")
        except InvalidField:
            pass

        # given sponsor example
        background = {'sponsor': sponsor,
                      'color': "ex. color",
                      'captain': captain,
                      'league': league}
        try:
            extract_background(background)
            self.assertTrue(False, "Expecting exception raised")
        except InvalidField:
            pass

    def testExtractBackgroundCantFindSponsor(self):
        """Test extract background when cant find sponsor"""

        # some date to use through out test
        league = "TTIEB Non-existent league"
        self.add_league(league)
        sponsor = "TTIEB Non-existent sponsor"
        color = "Some Color"
        captain = "TTIEB Non-existent player"
        background = {'sponsor': sponsor,
                      'color': color,
                      'captain': captain,
                      'league': league}
        try:
            extract_background(background)
            self.assertTrue(False, "Expecting exception raised")
        except SponsorDoesNotExist:
            pass

    def testExtractBackgroundCantFindLeague(self):
        """ Test extract background when cant find league"""

        # some date to use through out test
        league = "TTIEB Non-existent league"
        sponsor = "TTIEB Non-existent sponsor"
        self.add_sponsor(sponsor)
        color = "Some Color"
        captain = "TTIEB Non-existent player"
        background = {'sponsor': sponsor,
                      'color': color,
                      'captain': captain,
                      'league': league}
        try:
            extract_background(background)
            self.assertTrue(False, "Expecting exception raised")
        except LeagueDoesNotExist:
            pass

    def testExtractBackgroundNewTeam(self):
        """Test extract background for a new team"""

        # some date to use through out test
        league = "TTIEB Non-existent league"
        sponsor = "TTIEB Non-existent sponsor"
        self.add_sponsor(sponsor)
        self.add_league(league)
        color = "Some Color"
        captain = "TTIEB Non-existent player"
        background = {'sponsor': sponsor,
                      'color': color,
                      'captain': captain,
                      'league': league}

        # extract the background
        result = extract_background(background)

        # make sure the values match what was given
        self.assertEqual(result['sponsor']['sponsor_name'],
                         sponsor,
                         "Extracted wrong sponsor")
        self.assertEqual(result['league']['league_name'],
                         league,
                         "Extracted wrong league")
        self.assertEqual(result['team']['color'],
                         color,
                         "Extracted wrong color")
        self.assertEqual(result['captain']['player_name'],
                         captain,
                         "Extract wrong captain")

    def testExtractBackgroundExistingTeam(self):
        """Test extract background for an existing team"""

        # some date to use through out test
        league_name = "TTIEB Non-existent league"
        sponsor_name = "TTIEB Non-existent sponsor"
        color = "Some Color"
        sponsor = self.add_sponsor(sponsor_name)
        league = self.add_league(league_name)
        team = self.add_team(color, sponsor, league, date.today().year)
        captain = "TTIEB Non-existent player"
        background = {'sponsor': sponsor_name,
                      'color': color,
                      'captain': captain,
                      'league': league_name}

        # extract the background
        result = extract_background(background)

        # make sure the values match what was given
        self.assertEqual(result['sponsor']['sponsor_name'],
                         sponsor_name,
                         "Extracted wrong sponsor")
        self.assertEqual(result['league']['league_name'],
                         league_name,
                         "Extracted wrong league")
        self.assertEqual(result['team']['color'],
                         color,
                         "Extracted wrong color")
        self.assertEqual(result['team']['team_id'],
                         team["team_id"],
                         "Extracted wrong existing team")
        self.assertEqual(result['captain']['player_name'],
                         captain,
                         "Extract wrong captain")


class TestTeamImportAddTeam(TestSetup):
    def testAddTeamAlreadyExists(self):
        """Import a team that already exists"""

        # the testing lines
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

        # added the needed background
        sponsor = self.add_sponsor(sponsor)
        league = self.add_league(league)
        team = self.add_team(color, sponsor, league, date.today().year)

        # import the a test team
        importer = TeamList(lines, session=TestImportMockSession(self))
        importer.add_team_functional()
        self.assertEqual(importer.warnings, [], "Importing team gave warnings")
        team = Team.query.get(team['team_id'])
        self.assertEqual(len(team.players),
                         3,
                         "Importing team players were not created")

    def testAddTeam(self):
        """Import a team that already exists"""

        # the testing lines
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

        # added the needed background
        sponsor = self.add_sponsor(sponsor)
        league = self.add_league(league)

        # import the a test team
        importer = TeamList(lines, session=TestImportMockSession(self))
        importer.add_team_functional()
        self.assertEqual(importer.warnings, [], "Importing team gave warnings")
        teams = (Team.query
                 .filter(func.lower(Team.color) == func.lower(color))
                 .filter(Team.sponsor_id == sponsor['sponsor_id'])
                 .filter(Team.year == date.today().year)).all()
        self.assertTrue(len(teams) > 0, "Import team was not created")
        team = teams[0]
        self.assertEqual(len(team.players),
                         3,
                         "Importing team players were not created")

    def testAddTeamPlayerAlreadyExists(self):
        """Import a team where one player already exists"""

        # the testing lines
        sponsor = "Test Import Sponsor"
        color = "Blue"
        captain = "Test Captain"
        league = "Test Import League"
        player_email = "testgirlimport@mlsb.ca"
        player_name = "Test Girl"
        player_gender = "F"
        lines = ["{}:,{},".format(BACKGROUND['sponsor_name'], sponsor),
                 "{}:,{},".format(BACKGROUND['team_color'], color),
                 "{}:,{},".format(BACKGROUND['captain_name'], captain),
                 "{}:,{},".format(BACKGROUND['league_name'], league),
                 "{},{},{}".format(HEADERS['name'],
                                   HEADERS['email'],
                                   HEADERS['gender']),
                 "Test Captain,testcaptainimport@mlsb.ca,M",
                 "{},{},{}".format(player_name, player_email, player_gender)]

        # added the needed background
        sponsor = self.add_sponsor(sponsor)
        league = self.add_league(league)
        player = self.add_player(player_name,
                                 player_email,
                                 gender=player_gender)

        # import the a test team
        importer = TeamList(lines, session=TestImportMockSession(self))
        importer.add_team_functional()
        self.assertEqual(importer.warnings, [], "Importing team gave warnings")
        teams = (Team.query
                 .filter(func.lower(Team.color) == func.lower(color))
                 .filter(Team.sponsor_id == sponsor['sponsor_id'])
                 .filter(Team.year == date.today().year)).all()
        self.assertTrue(len(teams) > 0, "Import team was not created")
        team = teams[0]
        self.assertEqual(len(team.players),
                         2,
                         "Importing team players were not created")
        player_ids = [p.id for p in team.players]
        self.assertTrue(player['player_id'] in player_ids,
                        "Import team existing player not added")
