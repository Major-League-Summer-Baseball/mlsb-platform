'''
@author: Dallas Fraser
@author: 2019-03-13
@organization: MLSB API
@summary: Tests all the advanced league leader APIs
'''
from datetime import date
from api.helper import loads
from api.routes import Routes
from base64 import b64encode
from api.test.advanced.mock_league import MockLeague
from api.test.BaseTest import TestSetup, ADMIN, PASSWORD
from api.errors import InvalidField
headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' +
                                                  PASSWORD, "utf-8")
                                            ).decode("ascii")
}
VALID_YEAR = date.today().year
INVALID_YEAR = 100


class TestLeagueLeaders(TestSetup):

    def testInvalidtStat(self):
        """Test a stat that is not valid"""
        MockLeague(self)
        params = {'stat': "XXX"}
        rv = self.app.post(Routes['vleagueleaders'], json=params)
        expect = {}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, InvalidField.status_code,
                         Routes['vleagueleaders'] +
                         " View: invalid stat accepted")

    def testNonEmptyStat(self):
        """Test a stat that is not empty"""
        MockLeague(self)
        params = {'stat': "hr"}
        rv = self.app.post(Routes['vleagueleaders'], json=params)
        self.output(loads(rv.data))
        self.assertTrue(len(loads(rv.data)) > 0, Routes['vleagueleaders'] +
                        " View: hr stat was empty for all years")

    def testEmptyYear(self):
        """Test an empty year"""
        MockLeague(self)
        params = {'stat': "hr", 'year': INVALID_YEAR}
        rv = self.app.post(Routes['vleagueleaders'], json=params)
        expect = []
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['vleagueleaders'] +
                         " View: empty stat on not-recording year")

    def testNonEmptyYear(self):
        """Test a non-empty year"""
        MockLeague(self)
        params = {'stat': "k", 'year': VALID_YEAR}
        rv = self.app.post(Routes['vleagueleaders'], json=params)
        self.output(loads(rv.data))
        self.assertTrue(len(loads(rv.data)) > 0, Routes['vleagueleaders'] +
                        " View: hr stat was empty")

    def testGroupByTeam(self):
        """Test a non-empty year"""
        MockLeague(self)
        params = {'stat': "hr", 'year': VALID_YEAR}
        not_grouped = self.app.post(Routes['vleagueleaders'], json=params)
        params = {'stat': "hr", 'year': VALID_YEAR, 'group_by_team': 0}
        grouped = self.app.post(Routes['vleagueleaders'], json=params)
        self.output(loads(not_grouped.data))
        self.output(loads(grouped.data))
        self.assertFalse(loads(not_grouped.data) == loads(grouped.data),
                         Routes['vleagueleaders'] +
                         " View: group same as not grouped")
        for entry in loads(grouped.data):
            self.assertTrue(entry['team_id'] is None,
                            Routes['vleagueleaders'] +
                            " View: group by team, team should be None")
            self.assertTrue(entry['team'] is None,
                            Routes['vleagueleaders'] +
                            " View: group by team, team should be None")
