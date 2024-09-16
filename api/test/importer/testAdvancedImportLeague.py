from api.model import League
from api.test.BaseTest import TestSetup
from api.importers.league import \
    LeagueList, parse_parts, BACKGROUND, HEADERS, INVALID_ROW, \
    extract_column_indices_lookup, extract_background, \
    extract_game, extract_games
from api.errors import InvalidField, LeagueDoesNotExist, TeamDoesNotExist, \
    DivisionDoesNotExist
from api.test.importer.testImportMockSession import TestImportMockSession
import datetime
import uuid


class testAdvancedImportLeagueParsing(TestSetup):

    division = "Test Import Division"
    league = "Test Import League"
    home_team = "Test Import Home Team"
    away_team = "Teat Import Away Team"
    date = datetime.date.today().strftime("%Y-%m-%d")
    time = datetime.date.today().strftime("%H:%M")
    field = "WP1"

    def testParseLines(self):
        """Test a a valid file in the standard format"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            field = "WP1"
            entry = "{},{},{},{},{}".format(
                self.home_team, self.away_team, self.date, self.time, field
            )
            lines = [
                "{}:,{},,,".format(BACKGROUND['league'], self.league),
                "{}:,{},,,".format(BACKGROUND['division'], self.division),
                ",".join(HEADERS.values()),
                entry
            ]

            # parse the lines
            result = parse_parts(lines)

            # expecting no warnings
            self.assertEqual(result['warnings'], [], "Expected no warnings")

            # check background
            expected_background = {
                'league': self.league, 'division': self.division
            }
            error = "Failed parsing background"
            self.output(result['background'])
            self.output(expected_background)
            self.assertEqual(result['background'], expected_background, error)

            # check header
            expected_header = [value for value in HEADERS.values()]
            error = "Failed parsing header"
            self.output(result['header'])
            self.output(expected_header)
            self.assertEqual(result['header'], expected_header, error)

            # check the games
            expected_games = [entry.split(",")]
            self.assertEqual(
                result['games'], expected_games, "Games not returned"
            )

    def testParseLinesOrder(self):
        """Test that the order of a valid file does not matter"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            entry = "{},{},{},{},{}".format(
                self.home_team, self.away_team, self.date, self.time, self.field
            )
            lines = [
                entry,
                "{}:,{},,,".format(BACKGROUND['league'], self.league),
                "{}:,{},,,".format(BACKGROUND['division'], self.division),
                ",".join(HEADERS.values())
            ]

            # parse the lines
            result = parse_parts(lines)

            # expecting no warnings
            self.assertEqual(result['warnings'], [], "Expected no warnings")

            # check background
            expected_background = {
                'league': self.league, 'division': self.division
            }
            error = "Failed parsing background"
            self.output(result['background'])
            self.output(expected_background)
            self.assertEqual(result['background'], expected_background, error)

            # check header
            expected_header = [value for value in HEADERS.values()]
            error = "Failed parsing header"
            self.output(result['header'])
            self.output(expected_header)
            self.assertEqual(result['header'], expected_header, error)

            # check the games
            expected_games = [entry.split(",")]
            self.assertEqual(
                result['games'], expected_games, "Games not returned"
            )

    def testParseLinesDelimiter(self):
        """Test using a different delimiter"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            entry = "{}|{}|{}|{}|{}".format(
                self.home_team, self.away_team, self.date, self.time, self.field
            )
            lines = [
                "{}:|{}|||".format(BACKGROUND['league'], self.league),
                "{}:|{}|||".format(BACKGROUND['division'], self.division),
                "|".join(HEADERS.values()),
                entry
            ]

            # parse the lines
            result = parse_parts(lines, delimiter="|")

            # expecting no warnings
            self.assertEqual(result['warnings'], [], "Expected no warnings")

            # check background
            expected_background = {
                'league': self.league, 'division': self.division
            }
            error = "Failed parsing background"
            self.output(result['background'])
            self.output(expected_background)
            self.assertEqual(result['background'], expected_background, error)

            # check header
            expected_header = [value for value in HEADERS.values()]
            error = "Failed parsing header"
            self.output(result['header'])
            self.output(expected_header)
            self.assertEqual(result['header'], expected_header, error)

            # check the games
            expected_games = [entry.split("|")]
            self.assertEqual(
                result['games'], expected_games, "Games not returned"
            )

    def testParseLinesWarnings(self):
        """Test a a valid file in the standard format"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            entry = "{},{},{},{},{}".format(
                self.home_team, self.away_team, self.date, self.time, self.field
            )
            lines = [
                "WARNING,WARNING",
                "{}:,{},,,".format(BACKGROUND['league'], self.league),
                "{}:,{},,,".format(BACKGROUND['division'], self.division),
                "WARNING,WARNING,WARNING",
                ",".join(HEADERS.values()),
                entry
            ]

            # parse the lines
            result = parse_parts(lines)

            # expecting no warnings
            expected_warnings = [
                INVALID_ROW.format("WARNING,WARNING"),
                INVALID_ROW.format("WARNING,WARNING,WARNING")
            ]
            self.output(result['warnings'])
            self.output(expected_warnings)
            self.assertEqual(
                result['warnings'],
                expected_warnings,
                "Warnings were not returned"
            )
            # check background
            expected_background = {
                'league': self.league, 'division': self.division
            }
            error = "Failed parsing background"
            self.output(result['background'])
            self.output(expected_background)
            self.assertEqual(result['background'], expected_background, error)

            # check header
            expected_header = [value for value in HEADERS.values()]
            error = "Failed parsing header"
            self.output(result['header'])
            self.output(expected_header)
            self.assertEqual(result['header'], expected_header, error)

            # check the games
            expected_games = [entry.split(",")]
            self.assertEqual(
                result['games'], expected_games, "Games not returned"
            )


class testAdvancedImpotLeagueExtractFunctions(TestSetup):

    def testExtractColumnIndicesLookup(self):
        """Test extracting the lookup for fields to columns indices"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # simple working example
            header = ["Home Team", "AwAy Team", "Date", "time", "Field"]
            lookup = extract_column_indices_lookup(header)
            self.assertEqual(
                0, lookup['home'], "Did not extract home team header"
            )
            self.assertEqual(
                1, lookup['away'], "Did not extract away team header"
            )
            self.assertEqual(
                2, lookup['date'], "Did not extract date header"
            )
            self.assertEqual(
                3, lookup['time'], "Did not extract time header"
            )
            self.assertEqual(
                4, lookup['field'], "Did not extract field header"
            )

            try:
                header = ["AwAy Team", "Date", "time", "Field"]
                lookup = extract_column_indices_lookup(header)
                self.assertTrue(False, "Should have raised exception")
            except InvalidField:
                pass

            try:
                header = ["Home Team", "Date", "time", "Field"]
                lookup = extract_column_indices_lookup(header)
                self.assertTrue(False, "Should have raised exception")
            except InvalidField:
                pass

            try:
                header = ["Home Team", "AwAy Team", "time", "Field"]
                lookup = extract_column_indices_lookup(header)
                self.assertTrue(False, "Should have raised exception")
            except InvalidField:
                pass

            try:
                header = ["Home Team", "AwAy Team", "Date", "Field"]
                lookup = extract_column_indices_lookup(header)
                self.assertTrue(False, "Should have raised exception")
            except InvalidField:
                pass

            try:
                header = ["Home Team", "AwAy Team", "Date", "time"]
                lookup = extract_column_indices_lookup(header)
                self.assertTrue(False, "Should have raised exception")
            except InvalidField:
                pass

    def testExtractBackground(self):
        """Test extract background when cant find sponsor"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # some data to use through out test
            league_name = str(uuid.uuid1())
            division_name = str(uuid.uuid1())
            league = self.add_league(league_name)
            division = self.add_division(division_name)
            background = {'league': league_name, 'division': division_name}
            result = extract_background(background)

            # check the extracted league
            self.assertEqual(
                result['league']['league_id'],
                league['league_id'],
                "Did not find existing league in background"
            )
            self.assertEqual(
                result['league']['league_name'],
                league_name,
                "Extracted league name did not match"
            )

            # check the extracted division
            self.assertEqual(
                result['division']['division_id'],
                division['division_id'],
                "Did not find existing division in background"
            )
            self.assertEqual(
                result['division']['division_name'],
                division_name,
                "Extracted division name did not match"
            )

    def testExtractBackgroundCantFindLeague(self):
        """ Test extract background when cant find league"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # some date to use through out test
            league = str(uuid.uuid1())
            division_name = str(uuid.uuid1())
            self.add_division(division_name)
            background = {'league': league, 'division': division_name}
            try:
                extract_background(background)
                self.assertTrue(False, "Expecting exception raised")
            except LeagueDoesNotExist:
                pass

    def testExtractBackgroundCantFindDivision(self):
        """ Test extract background when cant find division"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # some date to use through out test
            league_name = str(uuid.uuid1())
            division_name = str(uuid.uuid1())
            self.add_league(league_name)
            background = {'league': league_name, 'division': division_name}
            try:
                extract_background(background)
                self.assertTrue(False, "Expecting exception raised")
            except DivisionDoesNotExist:
                pass

    def testExtractGame(self):
        """Test the extract game function"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            time = "12:15"
            date = "2019-04-07"
            field = "WP1"
            lookup = {"away": 0, "home": 1, "date": 2, "time": 3, "field": 4}
            game_entry = ["away_team", "home_team", date, time, field]
            team_lookup = {"away_team": 0, "home_team": 1}
            result = extract_game(game_entry, team_lookup, lookup)

            self.assertEqual(
                0, result["away_team_id"], "Failed to extract away team id"
            )
            self.assertEqual(
                1, result["home_team_id"], "Failed to extract home team id"
            )
            self.assertEqual(
                time, result["time"], "Failed to extract time"
            )
            self.assertEqual(
                date, result["date"], "Failed to extract date"
            )
            self.assertEqual(
                field, result["field"], "Failed to extract field"
            )

    def testExtractGameNonValidRow(self):
        """Test the extract game function when row invalid"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            lookup = {"away": 0, "home": 1, "date": 2, "time": 3, "field": 100}
            game_entry = ["away_team", "home_team", "", "", ""]
            team_lookup = {"away_team": 0, "home_team": 1}
            result = extract_game(game_entry, team_lookup, lookup)
            self.assertEqual(None, result, "Expected None for invalid row")

    def testExtractGameTeamNotFound(self):
        """Test the extract game when home/away team is found"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            time = "12:15"
            date = "2019-04-07"
            field = "WP1"
            lookup = {"away": 0, "home": 1, "date": 2, "time": 3, "field": 4}
            game_entry = ["away_team", "home_team", date, time, field]
            team_lookup = {"away_team": 0}
            try:
                extract_game(game_entry, team_lookup, lookup)
                self.assertTrue(False, "Expecting an error")
            except TeamDoesNotExist:
                pass

            team_lookup = {"home_team": 0}
            try:
                extract_game(game_entry, team_lookup, lookup)
                self.assertTrue(False, "Expecting an error")
            except TeamDoesNotExist:
                pass

    def testExtractGames(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            time = "12:15"
            date = "2019-04-07"
            field = "WP1"
            lookup = {"away": 0, "home": 1, "date": 2, "time": 3, "field": 4}
            game_entries = [["away_team", "home_team", date, time, field],
                            ["not_away_team", "home_team", date, time, field]]
            team_lookup = {"away_team": 0, "home_team": 1}
            result = extract_games(game_entries, team_lookup, lookup)

            self.assertEqual(1, len(result["warnings"]))
            self.assertEqual(1, len(result["games"]))
            game_information = result["games"][0]
            self.assertEqual(
                0,
                game_information["away_team_id"],
                "Failed to extract away team id"
            )
            self.assertEqual(
                1,
                game_information["home_team_id"],
                "Failed to extract home team id"
            )
            self.assertEqual(
                time, game_information["time"], "Failed to extract time"
            )
            self.assertEqual(
                date, game_information["date"], "Failed to extract date"
            )
            self.assertEqual(
                field, game_information["field"], "Failed to extract field"
            )


class testAdvancedImportLeague(TestSetup):

    def testImportLeague(self):
        """Import a league with no warnings"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            sponsor_name = str(uuid.uuid1())
            league_name = str(uuid.uuid1())
            division_name = str(uuid.uuid1())
            team_one_color = "Blue"
            team_two_color = "Red"
            sponsor = self.add_sponsor(sponsor_name)
            league = self.add_league(league_name)
            division = self.add_division(division_name)
            team_one = self.add_team(team_one_color, sponsor, league)
            team_two = self.add_team(team_two_color, sponsor, league)
            date = datetime.datetime.today().strftime("%Y-%m-%d")
            time = datetime.datetime.today().strftime("%H:%M")
            header_line = ",".join([HEADERS["home"],
                                    HEADERS["away"],
                                    HEADERS["date"],
                                    HEADERS["time"],
                                    HEADERS["field"]])
            entry = "{},{},{},{},{}".format(
                team_one["team_name"], team_two["team_name"], date, time, "WP1"
            )
            lines = [
                "{}:,{},".format(BACKGROUND['league'], league["league_name"]),
                "{}:,{},".format(
                    BACKGROUND['division'],
                    division["division_name"]
                ),
                header_line,
                entry
            ]
            league_importer = LeagueList(
                lines, session=TestImportMockSession(self)
            )
            league_importer.import_league_functional()
            self.assertEqual(
                len(league_importer.warnings),
                0,
                "Un-expected warning when importing league"
            )
            league = League.query.get(league["league_id"])
            games = []
            for game in league.games:
                games.append(game.json())
            self.assertEqual(
                len(games), 1, "Did not add game when importing league"
            )

    def testImportLeagueWarnings(self):
        """Import a league that has warnings"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            sponsor_name = str(uuid.uuid1())
            league_name = str(uuid.uuid1())
            division_name = str(uuid.uuid1())
            team_two_color = "Red"
            sponsor = self.add_sponsor(sponsor_name)
            league = self.add_league(league_name)
            division = self.add_division(division_name)
            team_two = self.add_team(team_two_color, sponsor, league)
            date = datetime.datetime.today().strftime("%Y-%m-%d")
            time = datetime.datetime.today().strftime("%H:%M")
            header_line = ",".join([HEADERS["home"],
                                    HEADERS["away"],
                                    HEADERS["date"],
                                    HEADERS["time"],
                                    HEADERS["field"]])
            entry = "{},{},{},{},{}".format(
                "not a team", team_two["team_name"], date, time, "WP1"
            )
            lines = [
                "{}:,{},".format(BACKGROUND['league'], league["league_name"]),
                "{}:,{},".format(
                    BACKGROUND['division'],
                    division["division_name"]
                ),
                header_line,
                entry
            ]
            league_importer = LeagueList(
                lines, session=TestImportMockSession(self)
            )
            league_importer.import_league_functional()
            error = "Expected warning when non-existent team"
            self.assertEqual(len(league_importer.warnings), 1, error)
            league = League.query.get(league["league_id"])
            games = []
            for game in league.games:
                games.append(game.json())
            self.assertEqual(
                len(games), 0, "Did add game where team was missing"
            )
