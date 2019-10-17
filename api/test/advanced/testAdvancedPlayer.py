'''
@author: Dallas Fraser
@author: 2019-03-13
@organization: MLSB API
@summary: Tests all the advanced player APIs
'''
from datetime import date
from api.helper import loads
from api.routes import Routes
from base64 import b64encode
from api.test.advanced.mock_league import MockLeague
from api.test.BaseTest import TestSetup, ADMIN, PASSWORD, KIK, KIKPW,\
    INVALID_ID

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


class PlayerTest(TestSetup):

    def testPostPlayerId(self):
        """Test player id parameter"""
        mocker = MockLeague(self)

        # test an invalid player id
        rv = self.app.post(Routes['vplayer'], data={'player_id': INVALID_ID})
        expect = {}
        self.output(expect)
        self.output(loads(rv.data))
        self.assertEqual(expect,
                         loads(rv.data),
                         Routes['vplayer'] + " Post: invalid player id")

        # test an valid player id
        player_id = mocker.get_players()[0]['player_id']
        rv = self.app.post(Routes['vplayer'], data={"player_id": player_id})
        expect = {'Test Player 1': {'avg': 0.5,
                                    'bats': 2,
                                    'd': 0,
                                    'e': 0,
                                    'fc': 0,
                                    'fo': 0,
                                    'go': 0,
                                    'hr': 1,
                                    'id': player_id,
                                    'k': 1,
                                    'rbi': 2,
                                    's': 0,
                                    'ss': 0}}
        self.output(expect)
        self.output(loads(rv.data))
        self.assertEqual(expect,
                         loads(rv.data),
                         Routes['vplayer'] + " Post: valid player id")

    def testPostYear(self):
        MockLeague(self)

        # test an invalid year
        rv = self.app.post(Routes['vplayer'], data={'year': INVALID_YEAR})
        expect = {}
        self.output(expect)
        self.output(loads(rv.data))
        self.assertEqual(expect,
                         loads(rv.data),
                         Routes['vplayer'] + " Post: invalid year")

        # test an valid year
        rv = self.app.post(Routes['vplayer'], data={"year": VALID_YEAR})
        self.output(loads(rv.data))
        self.assertTrue(len(loads(rv.data).keys()) > 0,
                        Routes['vplayer'] + " Post: valid year")

    def testPostLeagueId(self):
        mocker = MockLeague(self)

        # test an invalid league id
        rv = self.app.post(Routes['vplayer'], data={'league_id': INVALID_ID})
        expect = {}
        self.output(expect)
        self.output(loads(rv.data))
        self.assertEqual(expect,
                         loads(rv.data),
                         Routes['vplayer'] + " Post: invalid league id")

        # test an valid league id
        league_id = mocker.get_league()['league_id']
        expect = {'avg': 0.5,
                  'bats': 2,
                  'd': 0,
                  'e': 0,
                  'fc': 0,
                  'fo': 0,
                  'go': 0,
                  'hr': 1,
                  'id': mocker.get_players()[0]['player_id'],
                  'k': 1,
                  'rbi': 2,
                  's': 0,
                  'ss': 0}
        player_check = mocker.get_players()[0]
        rv = self.app.post(Routes['vplayer'], data={"league_id": league_id})
        self.output(loads(rv.data))
        self.assertTrue(len(loads(rv.data).keys()) == 4,
                        Routes['vplayer'] + " Post: valid league id")
        self.assertEqual(loads(rv.data)[player_check['player_name']],
                         expect,
                         Routes['vplayer'] + " Post: valid league id")

    def testPostTeamId(self):
        mocker = MockLeague(self)

        # test an invalid team id
        rv = self.app.post(Routes['vplayer'], data={'team_id': INVALID_ID})
        expect = {}
        self.output(expect)
        self.output(loads(rv.data))
        self.assertEqual(expect,
                         loads(rv.data),
                         Routes['vplayer'] + " Post: invalid team id")

        # test an valid team id
        team_id = mocker.get_teams()[0]['team_id']
        expect = {'avg': 0.5,
                  'bats': 2,
                  'd': 0,
                  'e': 0,
                  'fc': 0,
                  'fo': 0,
                  'go': 0,
                  'hr': 1,
                  'id': mocker.get_players()[0]['player_id'],
                  'k': 1,
                  'rbi': 2,
                  's': 0,
                  'ss': 0}
        player_check = mocker.get_players()[0]
        rv = self.app.post(Routes['vplayer'], data={"team_id": team_id})
        self.output(loads(rv.data))
        self.assertTrue(len(loads(rv.data).keys()) == 2,
                        Routes['vplayer'] + " Post: valid team id")
        self.assertEqual(loads(rv.data)[player_check['player_name']],
                         expect,
                         Routes['vplayer'] + " Post: valid team id")
        absent_player_name = mocker.get_players()[2]['player_name']
        player_present = absent_player_name in loads(rv.data).keys()
        self.assertTrue(not player_present,
                        Routes['vplayer'] + " Post: valid team id")
