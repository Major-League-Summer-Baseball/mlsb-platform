from base64 import b64encode
from api.routes import Routes
from api.errors import InvalidField, LeagueEventDoesNotExist
from api.test.BaseTest import \
    TestSetup, ADMIN, PASSWORD, SUCCESSFUL_GET_CODE, \
    INVALID_ID, SUCCESSFUL_PUT_CODE


headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' +
                                                  PASSWORD, "utf-8")
                                            ).decode("ascii")
}
MISSING_PARAMETER = ('Missing required parameter in the JSON body ' +
                     'or the post body or the query string')


class TestLeagueEvent(TestSetup):

    def testLeagueEventInvalidPost(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # Note Valid Requests are tested in BaseTest method add_league_event
            # missing parameters
            params = {}
            result = {
                'message': {
                    'name': MISSING_PARAMETER,
                    'description': MISSING_PARAMETER

                }
            }
            error_message = (
                Routes['league_event'] +
                " POST: request with missing parameter"
            )
            self.postInvalidTest(
                Routes['league_event'],
                params,
                InvalidField.status_code,
                self.assertEqual,
                result,
                error_message=error_message
            )

            # testing invalid parameter types
            params = {'name': 1, 'description': '<p>Some description</p>'}
            result = {
                'details': 'League event - name',
                'message': InvalidField.message
            }
            error_message = (
                Routes['league_event'] + " POST: request with invalid name"
            )
            self.postInvalidTest(
                Routes['league_event'],
                params,
                InvalidField.status_code,
                self.assertEqual,
                result,
                error_message=error_message
            )

            params = {'name': 'Some name', 'description': 1}
            result = {
                'details': 'League event - description',
                'message': InvalidField.message
            }
            error_message = (
                Routes['league_event'] +
                " POST: request with invalid description"
            )
            self.postInvalidTest(
                Routes['league_event'],
                params,
                InvalidField.status_code,
                self.assertEqual,
                result,
                error_message=error_message
            )

    def testLeagueEventListAPI(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # proper insertion with post
            self.add_league_event("Some event", "<p>Some description</p>")

            # test a get with league events
            error_message = (
                Routes['league_event'] +
                " GET Failed to return list of league events"
            )
            self.getListTest(
                Routes['league_event'], error_message=error_message
            )

    def testLeagueEventAPIGet(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # add a league event
            league_event = self.add_league_event(
                "Some event",
                "<p>Some description</p>"
            )

            # invalid League event id
            expect = {
                'details': INVALID_ID,
                "message": LeagueEventDoesNotExist.message
            }
            error_message = (
                Routes['league_event'] +
                " Get: Invalid League Event"
            )
            self.getTest(
                Routes['league_event'] + "/" + str(INVALID_ID),
                LeagueEventDoesNotExist.status_code,
                self.assertEqual,
                expect,
                error_message=error_message
            )

            # valid League event id
            league_event_id = str(league_event['league_event_id'])
            route = Routes['league_event'] + "/" + league_event_id
            error_message = Routes['league_event'] + " Get: valid League Event"
            self.getTest(
                route,
                SUCCESSFUL_GET_CODE,
                self.assertLeagueEventModelEqual,
                league_event,
                error_message=error_message
            )

    def testLeagueEventAPIPut(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # add a league event
            league_event = self.add_league_event(
                "Some event",
                "<p>Some description</p>"
            )

            # invalid league id
            params = {'name': 'Updated event'}
            result = {
                'details': INVALID_ID,
                'message': LeagueEventDoesNotExist.message
            }
            error_message = (
                Routes['league_event'] + ' PUT:Invalid league event ID'
            )
            self.putTest(
                Routes['league_event'] + '/' + str(INVALID_ID),
                params,
                LeagueEventDoesNotExist.status_code,
                self.assertEqual,
                result,
                error_message=error_message
            )

            # invalid league_name type
            params = {'name': 1}
            result = {
                'details': 'League event - name',
                'message': InvalidField.message
            }
            error_message = Routes['league_event'] + ' PUT: Invalid parameters'
            league_event_id = str(league_event['league_event_id'])
            self.putTest(
                Routes['league_event'] + f'/{league_event_id}',
                params,
                InvalidField.status_code,
                self.assertEqual,
                result,
                error_message=error_message
            )

            # successfully update
            league_event['name'] = "Updated Event"
            params = {'name': league_event['name']}
            error_message = Routes['league_event'] + ' PUT: Successful Update'
            self.putTest(
                Routes['league_event'] + f'/{league_event_id}',
                params,
                SUCCESSFUL_PUT_CODE,
                self.assertEqual,
                None,
                error_message=error_message)

            league_event['description'] = "<p>Updated Descript</p>"
            params = {'description': league_event['description']}
            error_message = Routes['league_event'] + ' PUT: Successful Update'
            self.putTest(
                Routes['league_event'] + f'/{league_event_id}',
                params,
                SUCCESSFUL_PUT_CODE,
                self.assertEqual,
                None,
                error_message=error_message
            )

            # now get it
            error_message = Routes['league_event'] + " Get: valid League Event"
            self.getTest(
                Routes['league_event'] + f'/{league_event_id}',
                SUCCESSFUL_GET_CODE,
                self.assertLeagueEventModelEqual,
                league_event,
                error_message=error_message
            )
