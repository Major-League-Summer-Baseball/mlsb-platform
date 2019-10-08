'''
@author: Dallas Fraser
@author: 2019-03-13
@organization: MLSB API
@summary: Tests all the advanced player team lookup APIs
'''
from datetime import date
from api.helper import loads
from api.routes import Routes
from base64 import b64encode
from api.test.advanced.mock_league import MockLeague
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


class TestPlayerTeamLookup(TestSetup):

    def testEmail(self):
        """Tests using a player email as a parameter"""
        mocker = MockLeague(self)
        league = mocker.get_league()
        team = mocker.get_teams()[0]
        player = mocker.get_players()[0]
        sponsor = mocker.get_sponsor()

        # test a test player emails
        params = {'email': mocker.get_player_email(0)}
        rv = self.app.post(Routes['vplayerteamLookup'], data=params)
        expect = [{'captain': player,
                   'color': team['color'],
                   'espys': 0,
                   'league_id': league['league_id'],
                   'sponsor_id': sponsor['sponsor_id'],
                   'team_id': team['team_id'],
                   'team_name': team['team_name'],
                   'year': team['year']}]
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect,
                         loads(rv.data),
                         Routes['vplayerteamLookup'])

    def testPlayerName(self):
        """Tests using a player name as a parameter"""
        mocker = MockLeague(self)
        league = mocker.get_league()
        team = mocker.get_teams()[0]
        player = mocker.get_players()[0]
        sponsor = mocker.get_sponsor()

        # test a test player names
        params = {'player_name': mocker.get_players()[0]['player_name']}
        rv = self.app.post(Routes['vplayerteamLookup'], data=params)
        expect = [{'captain': player,
                   'color': team['color'],
                   'espys': 0,
                   'league_id': league['league_id'],
                   'sponsor_id': sponsor['sponsor_id'],
                   'team_id': team['team_id'],
                   'team_name': team['team_name'],
                   'year': team['year']}]
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect,
                         loads(rv.data),
                         Routes['vplayerteamLookup'])

        # test a test player names
        player_two = mocker.get_players()[3]
        team_two = mocker.get_teams()[1]
        params = {'player_name': "Test Player"}
        rv = self.app.post(Routes['vplayerteamLookup'], data=params)
        expect = [{'captain': player,
                   'color': team['color'],
                   'espys': 0,
                   'league_id': league['league_id'],
                   'sponsor_id': sponsor['sponsor_id'],
                   'team_id': team['team_id'],
                   'team_name': team['team_name'],
                   'year': team['year']},
                  {'captain': player_two,
                   'color': team_two['color'],
                   'espys': 0,
                   'league_id': league['league_id'],
                   'sponsor_id': sponsor['sponsor_id'],
                   'team_id': team_two['team_id'],
                   'team_name': team_two['team_name'],
                   'year': team_two['year']}]
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect,
                         loads(rv.data),
                         Routes['vplayerteamLookup'])

    def testPlayerId(self):
        """Tests using a player id as a parameter"""
        mocker = MockLeague(self)
        league = mocker.get_league()
        team = mocker.get_teams()[0]
        player = mocker.get_players()[0]
        sponsor = mocker.get_sponsor()

        # test a test player names
        params = {'player_id': mocker.get_players()[0]['player_id']}
        rv = self.app.post(Routes['vplayerteamLookup'], data=params)
        expect = [{'captain': player,
                   'color': team['color'],
                   'espys': 0,
                   'league_id': league['league_id'],
                   'sponsor_id': sponsor['sponsor_id'],
                   'team_id': team['team_id'],
                   'team_name': team['team_name'],
                   'year': team['year']}]
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect,
                         loads(rv.data),
                         Routes['vplayerteamLookup'])
