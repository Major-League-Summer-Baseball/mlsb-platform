from api.helper import loads
from api.routes import Routes
from api.errors import LeagueDoesNotExist
from api.test.BaseTest import TestSetup, INVALID_ID
from api.test.advanced.mock_league import MockLeague
import datetime


class TestSchedule(TestSetup):

    def testEmptyYear(self):
        """Test schedule view for empty league"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            league_id = MockLeague(self).league['league_id']
            rv = self.app.get(f"{Routes['vschedule']}/2012/{league_id}")
            expect = []
            self.output(loads(rv.data))
            self.output(expect)
            self.assertEqual(
                expect,
                loads(rv.data)['items'],
                Routes['vschedule'] + "View: on 2012 year"
            )

    def testLeagueDoesNotExist(self):
        """Test schedule view for empty league"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            url = Routes['vschedule'] + "/2012" + "/" + str(INVALID_ID)
            rv = self.app.get(url)
            self.output(rv.status_code)
            self.output(LeagueDoesNotExist.status_code)
            self.assertEqual(
                rv.status_code,
                LeagueDoesNotExist.status_code,
                Routes['vschedule'] + "View: on invalid league"
            )

    def testMockLeague(self):
        """Test schedule view for mocked league"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            league_id = MockLeague(self).league['league_id']
            year = datetime.datetime.now().year
            url = Routes['vschedule'] + "/" + str(year) + "/" + str(league_id)
            rv = self.app.get(url)
            game = {
                'away_team': 'Advanced Test Sponsor Test Team 2',
                'home_team': 'Advanced Test Sponsor Test Team',
                'score': '1-6'
            }
            expect = ["1-6", "0-0", ""]
            self.output(loads(rv.data))
            self.output(expect)
            for index, game in enumerate(loads(rv.data)['items']):
                self.assertEqual(expect[index], game['score'])
