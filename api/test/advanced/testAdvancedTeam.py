from datetime import date
from base64 import b64encode
from api.helper import loads
from api.routes import Routes
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
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            mocker = MockLeague(self)

            # invalid team id
            rv = self.app.post(Routes['vteam'], json={'team_id': INVALID_ID})
            expect = {}
            self.output(loads(rv.data))
            self.output(expect)
            self.assertEqual(
                expect,
                loads(rv.data),
                Routes['vteam'] + " Post: invalid team id"
            )

            # valid team id
            team = mocker.get_teams()[0]
            team_id = team['team_id']
            rv = self.app.post(Routes['vteam'], json={'team_id': team_id})
            expect = {
                'games': 3,
                'hits_allowed': 3,
                'hits_for': 2,
                'losses': 1,
                'name': team['team_name'],
                'team_name': team['team_name'],
                'runs_against': 6,
                'runs_for': 1,
                'ties': 1,  # today maybe considered a tie or not
                'wins': 0,
                'espys': 0
            }
            self.output(loads(rv.data))
            self.output(expect)
            self.assertTrue(
                len(loads(rv.data).keys()) == 1,
                Routes['vteam'] + " Post: valid team id"
            )
            data = loads(rv.data)[str(team_id)]
            self.assertEqual(expect['espys'], data['espys'])
            self.assertEqual(expect['runs_for'], data['runs_for'])
            self.assertEqual(expect['runs_against'], data['runs_against'])
            self.assertEqual(expect['wins'], data['wins'])
            self.assertEqual(expect['losses'], data['losses'])

    def testPostYear(self):
        """Test year parameter"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            mocker = MockLeague(self)

            # invalid year
            rv = self.app.post(Routes['vteam'], json={'year': INVALID_YEAR})
            expect = {}
            self.output(loads(rv.data))
            self.output(expect)
            self.assertEqual(
                expect,
                loads(rv.data),
                Routes['vteam'] + " Post: invalid year"
            )

            # valid year
            team = mocker.get_teams()[0]
            team_id = team['team_id']
            rv = self.app.post(Routes['vteam'], json={'year': VALID_YEAR})
            expect = {
                'games': 1,
                'hits_allowed': 3,
                'hits_for': 2,
                'losses': 1,
                'name': team['team_name'],
                'team_name': team['team_name'],
                'runs_against': 6,
                'runs_for': 1,
                'ties': 1,
                'wins': 0,
                'espys': 0
            }
            self.output(loads(rv.data))
            self.output(expect)
            self.assertTrue(
                len(loads(rv.data).keys()) > 0,
                Routes['vteam'] + " Post: valid year"
            )
            data = loads(rv.data)[str(team_id)]
            self.assertEqual(expect['espys'], data['espys'])
            self.assertEqual(expect['runs_for'], data['runs_for'])
            self.assertEqual(expect['runs_against'], data['runs_against'])
            self.assertEqual(expect['wins'], data['wins'])
            self.assertEqual(expect['losses'], data['losses'])
            self.assertEqual(expect['ties'], data['ties'])

    def testLeagueId(self):
        """Test league id parameter"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            mocker = MockLeague(self)

            # invalid league id
            rv = self.app.post(Routes['vteam'], json={'league_id': INVALID_ID})
            expect = {}
            self.output(loads(rv.data))
            self.output(expect)
            self.assertEqual(
                expect,
                loads(rv.data),
                Routes['vteam'] + " Post: invalid league id"
            )

            # valid league id
            league_id = mocker.get_league()['league_id']
            team = mocker.get_teams()[0]
            team_id = team['team_id']
            rv = self.app.post(Routes['vteam'], json={'league_id': league_id})
            expect = {
                'games': 1,
                'hits_allowed': 3,
                'hits_for': 2,
                'losses': 1,
                'name': team['team_name'],
                'team_name': team['team_name'],
                'runs_against': 6,
                'runs_for': 1,
                'ties': 1,
                'wins': 0,
                'espys': 0
            }
            self.output(loads(rv.data))
            self.output(expect)
            self.assertTrue(
                len(loads(rv.data).keys()) > 0,
                Routes['vteam'] + " Post: valid year"
            )
            data = loads(rv.data)[str(team_id)]
            self.assertEqual(expect['espys'], data['espys'])
            self.assertEqual(expect['runs_for'], data['runs_for'])
            self.assertEqual(expect['runs_against'], data['runs_against'])
            self.assertEqual(expect['wins'], data['wins'])
            self.assertEqual(expect['losses'], data['losses'])
            self.assertEqual(expect['ties'], data['ties'])

    def testEspysParameter(self):
        """Test that the espys are properly being calculated"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            mocker = MockLeague(self)

            # add an espys to the team
            self.add_espys(
                mocker.get_teams()[0], mocker.get_sponsor(), points=1
            )

            # valid league id
            league_id = mocker.get_league()['league_id']
            team = mocker.get_teams()[0]
            team_id = team['team_id']
            rv = self.app.post(Routes['vteam'], json={'league_id': league_id})
            expect = {
                'games': 1,
                'hits_allowed': 3,
                'hits_for': 2,
                'losses': 1,
                'name': team['team_name'],
                'team_name': team['team_name'],
                'runs_against': 6,
                'runs_for': 1,
                'ties': 1,
                'wins': 0,
                'espys': 1
            }
            self.output(loads(rv.data))
            self.output(expect)
            self.assertTrue(
                len(loads(rv.data).keys()) > 0,
                Routes['vteam'] + " Post: valid year"
            )
            data = loads(rv.data)[str(team_id)]
            self.assertEqual(expect['espys'], data['espys'])
            self.assertEqual(expect['runs_for'], data['runs_for'])
            self.assertEqual(expect['runs_against'], data['runs_against'])
            self.assertEqual(expect['wins'], data['wins'])
            self.assertEqual(expect['losses'], data['losses'])
            self.assertEqual(expect['ties'], data['ties'])
