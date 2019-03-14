'''
@author: Dallas Fraser
@date: 2019-03-13
@organization: MLSB API
@summary: Tests all the basic espys APIS
'''
from api.routes import Routes
from api.errors import \
    SponsorDoesNotExist, InvalidField, EspysDoesNotExist, TeamDoesNotExist
from base64 import b64encode
from api.test.BaseTest import TestSetup, ADMIN, PASSWORD, SUCCESSFUL_GET_CODE,\
                              INVALID_ID, SUCCESSFUL_PUT_CODE,\
                              addEspy, VALID_YEAR


headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' +
                                                  PASSWORD, "utf-8")
                                            ).decode("ascii")
}
MISSING_PARAMETER = ('Missing required parameter in the JSON body ' +
                     'or the post body or the query string')


class TestEspys(TestSetup):
    def testEspysApiGet(self):
        # proper insertion
        points = 10
        espy = addEspy(self, points)

        # invalid espy id
        result = {'details': INVALID_ID, 'message': EspysDoesNotExist.message}
        error_message = Routes['espy'] + " GET invalid espy id"
        self.getTest(Routes['espy'] + "/" + str(INVALID_ID),
                     EspysDoesNotExist.status_code,
                     self.assertEqual,
                     result,
                     error_message=error_message)

        # valid espy id
        self.getTest(Routes['espy'] + "/" + str(espy['espy_id']),
                     SUCCESSFUL_GET_CODE,
                     self.assertEspysModelEqual,
                     espy,
                     error_message=error_message)

    def testEspysApiDelete(self):
        # proper insertion with post
        points = 10
        espy = addEspy(self, points)

        # delete invalid espy
        error_message = Routes['espy'] + " DELETE Invalid espy id "
        self.deleteValidTest(Routes['espy'],
                             EspysDoesNotExist.status_code,
                             self.assertEqual,
                             espy['espy_id'],
                             espy,
                             EspysDoesNotExist.message,
                             error_message=error_message)

        # delete valid player id
        error_message = Routes['espy'] + " DELETE valid espy id"
        self.deleteInvalidTest(Routes['espy'],
                               EspysDoesNotExist.status_code,
                               EspysDoesNotExist.message,
                               error_message=error_message)

    def testEspysApiPut(self):
        # must add a espy
        points = 10
        receipt = "New Receipt"
        description = " New Description"
        espy = addEspy(self, points)
        valid_route = Routes['espy'] + "/" + str(espy['espy_id'])
        invalid_route = Routes['espy'] + "/" + str(INVALID_ID)

        # invalid espy id
        params = {'team_id': espy['team_id'],
                  'sponsor_id': espy['sponsor_id'],
                  'description': description,
                  'points': points,
                  'receipt': receipt}
        result = {'details': INVALID_ID, 'message': EspysDoesNotExist.message}
        error_message = Routes['espy'] + ' PUT: Invalid espy ID'
        self.putTest(invalid_route,
                     params,
                     EspysDoesNotExist.status_code,
                     self.assertEqual,
                     result,
                     error_message=error_message)

        # invalid team id
        params = {'team_id': INVALID_ID,
                  'sponsor_id': espy['sponsor_id'],
                  'description': description,
                  'points': points,
                  'receipt': receipt}
        result = {'details': INVALID_ID, 'message': TeamDoesNotExist.message}
        error_message = Routes['espy'] + ' PUT: Invalid espy team'
        self.putTest(valid_route,
                     params,
                     EspysDoesNotExist.status_code,
                     self.assertEqual,
                     result,
                     error_message=error_message)

        # invalid sponsor id
        params = {'team_id': espy['team_id'],
                  'sponsor_id': INVALID_ID,
                  'description': description,
                  'points': points,
                  'receipt': receipt}
        result = {'details': INVALID_ID,
                  'message': SponsorDoesNotExist.message}
        error_message = Routes['espy'] + ' PUT: Invalid sponsor'
        self.putTest(valid_route,
                     params,
                     SponsorDoesNotExist.status_code,
                     self.assertEqual,
                     result,
                     error_message=error_message)

        # successfully update
        params = {'team_id': espy['team_id'],
                  'sponsor_id': espy['sponsor_id'],
                  'description': description,
                  'points': points,
                  'receipt': receipt}
        result = None
        error_message = Routes['espy'] + " PUT: Valid espy update"
        self.putTest(valid_route,
                     params,
                     SUCCESSFUL_PUT_CODE,
                     self.assertEqual,
                     result,
                     error_message=error_message)

        # now get espy to ensure updated were saved
        error_message = Routes['espy'] + " GET: updated espy"
        espy['team_id'] = params['team_id']
        espy['sponsor_id'] = params['sponsor_id']
        espy['description'] = params['description']
        espy['points'] = params['points']
        espy['receipt'] = params['receipt']
        self.getTest(valid_route,
                     SUCCESSFUL_GET_CODE,
                     self.assertEspysModelEqual,
                     espy,
                     error_message=error_message)

    def testEspysApiInvalidPost(self):
        # missing parameters
        sponsor = self.add_sponsor("Test Team")
        team = self.add_team("Black",
                             sponsor,
                             self.add_league("Test League"),
                             VALID_YEAR)
        params = {}
        result = {'message': {
                              'points': MISSING_PARAMETER,
                              'team_id': MISSING_PARAMETER
                              }
                  }
        error_message = (Routes['espy'] +
                         " POST: request with missing parameter")
        self.postInvalidTest(Routes['espy'],
                             params,
                             InvalidField.status_code,
                             self.assertEqual,
                             result,
                             error_message=error_message)

        # testing a team id parameter
        params = {'team_id': INVALID_ID,
                  'sponsor_id': sponsor['sponsor_id'],
                  'points': 5}
        result = {'details': INVALID_ID, 'message': TeamDoesNotExist.message}
        error_message = (Routes['espy'] +
                         " POST: request with invalid team id")
        self.postInvalidTest(Routes['espy'],
                             params,
                             TeamDoesNotExist.status_code,
                             self.assertEqual,
                             result,
                             error_message=error_message)

        # testing sponsor id parameter
        params = {'team_id': team['team_id'],
                  'sponsor_id': INVALID_ID,
                  'points': 5}
        result = {'details': INVALID_ID,
                  'message': SponsorDoesNotExist.message}
        error_message = (Routes['espy'] +
                         " POST: request with invalid sponsor id")
        self.postInvalidTest(Routes['espy'],
                             params,
                             SponsorDoesNotExist.status_code,
                             self.assertEqual,
                             result,
                             error_message=error_message)

        # testing points parameter
        params = {'team_id': team['team_id'],
                  'sponsor_id': sponsor['sponsor_id'],
                  'points': "XX"}
        result = {'details': 'Game - points', 'message': InvalidField.message}
        error_message = (Routes['espy'] +
                         " POST: request with invalid points")
        self.postInvalidTest(Routes['espy'],
                             params,
                             InvalidField.status_code,
                             self.assertEqual,
                             result,
                             error_message=error_message)

    def testEspysList(self):
        # test a get with espys
        error_message = (Routes['espy'] +
                         " GET Failed to return list of espys")
        self.getListTest(Routes['espy'], error_message=error_message)
