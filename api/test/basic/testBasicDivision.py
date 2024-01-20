from base64 import b64encode
from api.routes import Routes
from api.errors import InvalidField, DivisionDoesNotExist
from api.test.BaseTest import \
    TestSetup, ADMIN, PASSWORD, SUCCESSFUL_GET_CODE, \
    INVALID_ID, SUCCESSFUL_PUT_CODE
from uuid import uuid1 as random_string


headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' +
                                                  PASSWORD, "utf-8")
                                            ).decode("ascii")
}
MISSING_PARAMETER = ('Missing required parameter in the JSON body ' +
                     'or the post body or the query string')


class TestDivision(TestSetup):

    def testDivisionInvalidPost(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # Note Valid Requests are tested in BaseTest method add_Division
            # missing parameters
            params = {}
            result = {
                'message': {
                    'division_name': MISSING_PARAMETER
                }
            }
            error_message = (
                Routes['division'] + " POST: request with missing parameter"
            )
            self.postInvalidTest(
                Routes['division'],
                params,
                InvalidField.status_code,
                self.assertEqual,
                result,
                error_message=error_message
            )

            # testing a Division name parameter
            params = {'division_name': 1}
            result = {
                'details': 'Division - name',
                'message': InvalidField.message
            }
            error_message = (
                Routes['division'] + " POST: request with invalid division_name"
            )
            self.postInvalidTest(
                Routes['division'],
                params,
                InvalidField.status_code,
                self.assertEqual,
                result,
                error_message=error_message
            )

            # division invalid short name
            params = {
                'division_name': str(random_string()),
                'division_shortname': 1
            }
            result = {
                'details': 'Division - shortname',
                'message': InvalidField.message
            }
            error_message = (
                Routes['division'] +
                " POST: request with invalid division_shortname"
            )
            self.postInvalidTest(
                Routes['division'],
                params,
                InvalidField.status_code,
                self.assertEqual,
                result,
                error_message=error_message
            )

    def testDivisionListAPI(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # proper insertion with post
            self.add_division(str(random_string()))

            # test a get with Divisions
            error_message = (
                Routes['division'] +
                " GET Failed to return list of Divisions"
            )
            self.getListTest(Routes['division'], error_message=error_message)

    def testDivisionAPIGet(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # add a Division
            division = self.add_division(str(random_string()))

            # invalid Division id
            expect = {
                'details': INVALID_ID,
                "message": DivisionDoesNotExist.message
            }
            error_message = Routes['division'] + " Get: Invalid division"
            self.getTest(
                Routes['division'] + "/" + str(INVALID_ID),
                DivisionDoesNotExist.status_code,
                self.assertEqual,
                expect,
                error_message=error_message
            )

            # valid Division id
            self.getTest(
                Routes['division'] + "/" + str(division['division_id']),
                SUCCESSFUL_GET_CODE,
                self.assertDivisionModelEqual,
                division,
                error_message=Routes['division'] + " Get: valid Division"
            )

    def testDivisionAPIPut(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # add a Division
            division = self.add_division(str(random_string()))

            # invalid Division id
            params = {'division_name': str(random_string())}
            result = {
                'details': INVALID_ID,
                'message': DivisionDoesNotExist.message
            }
            error_message = Routes['division'] + ' PUT:Invalid division ID'
            self.putTest(
                Routes['division'] + '/' + str(INVALID_ID),
                params,
                DivisionDoesNotExist.status_code,
                self.assertEqual,
                result,
                error_message=error_message
            )

            # invalid Division_name type
            params = {'division_name': 1}
            result = {
                'details': 'Division - name',
                'message': InvalidField.message
            }
            error_message = Routes['division'] + ' PUT: Invalid parameters'
            self.putTest(
                Routes['division'] + '/' + str(division['division_id']),
                params,
                InvalidField.status_code,
                self.assertEqual,
                result,
                error_message=error_message
            )

            params = {'division_shortname': 1}
            result = {
                'details': 'Division - shortname',
                'message': InvalidField.message
            }
            error_message = Routes['division'] + ' PUT: Invalid parameters'
            self.putTest(
                Routes['division'] + '/' + str(division['division_id']),
                params,
                InvalidField.status_code,
                self.assertEqual,
                result,
                error_message=error_message
            )

            # successfully update
            division['division_name'] = str(random_string())
            params = {'division_name': division['division_name']}
            error_message = Routes['division'] + ' PUT: Successful Update'
            self.putTest(
                Routes['division'] + '/' + str(division['division_id']),
                params,
                SUCCESSFUL_PUT_CODE,
                self.assertEqual,
                None,
                error_message=error_message
            )

            # successfully update the shortname
            division['division_shortname'] = str(random_string())
            params = {'division_shortname': division['division_shortname']}
            error_message = Routes['division'] + ' PUT: Successful Update'
            self.putTest(
                Routes['division'] + '/' + str(division['division_id']),
                params,
                SUCCESSFUL_PUT_CODE,
                self.assertEqual,
                None,
                error_message=error_message
            )

            # now get it
            self.getTest(
                Routes['division'] + "/" + str(division['division_id']),
                SUCCESSFUL_GET_CODE,
                self.assertDivisionModelEqual,
                division,
                error_message=Routes['fun'] + " Get: valid Division"
            )
