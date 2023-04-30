'''
@author: Dallas Fraser
@date: 2019-03-13
@organization: MLSB API
@summary: Tests all the basic game APIS
'''
from api.helper import loads
from api.routes import Routes
from api.errors import \
    InvalidField, LeagueEventDoesNotExist,\
    LeagueEventDateDoesNotExist
from uuid import uuid1
from base64 import b64encode
from api.test.BaseTest import TestSetup, ADMIN, PASSWORD, SUCCESSFUL_GET_CODE,\
    INVALID_ID, SUCCESSFUL_PUT_CODE


headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' +
                                                  PASSWORD, "utf-8")
                                            ).decode("ascii")
}
MISSING_PARAMETER = ('Missing required parameter in the JSON body ' +
                     'or the post body or the query string')


class TestLeagueEventDate(TestSetup):

    def testLeagueEventDateInvalidPost(self):
        # Note Valid Requests are tested in
        # BaseTest method add_league_event_date
        # missing parameters
        self.show_results = True
        params = {}
        expect = {
            'message': {
                'league_event_id': MISSING_PARAMETER,
                'date': MISSING_PARAMETER,
                'time': MISSING_PARAMETER
            }
        }
        error_message = (Routes['league_event_date'] +
                         " POST: request with missing parameter")
        self.postInvalidTest(Routes['league_event_date'],
                             params,
                             InvalidField.status_code,
                             self.assertEqual,
                             expect,
                             error_message=error_message)

        # add a league event
        league_event = self.add_league_event(
            str(uuid1()),
            "<p>Some description</p>"
        )

        # testing invalid date
        params = {
            'league_event_id': league_event['league_event_id'],
            'date': "2014-02-2014",
            'time': "22:40"
        }
        expect = {
            'details': 'League Event Date - date',
            'message': InvalidField.message
        }
        error_message = (Routes['league_event_date'] +
                         " POST: request with invalid date")
        self.postInvalidTest(Routes['league_event_date'],
                             params,
                             InvalidField.status_code,
                             self.assertEqual,
                             expect,
                             error_message=error_message)

        # testing invalid time
        params = {
            'league_event_id': league_event['league_event_id'],
            'date': "2014-02-02",
            'time': "22:66"
        }
        expect = {
            'details': 'League Event Date - time',
            'message': InvalidField.message
        }
        error_message = (Routes['league_event_date'] +
                         " POST: request with invalid time")
        self.postInvalidTest(Routes['league_event_date'],
                             params,
                             InvalidField.status_code,
                             self.assertEqual,
                             expect,
                             error_message=error_message)

        # testing invalid league event id
        params = {
            'league_event_id': INVALID_ID,
            'date': "2014-02-10",
            'time': "22:40"
        }
        expect = {
            'details': INVALID_ID,
            'message': LeagueEventDoesNotExist.message
        }
        error_message = (Routes['league_event_date'] +
                         " POST: request with invalid league event id")
        self.postInvalidTest(Routes['league_event_date'],
                             params,
                             LeagueEventDoesNotExist.status_code,
                             self.assertEqual,
                             expect,
                             error_message=error_message)

    def testLeagueEventDateListAPI(self):
        # add league event
        league_event = self.add_league_event(
            str(uuid1()),
            "<p>Some description</p>"
        )

        # add a league event date
        self.add_league_event_date(league_event, "2014-02-10", "22:40")

        # test a get
        error_message = (Routes['league_event_date'] +
                         " GET Failed to return list of League Event Dates")
        self.getListTest(
            Routes['league_event_date'],
            error_message=error_message
        )

    def testLeagueEventDateGet(self):
        # add league event date
        route = Routes['league_event_date']
        league_event = self.add_league_event(
            str(uuid1()),
            "<p>Some description</p>"
        )
        league_event_date = self.add_league_event_date(
            league_event,
            "2014-02-10",
            "22:40"
        )

        # invalid id
        expect = {
            'details': INVALID_ID,
            "message": LeagueEventDateDoesNotExist.message
        }
        self.getTest(
            f"{route}/{INVALID_ID}",
            LeagueEventDateDoesNotExist.status_code,
            self.assertEqual,
            expect,
            error_message=f"{route} Get: Invalid League Event Date"
        )

        # valid id
        self.getTest(
            f"{route}/{league_event_date['league_event_date_id']}",
            SUCCESSFUL_GET_CODE,
            self.assertLeagueEventDateModelEqual,
            league_event_date,
            error_message=f"{route} Get: valid League Event Date"
        )

    def testLeagueEventDateDelete(self):
        # delete invalid id
        route = Routes['league_event_date']
        rv = self.app.delete(f"{route}/{INVALID_ID}", headers=headers)
        expect = {
            'details': INVALID_ID,
            'message': LeagueEventDateDoesNotExist.message
        }
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(
            loads(rv.data),
            expect,
            f"{route} DELETE: on invalid game id"
        )
        self.assertEqual(
            rv.status_code,
            LeagueEventDateDoesNotExist.status_code,
            f"{route} DELETE: on invalid game id"
        )

        # add a league event date
        league_event = self.add_league_event(
            str(uuid1()),
            "<p>Some description</p>"
        )
        league_event_date = self.add_league_event_date(
            league_event,
            "2014-02-10",
            "22:40"
        )

        # delete valid game id
        rv = self.app.delete(
            f"{route}/{league_event_date['league_event_date_id']}",
            headers=headers
        )
        expect = None
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(
            loads(rv.data),
            expect,
            f"{route} DELETE: on valid game id"
        )
        self.assertEqual(
            rv.status_code,
            200,
            f"{route} DELETE: on valid game id"
        )

    def testLeagueEventDatePut(self):
        route = Routes['league_event_date']

        # add a league event
        league_event = self.add_league_event(
            str(uuid1()),
            "<p>Some description</p>"
        )
        second_league_event = self.add_league_event(
            str(uuid1()),
            "<p>Some description</p>"
        )
        league_event_date = self.add_league_event_date(
            league_event,
            "2014-02-10",
            "22:40"
        )
        invalid_route = f"{route}/{INVALID_ID}"
        valid_route = f"{route}/{league_event_date['league_event_date_id']}"

        # invalid id
        params = {
            'date': "2014-08-22",
            'time': "11:37",
            'league_event_id': league_event['league_event_id']
        }
        expect = {
            'details': INVALID_ID,
            'message': LeagueEventDateDoesNotExist.message}
        error_message = f"{route} PUT: invalid game id"
        self.putTest(invalid_route,
                     params,
                     LeagueEventDateDoesNotExist.status_code,
                     self.assertEqual,
                     expect,
                     error_message=error_message)

        # invalid league event id
        params = {
            'date': "2014-08-22",
            'time': "11:37",
            'league_event_id': INVALID_ID
        }
        expect = {
            'details': INVALID_ID,
            'message': LeagueEventDoesNotExist.message
        }
        error_message = f"{route} PUT: invalid league event id"
        self.putTest(valid_route,
                     params,
                     LeagueEventDoesNotExist.status_code,
                     self.assertEqual,
                     expect,
                     error_message=error_message)

        # invalid date
        params = {
            'date': "xx-08-22",
            'time': "11:37",
            'league_event_id': league_event['league_event_id']
        }
        expect = {
            'details': 'League Event Date - date',
            'message': InvalidField.message
        }
        error_message = f"{route} PUT: invalid date"
        self.putTest(valid_route,
                     params,
                     InvalidField.status_code,
                     self.assertEqual,
                     expect,
                     error_message=error_message)

        # invalid time
        params = {
            'date': "2014-08-22",
            'time': "XX:37",
            'league_event_id': league_event['league_event_id']
        }
        expect = {
            'details': 'League Event Date - time',
            'message': InvalidField.message
        }
        error_message = f"{route} PUT: invalid time"
        self.putTest(valid_route,
                     params,
                     InvalidField.status_code,
                     self.assertEqual,
                     expect,
                     error_message=error_message)

        # valid update parameters
        params = {
            'date': "2014-08-22",
            'time': "11:37",
            'league_event_id': second_league_event['league_event_id']
        }
        league_event_date['date'] = params['date']
        league_event_date['time'] = params['time']
        league_event_date['league_event_id'] = params['league_event_id']
        self.putTest(valid_route,
                     params,
                     SUCCESSFUL_PUT_CODE,
                     self.assertEqual,
                     None,
                     error_message=f"{route} PUT: valid update")

        # test a valid get
        error_message = f"{route} GET: just updated league event date"
        self.getTest(valid_route,
                     SUCCESSFUL_GET_CODE,
                     self.assertLeagueEventDateModelEqual,
                     league_event_date,
                     error_message=error_message)
