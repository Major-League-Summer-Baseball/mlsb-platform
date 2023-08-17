'''
@author: Dallas Fraser
@date: 2019-03-13
@organization: MLSB API
@summary: Tests all the basic player APIS
'''
from api.routes import Routes
from api.errors import InvalidField, PlayerDoesNotExist, NonUniqueEmail
from base64 import b64encode
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


class TestPlayer(TestSetup):

    def testPlayerInvalidPost(self):
        # Note Valid Requests are tested in BaseTest method add_player
        # missing parameters
        params = {}
        result = {'message': {
            'player_name': MISSING_PARAMETER,
            'email': MISSING_PARAMETER
        }
        }
        error_message = (Routes['player'] +
                         " POST: request with missing parameter")
        self.postInvalidTest(Routes['player'],
                             params,
                             InvalidField.status_code,
                             self.assertEqual,
                             result,
                             error_message=error_message)

        # testing a gender parameter
        params = {'player_name': 'Dallas Fraser',
                  'gender': 'X',
                  'email': "new@mlsb.ca"}
        result = {'details': 'Player - gender',
                  'message': InvalidField.message}
        error_message = (Routes['player'] +
                         " POST: request with invalid gender")
        self.postInvalidTest(Routes['player'],
                             params,
                             InvalidField.status_code,
                             self.assertEqual,
                             result,
                             error_message=error_message)

        # testing player_name parameter
        params = {'player_name': 1, 'gender': 'M', 'email': 'new@mlsb.ca'}
        result = {'details': 'Player - name', 'message': InvalidField.message}
        error_message = (Routes['player'] +
                         " POST: request with invalid player name")
        self.postInvalidTest(Routes['player'],
                             params,
                             InvalidField.status_code,
                             self.assertEqual,
                             result,
                             error_message=error_message)

    def testPlayerListApi(self):
        # add a player
        self.add_player("Test Player", "TestPlayer@mlsb.ca", gender="M")

        # test a get with leagues
        error_message = (Routes['player'] +
                         " GET Failed to return list of players")
        self.getListTest(Routes['player'], error_message=error_message)

    def testPlayerApiGet(self):
        # add a player
        player = self.add_player("Test Player",
                                 "TestPlayer@mlsb.ca",
                                 gender="M")
        # invalid Player id
        expect = {'details': INVALID_ID, "message": PlayerDoesNotExist.message}
        self.getTest(Routes['player'] + "/" + str(INVALID_ID),
                     PlayerDoesNotExist.status_code,
                     self.assertEqual,
                     expect,
                     error_message=Routes['player'] + " Get: Invalid Player")

        # valid Player id
        self.getTest(Routes['player'] + "/" + str(player['player_id']),
                     SUCCESSFUL_GET_CODE,
                     self.assertPlayerModelEqual,
                     player,
                     error_message=Routes['player'] + " Get: valid Player")

    def testPlayerApiDelete(self):
        # add a player
        player = self.add_player("Test Player",
                                 "TestPlayer@mlsb.ca",
                                 gender="M")

        # delete of invalid league id
        error_message = Routes['player'] + " DELETE Invalid player id "
        self.deleteValidTest(Routes['player'],
                             PlayerDoesNotExist.status_code,
                             self.assertPlayerModelEqual,
                             player['player_id'],
                             player,
                             PlayerDoesNotExist.message,
                             error_message=error_message)

        # delete valid player id
        error_message = Routes['player'] + " DELETE valid player id "
        self.deleteInvalidTest(Routes['player'],
                               PlayerDoesNotExist.status_code,
                               PlayerDoesNotExist.message,
                               error_message=error_message)

    def testPlayerApiPut(self):
        # add a player
        player = self.add_player("Test Player",
                                 "TestPlayer@mlsb.ca",
                                 gender="M")

        # invalid player id
        params = {'player_name': 'David Duchovny', 'gender': "F"}
        result = {'details': INVALID_ID, 'message': PlayerDoesNotExist.message}
        error_message = Routes['player'] + ' PUT: Invalid Player ID'
        self.putTest(Routes['player'] + '/' + str(INVALID_ID),
                     params,
                     PlayerDoesNotExist.status_code,
                     self.assertEqual,
                     result,
                     error_message=error_message)

        # invalid player_name type
        params = {'player_name': 1, 'gender': "F"}
        result = {'details': 'Player - name', 'message': InvalidField.message}
        error_message = Routes['player'] + ' PUT: Invalid Player name'
        self.putTest(Routes['player'] + "/" + str(player['player_id']),
                     params,
                     InvalidField.status_code,
                     self.assertEqual,
                     result,
                     error_message=error_message)

        # invalid gender
        params = {'player_name': "David Duchovny", 'gender': "X"}
        result = {'details': 'Player - gender',
                  'message': InvalidField.message}
        error_message = Routes['player'] + ' PUT: Invalid Player gender'
        self.putTest(Routes['player'] + "/" + str(player['player_id']),
                     params,
                     InvalidField.status_code,
                     self.assertEqual,
                     result,
                     error_message=error_message)

        # successfully update
        params = {'player_name': "David Duchovny", 'gender': "F"}
        player['player_name'] = "David Duchovny"
        player['gender'] = "f"
        result = None
        error_message = Routes['player'] + ' PUT: Valid player update'
        self.putTest(Routes['player'] + "/" + str(player['player_id']),
                     params,
                     SUCCESSFUL_PUT_CODE,
                     self.assertEqual,
                     result,
                     error_message=error_message)

        # now get it
        error_message = Routes['player'] + " Get: valid player"
        self.getTest(Routes['player'] + "/" + str(player['player_id']),
                     SUCCESSFUL_GET_CODE,
                     self.assertPlayerModelEqual,
                     player,
                     error_message=error_message)

    def testPlayerApiPutDuplicateEmail(self):
        # add two player
        player_one = self.add_player("Test Player",
                                     "TestPlayer@mlsb.ca",
                                     gender="M")
        player_two_email = "TestPlayerTwo@mlsb.ca"
        self.add_player("Test Player", player_two_email, gender="M")

        # try to update the first player to have the same email as the second
        params = {'email': player_two_email}
        result = {'details': player_two_email.strip().lower(),
                  'message': NonUniqueEmail.message}
        error_message = Routes['player'] + ' PUT: Valid player update'
        self.putTest(Routes['player'] + "/" + str(player_one['player_id']),
                     params,
                     NonUniqueEmail.status_code,
                     self.assertEqual,
                     result,
                     error_message=error_message)
