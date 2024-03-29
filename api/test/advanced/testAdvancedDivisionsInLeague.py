from datetime import date
from base64 import b64encode
from api.helper import loads
from api.routes import Routes
from api.errors import LeagueDoesNotExist
from api.test.advanced.mock_league import MockLeague
from api.test.BaseTest import TestSetup, ADMIN, PASSWORD, INVALID_ID
headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' +
                                                  PASSWORD, "utf-8")
                                            ).decode("ascii")
}
VALID_YEAR = date.today().year
INVALID_YEAR = 100

MAIN_ROUTE = Routes['vdivisions']


class TestDivisionInLeague(TestSetup):
    def testGetLeagueDoesNotExists(self):
        """Test a get request for a league that does not exist"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            rv = self.app.get(f"{MAIN_ROUTE}/{VALID_YEAR}/{INVALID_ID}")
            expect = {
                'details': INVALID_ID, 'message': LeagueDoesNotExist.message
            }
            self.output(loads(rv.data))
            self.output(expect)
            self.assertEqual(
                loads(rv.data), expect, f"{MAIN_ROUTE}: GET league that Dne"
            )
            self.assertEqual(
                LeagueDoesNotExist.status_code,
                rv.status_code,
                f"{MAIN_ROUTE}: GET league that Dne"
            )

    def testGetLeagueDoesExistsNoGames(self):
        """Test a get request for a league that exist but invalid year"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            mocker = MockLeague(self)
            league = mocker.get_league()
            league_id = league['league_id']
            result = self.app.get(f"{MAIN_ROUTE}/{INVALID_YEAR}/{league_id}")
            expect = []
            self.output(loads(result.data))
            self.output(expect)
            self.assertEqual(
                expect,
                loads(result.data),
                f"{MAIN_ROUTE}: GET league that exists but no games"
            )

    def testGetLeagueExists(self):
        """Test a get request for a league that exists"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            mocker = MockLeague(self)
            league = mocker.get_league()
            league_id = league['league_id']
            result = self.app.get(f"{MAIN_ROUTE}/{VALID_YEAR}/{league_id}")
            expect = [mocker.get_division()]
            self.output(loads(result.data))
            self.output(expect)
            self.assertEqual(
                expect, loads(result.data),
                f"{MAIN_ROUTE}: GET league that exists but no games"
            )
