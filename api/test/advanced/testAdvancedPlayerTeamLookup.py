from datetime import date
from base64 import b64encode
from api.helper import loads
from api.routes import Routes
from api.test.advanced.mock_league import MockLeague
from api.test.BaseTest import TestSetup, ADMIN, PASSWORD

headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' +
                                                  PASSWORD, "utf-8")
                                            ).decode("ascii")
}
VALID_YEAR = date.today().year
INVALID_YEAR = 100


class TestPlayerTeamLookup(TestSetup):

    def testEmail(self):
        """Tests using a player email as a parameter"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            mocker = MockLeague(self)
            league = mocker.get_league()
            team = mocker.get_teams()[0]
            player = mocker.get_players()[0]
            sponsor = mocker.get_sponsor()

            # test a test player emails
            params = {'email': mocker.get_player_email(0)}
            rv = self.app.post(Routes['vplayerteamLookup'], json=params)
            expect = [
                {
                    'captain': player,
                    'color': team['color'],
                    'espys': 0,
                    'league_id': league['league_id'],
                    'sponsor_id': sponsor['sponsor_id'],
                    'team_id': team['team_id'],
                    'team_name': team['team_name'],
                    'year': team['year']
                }
            ]
            self.output(loads(rv.data))
            self.output(expect)
            self.assertEqual(
                expect, loads(rv.data), Routes['vplayerteamLookup']
            )

    def testPlayerName(self):
        """Tests using a player name as a parameter"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            mocker = MockLeague(self)
            league = mocker.get_league()
            team = mocker.get_teams()[0]
            player = mocker.get_players()[0]
            sponsor = mocker.get_sponsor()

            # test a test player names
            params = {'player_name': player['player_name']}
            rv = self.app.post(Routes['vplayerteamLookup'], json=params)
            expect = [
                {
                    'captain': player,
                    'color': team['color'],
                    'espys': 0,
                    'league_id': league['league_id'],
                    'sponsor_id': sponsor['sponsor_id'],
                    'team_id': team['team_id'],
                    'team_name': team['team_name'],
                    'year': team['year']
                }
            ]
            self.output(loads(rv.data))
            self.output(expect)
            self.assertEqual(
                expect, loads(rv.data), Routes['vplayerteamLookup']
            )

            # test a test player names
            params = {'player_name': "Not a player"}
            rv = self.app.post(Routes['vplayerteamLookup'], json=params)
            expect = []
            self.output(loads(rv.data))
            self.output(expect)
            self.assertEqual(
                expect, loads(rv.data), Routes['vplayerteamLookup']
            )

    def testPlayerId(self):
        """Tests using a player id as a parameter"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            mocker = MockLeague(self)
            league = mocker.get_league()
            team = mocker.get_teams()[0]
            player = mocker.get_players()[0]
            sponsor = mocker.get_sponsor()

            # test a test player names
            params = {'player_id': mocker.get_players()[0]['player_id']}
            rv = self.app.post(Routes['vplayerteamLookup'], json=params)
            expect = [
                {
                    'captain': player,
                    'color': team['color'],
                    'espys': 0,
                    'league_id': league['league_id'],
                    'sponsor_id': sponsor['sponsor_id'],
                    'team_id': team['team_id'],
                    'team_name': team['team_name'],
                    'year': team['year']
                }
            ]
            self.output(loads(rv.data))
            self.output(expect)
            self.assertEqual(
                expect, loads(rv.data), Routes['vplayerteamLookup']
            )
