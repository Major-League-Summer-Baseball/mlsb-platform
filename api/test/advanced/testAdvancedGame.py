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


class GameTest(TestSetup):

    def testPostYear(self):
        """Test the year parameter"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # test an invalid year
            MockLeague(self)
            rv = self.app.post(Routes['vgame'], json={"year": INVALID_YEAR})
            expect = []
            self.output(loads(rv.data))
            self.output(expect)
            self.assertEqual(
                expect,
                loads(rv.data),
                Routes['vgame'] + " Post: invalid year"
            )

            # test a valid year
            rv = self.app.post(Routes['vgame'], json={"year": VALID_YEAR})
            expect = 3
            self.output(loads(rv.data))
            self.output(expect)
            self.assertTrue(
                len(loads(rv.data)) > 0,
                Routes['vgame'] + " Post: valid year"
            )

    def testPostLeagueId(self):
        """Test league id parameter"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # test an invalid league id
            mocker = MockLeague(self)
            rv = self.app.post(Routes['vgame'], json={"league_id": INVALID_ID})
            expect = []
            self.output(loads(rv.data))
            self.output(expect)
            self.assertEqual(
                expect,
                loads(rv.data),
                Routes['vgame'] + " Post: invalid league id"
            )

            # test a valid league id
            data = {"league_id": mocker.get_league()['league_id']}
            rv = self.app.post(Routes['vgame'], json=data)
            expect = 3
            self.output(loads(rv.data))
            self.output(expect)
            self.assertEqual(
                expect,
                len(loads(rv.data)),
                Routes['vgame'] + " Post: valid league id"
            )

    def testPostGameId(self):
        """Test game id parameter"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # test an invalid league id
            mocker = MockLeague(self)
            rv = self.app.post(Routes['vgame'], json={"game_id": INVALID_ID})
            expect = []
            self.output(loads(rv.data))
            self.output(expect)
            self.assertEqual(
                expect,
                loads(rv.data),
                Routes['vgame'] + " Post: invalid game id"
            )

            # test a valid league id
            data = {"game_id": mocker.get_games()[0]['game_id']}
            rv = self.app.post(Routes['vgame'], json=data)
            games_data = loads(rv.data)
            game_data = games_data[0]
            expect = 1
            self.output(loads(rv.data))
            self.output(expect)
            self.assertEqual(expect, len(games_data))
            self.assertEqual(6, game_data['away_score'])
            self.assertEqual(4, len(game_data['away_bats']))
            self.assertEqual(1, game_data['home_score'])
            self.assertEqual(4, len(game_data['home_bats']))
            self.assertLeagueModelEqual(
                mocker.get_league(), game_data['league']
            )
