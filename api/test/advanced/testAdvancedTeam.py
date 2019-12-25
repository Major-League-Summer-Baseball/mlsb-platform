'''
@author: Dallas Fraser
@author: 2019-03-13
@organization: MLSB API
@summary: Tests all the advanced team APIs
'''
from datetime import date
from api.helper import loads
from api.routes import Routes
from base64 import b64encode
from api.test.advanced.mock_league import MockLeague
from api.test.BaseTest import TestSetup, ADMIN, PASSWORD, INVALID_ID

headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' +
                                                  PASSWORD, "utf-8")
                                            ).decode("ascii")
}
VALID_YEAR = date.today().year
INVALID_YEAR = 100


class TeamTest(TestSetup):

    def testPostTeamId(self):
        """Test team id parameter"""
        mocker = MockLeague(self)

        # invalid team id
        rv = self.app.post(Routes['vteam'], data={'team_id': INVALID_ID})
        expect = {}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['vteam'] + " Post: invalid team id")

        # valid team id
        team = mocker.get_teams()[0]
        team_id = team['team_id']
        rv = self.app.post(Routes['vteam'], data={'team_id': team_id})
        expect = {'games': 3,
                  'hits_allowed': 3,
                  'hits_for': 2,
                  'losses': 1,
                  'name': team['team_name'],
                  'runs_against': 6,
                  'runs_for': 1,
                  'ties': 0,
                  'wins': 0}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertTrue(len(loads(rv.data).keys()) == 1,
                        Routes['vteam'] + " Post: valid team id")
        self.assertEqual(expect, loads(rv.data)[str(team_id)],
                         Routes['vteam'] + " Post: valid team id")

    def testPostYear(self):
        """Test year parameter"""
        mocker = MockLeague(self)

        # invalid year
        rv = self.app.post(Routes['vteam'], data={'year': INVALID_YEAR})
        expect = {}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['vteam'] + " Post: invalid year")

        # valid year
        team = mocker.get_teams()[0]
        team_id = team['team_id']
        rv = self.app.post(Routes['vteam'], data={'year': VALID_YEAR})
        expect = {'games': 1,
                  'hits_allowed': 3,
                  'hits_for': 2,
                  'losses': 1,
                  'name': team['team_name'],
                  'runs_against': 6,
                  'runs_for': 1,
                  'ties': 0,
                  'wins': 0}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertTrue(len(loads(rv.data).keys()) > 0,
                        Routes['vteam'] + " Post: valid year")
        self.assertEqual(expect,
                         loads(rv.data)[str(team_id)],
                         Routes['vteam'] + " Post: valid year")

    def testLeagueId(self):
        """Test league id parameter"""
        mocker = MockLeague(self)

        # invalid league id
        rv = self.app.post(Routes['vteam'], data={'league_id': INVALID_ID})
        expect = {}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['vteam'] + " Post: invalid league id")

        # valid league id
        league_id = mocker.get_league()['league_id']
        team = mocker.get_teams()[0]
        team_id = team['team_id']
        rv = self.app.post(Routes['vteam'], data={'league_id': league_id})
        expect = {'games': 1,
                  'hits_allowed': 3,
                  'hits_for': 2,
                  'losses': 1,
                  'name': team['team_name'],
                  'runs_against': 6,
                  'runs_for': 1,
                  'ties': 0,
                  'wins': 0}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertTrue(len(loads(rv.data).keys()) > 0,
                        Routes['vteam'] + " Post: valid year")
        self.assertEqual(expect,
                         loads(rv.data)[str(team_id)],
                         Routes['vteam'] + " Post: valid year")
