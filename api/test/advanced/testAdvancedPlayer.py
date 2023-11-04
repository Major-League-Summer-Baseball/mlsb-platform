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


class PlayerTest(TestSetup):

    def testPostPlayerId(self):
        """Test player id parameter"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            mocker = MockLeague(self)

            # test an invalid player id
            rv = self.app.post(
                Routes['vplayer'], json={'player_id': INVALID_ID}
            )
            expect = {}
            self.output(expect)
            self.output(loads(rv.data))
            self.assertEqual(
                expect,
                loads(rv.data),
                Routes['vplayer'] + " Post: invalid player id"
            )

            # test an valid player id
            player = mocker.get_players()[0]
            player_id = player['player_id']
            rv = self.app.post(Routes['vplayer'], json={"player_id": player_id})
            expect = {
                player['player_name']: {
                    'avg': 0.5,
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
                    'ss': 0
                }
            }
            self.output(expect)
            self.output(loads(rv.data))
            self.assertEqual(
                expect,
                loads(rv.data),
                Routes['vplayer'] + " Post: valid player id"
            )

    def testPostYear(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            MockLeague(self)

            # test an invalid year
            rv = self.app.post(Routes['vplayer'], json={'year': INVALID_YEAR})
            expect = {}
            self.output(expect)
            self.output(loads(rv.data))
            self.assertEqual(
                expect,
                loads(rv.data),
                Routes['vplayer'] + " Post: invalid year"
            )

            # test an valid year
            rv = self.app.post(Routes['vplayer'], json={"year": VALID_YEAR})
            self.output(loads(rv.data))
            self.assertTrue(
                len(loads(rv.data).keys()) > 0,
                Routes['vplayer'] + " Post: valid year"
            )

    def testPostLeagueId(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            mocker = MockLeague(self)

            # test an invalid league id
            rv = self.app.post(
                Routes['vplayer'], json={'league_id': INVALID_ID}
            )
            expect = {}
            self.output(expect)
            self.output(loads(rv.data))
            self.assertEqual(
                expect,
                loads(rv.data),
                Routes['vplayer'] + " Post: invalid league id"
            )

            # test an valid league id
            league_id = mocker.get_league()['league_id']
            expect = {
                'avg': 0.5,
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
                'ss': 0
            }
            player_check = mocker.get_players()[0]
            rv = self.app.post(
                Routes['vplayer'], json={"league_id": league_id}
            )
            self.output(loads(rv.data))
            self.assertTrue(
                len(loads(rv.data).keys()) == 4,
                Routes['vplayer'] + " Post: valid league id"
            )
            self.assertEqual(
                loads(rv.data)[player_check['player_name']],
                expect,
                Routes['vplayer'] + " Post: valid league id"
            )

    def testPostTeamId(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            mocker = MockLeague(self)

            # test an invalid team id
            rv = self.app.post(Routes['vplayer'], json={'team_id': INVALID_ID})
            expect = {}
            self.output(expect)
            self.output(loads(rv.data))
            self.assertEqual(
                expect,
                loads(rv.data),
                Routes['vplayer'] + " Post: invalid team id"
            )

            # test an valid team id
            team_id = mocker.get_teams()[0]['team_id']
            expect = {
                'avg': 0.5,
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
                'ss': 0
            }
            player_check = mocker.get_players()[0]
            rv = self.app.post(Routes['vplayer'], json={"team_id": team_id})
            self.output(loads(rv.data))
            self.assertTrue(
                len(loads(rv.data).keys()) == 2,
                Routes['vplayer'] + " Post: valid team id"
            )
            self.assertEqual(
                loads(rv.data)[player_check['player_name']],
                expect,
                Routes['vplayer'] + " Post: valid team id"
            )
            absent_player_name = mocker.get_players()[2]['player_name']
            player_present = absent_player_name in loads(rv.data).keys()
            self.assertTrue(
                not player_present,
                Routes['vplayer'] + " Post: valid team id"
            )
