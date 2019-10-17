'''
@author: Dallas Fraser
@date: 2019-03-13
@organization: MLSB API
@summary: Tests all the basic league APIS
'''
from api.routes import Routes
from api.errors import InvalidField, LeagueDoesNotExist
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


class TestLeague(TestSetup):

    def testLeagueInvalidPost(self):
        # Note Valid Requests are tested in BaseTest method add_league
        # missing parameters
        params = {}
        result = {'message': {
            'league_name': MISSING_PARAMETER
        }
        }
        error_message = (Routes['league'] +
                         " POST: request with missing parameter")
        self.postInvalidTest(Routes['league'],
                             params,
                             InvalidField.status_code,
                             self.assertEqual,
                             result,
                             error_message=error_message)

        # testing a league name parameter
        params = {'league_name': 1}
        result = {'details': 'League - name', 'message': InvalidField.message}
        error_message = (Routes['league'] +
                         " POST: request with invalid league_name")
        self.postInvalidTest(Routes['league'],
                             params,
                             InvalidField.status_code,
                             self.assertEqual,
                             result,
                             error_message=error_message)

    def testLeagueListAPI(self):
        # proper insertion with post
        self.add_league("New League")

        # test a get with leagues
        error_message = (Routes['league'] +
                         " GET Failed to return list of leagues")
        self.getListTest(Routes['league'], error_message=error_message)

    def testLeagueAPIGet(self):
        # add a league
        league = self.add_league("New League")

        # invalid League id
        expect = {'details': INVALID_ID, "message": LeagueDoesNotExist.message}
        self.getTest(Routes['league'] + "/" + str(INVALID_ID),
                     LeagueDoesNotExist.status_code,
                     self.assertEqual,
                     expect,
                     error_message=Routes['league'] + " Get: Invalid League")

        # valid League id
        self.getTest(Routes['league'] + "/" + str(league['league_id']),
                     SUCCESSFUL_GET_CODE,
                     self.assertLeagueModelEqual,
                     league,
                     error_message=Routes['league'] + " Get: valid League")

    def testLeagueAPIPut(self):
        # add a league
        league = self.add_league("New League")

        # invalid league id
        params = {'league_name': 'Chainsaw Classic'}
        result = {'details': INVALID_ID, 'message': LeagueDoesNotExist.message}
        self.putTest(Routes['league'] + '/' + str(INVALID_ID),
                     params,
                     LeagueDoesNotExist.status_code,
                     self.assertEqual,
                     result,
                     error_message=Routes['league'] + ' PUT:Invalid league ID')

        # invalid league_name type
        params = {'league_name': 1}
        result = {'details': 'League - name', 'message': InvalidField.message}
        error_message = Routes['league'] + ' PUT: Invalid parameters'
        self.putTest(Routes['league'] + '/' + str(league['league_id']),
                     params,
                     InvalidField.status_code,
                     self.assertEqual,
                     result,
                     error_message=error_message)

        # successfully update
        league['league_name'] = "Updated league name"
        params = {'league_name': league['league_name']}
        error_message = Routes['league'] + ' PUT: Successful Update'
        self.putTest(Routes['league'] + '/' + str(league['league_id']),
                     params,
                     SUCCESSFUL_PUT_CODE,
                     self.assertEqual,
                     None,
                     error_message=error_message)

        # now get it
        self.getTest(Routes['league'] + "/" + str(league['league_id']),
                     SUCCESSFUL_GET_CODE,
                     self.assertLeagueModelEqual,
                     league,
                     error_message=Routes['fun'] + " Get: valid League")
