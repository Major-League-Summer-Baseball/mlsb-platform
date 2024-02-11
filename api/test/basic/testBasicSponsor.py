from base64 import b64encode
from api.routes import Routes
from api.errors import SponsorDoesNotExist, InvalidField
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


class TestSponsor(TestSetup):

    def testSponsorInvalidPost(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # Note Valid Requests are tested in BaseTest method add_sponsor
            # missing parameters
            params = {}
            result = {'message': {'sponsor_name': MISSING_PARAMETER}}
            error_message = (
                Routes['sponsor'] + " POST: request with missing parameter"
            )
            self.postInvalidTest(
                Routes['sponsor'],
                params,
                InvalidField.status_code,
                self.assertEqual,
                result,
                error_message=error_message
            )

            # testing with improper name parameters
            params = {'sponsor_name': 1}
            result = {
                'details': 'Sponsor - name', 'message': InvalidField.message
            }
            error_message = (
                Routes['sponsor'] + " POST: request with invalid parameters"
            )
            self.postInvalidTest(
                Routes['sponsor'],
                params,
                InvalidField.status_code,
                self.assertEqual,
                result,
                error_message=error_message
            )

    def testSponsorListAPI(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # add a sponsor
            self.add_sponsor("New Sponsor")

            # test a get with sponsors
            error_message = (
                Routes['sponsor'] + " GET Failed to return list of sponsors"
            )
            self.getListTest(Routes['sponsor'], error_message=error_message)

    def testSponsorAPIGet(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # insert a sponsor
            sponsor = self.add_sponsor("XXTEST")

            # invalid sponsor id
            expect = {
                'details': INVALID_ID,
                "message": SponsorDoesNotExist.message
            }
            self.getTest(
                Routes['sponsor'] + "/" + str(INVALID_ID),
                SponsorDoesNotExist.status_code,
                self.assertEqual,
                expect,
                error_message=Routes['sponsor'] + " Get: Invalid Sponsor"
            )

            # valid sponsor id
            self.getTest(
                Routes['sponsor'] + "/" + str(sponsor['sponsor_id']),
                SUCCESSFUL_GET_CODE,
                self.assertSponsorModelEqual,
                sponsor,
                error_message=Routes['sponsor'] + " Get: valid Sponsor"
            )

    def testSponsorAPIDelete(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # insert a sponsor
            sponsor = self.add_sponsor("XXTEST")

            # delete of invalid sponsor id
            error_message = Routes['sponsor'] + " DELETE Invalid Sponsor id "
            self.deleteValidTest(
                Routes['sponsor'],
                SponsorDoesNotExist.status_code,
                self.assertSponsorModelEqual,
                sponsor['sponsor_id'],
                sponsor,
                SponsorDoesNotExist.message,
                error_message=error_message
            )

            # delete valid sponsor id
            error_message = Routes['sponsor'] + " DELETE valid Sponsor id "
            self.deleteInvalidTest(
                Routes['sponsor'],
                SponsorDoesNotExist.status_code,
                SponsorDoesNotExist.message,
                error_message=error_message
            )

    def testSponsorAPIPut(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # insert a sponsor
            sponsor = self.add_sponsor("XXTEST")
            sponsor_updated_name = "YYTEST"

            # invalid sponsor id
            params = {'sponsor_name': 'New League'}
            expect = {
                'details': INVALID_ID,
                'message': SponsorDoesNotExist.message
            }
            error_message = Routes['sponsor'] + " PUT: given invalid sponsor ID"
            self.putTest(
                Routes['sponsor'] + "/" + str(INVALID_ID),
                params,
                SponsorDoesNotExist.status_code,
                self.assertEqual,
                expect,
                error_message=error_message
            )

            # invalid parameters
            params = {'sponsor_name': 1}
            expect = {
                'details': "Sponsor - name",
                'message': InvalidField.message
            }
            error_message = Routes['sponsor'] + " PUT: given invalid parameters"
            self.putTest(
                Routes['sponsor'] + "/" + str(sponsor['sponsor_id']),
                params,
                InvalidField.status_code,
                self.assertEqual,
                expect,
                error_message=error_message
            )

            # successful update
            params = {'sponsor_name': sponsor_updated_name}
            sponsor['sponsor_name'] = sponsor_updated_name
            error_message = Routes['sponsor'] + " PUT: Failed to update Sponsor"
            self.putTest(
                Routes['sponsor'] + "/" + str(sponsor['sponsor_id']),
                params,
                SUCCESSFUL_PUT_CODE,
                self.assertEqual,
                None,
                error_message=error_message
            )

            # now try to get it
            self.getTest(
                Routes['sponsor'] + "/" + str(sponsor['sponsor_id']),
                SUCCESSFUL_GET_CODE,
                self.assertSponsorModelEqual,
                sponsor,
                error_message=Routes['fun'] + " Get: valid Sponsor"
            )
