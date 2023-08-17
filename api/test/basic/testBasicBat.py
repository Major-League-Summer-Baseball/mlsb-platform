'''
@author: Dallas Fraser
@date: 2019-03-13
@organization: MLSB API
@summary: Tests all the basic bat APIS
'''
from api.routes import Routes
from api.errors import \
    InvalidField, TeamDoesNotExist, PlayerDoesNotExist, \
    GameDoesNotExist, BatDoesNotExist
from base64 import b64encode
from api.test.BaseTest import \
    TestSetup, ADMIN, PASSWORD, SUCCESSFUL_GET_CODE, \
    INVALID_ID, SUCCESSFUL_PUT_CODE, addBat, addGame


headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' +
                                                  PASSWORD, "utf-8")
                                            ).decode("ascii")
}
MISSING_PARAMETER = ('Missing required parameter in the JSON body ' +
                     'or the post body or the query string')


class TestBat(TestSetup):

    def testBateInvalidPost(self):
        # Note Valid Requests are tested in BaseTest method add_bat
        # missing parameters
        game = addGame(self)
        player = self.add_player("Test Player",
                                 "TestPLayer@mlsb.ca",
                                 gender="M")
        params = {}
        expect = {
            'message': {
                'game_id': MISSING_PARAMETER,
                'hit': MISSING_PARAMETER,
                'player_id': MISSING_PARAMETER,
                'team_id': MISSING_PARAMETER
            }
        }
        error_message = (Routes['bat'] +
                         " POST: request with missing parameter")
        self.postInvalidTest(Routes['bat'],
                             params,
                             InvalidField.status_code,
                             self.assertEqual,
                             expect,
                             error_message=error_message)

        # testing invalid player
        params = {
            'game_id': game['game_id'],
            'player_id': INVALID_ID,
            'team_id': game['home_team_id'],
            'rbi': 2,
            'hit': "hr",
            'inning': 1
        }
        expect = {'details': INVALID_ID, 'message': PlayerDoesNotExist.message}
        error_message = (Routes['bat'] +
                         " POST: request with invalid player id")
        self.postInvalidTest(Routes['bat'],
                             params,
                             PlayerDoesNotExist.status_code,
                             self.assertEqual,
                             expect,
                             error_message=error_message)

        # testing invalid game
        params = {
            'game_id': INVALID_ID,
            'player_id': player['player_id'],
            'team_id': game['home_team_id'],
            'rbi': 2,
            'hit': "hr",
            'inning': 1
        }
        expect = {'details': INVALID_ID, 'message': GameDoesNotExist.message}
        error_message = (Routes['bat'] +
                         " POST: request with invalid game id")
        self.postInvalidTest(Routes['bat'],
                             params,
                             GameDoesNotExist.status_code,
                             self.assertEqual,
                             expect,
                             error_message=error_message)

        # testing invalid team
        params = {
            'game_id': game['game_id'],
            'player_id': player['player_id'],
            'team_id': INVALID_ID,
            'rbi': 2,
            'hit': "hr",
            'inning': 1
        }
        expect = {'details': str(INVALID_ID),
                  'message': TeamDoesNotExist.message}
        error_message = (Routes['bat'] +
                         " POST: request with invalid team id")
        self.postInvalidTest(Routes['bat'],
                             params,
                             TeamDoesNotExist.status_code,
                             self.assertEqual,
                             expect,
                             error_message=error_message)

        # testing invalid rbi
        params = {
            'game_id': INVALID_ID,
            'player_id': player['player_id'],
            'team_id': game['home_team_id'],
            'rbi': 100,
            'hit': "hr",
            'inning': 1
        }
        expect = {'details': 'Bat - rbi', 'message': InvalidField.message}
        error_message = (Routes['bat'] +
                         " POST: request with invalid rbi")
        self.postInvalidTest(Routes['bat'],
                             params,
                             InvalidField.status_code,
                             self.assertEqual,
                             expect,
                             error_message=error_message)

        # testing invalid inning
        params = {
            'game_id': INVALID_ID,
            'player_id': player['player_id'],
            'team_id': game['home_team_id'],
            'rbi': 1,
            'hit': "hr",
            'inning': -1
        }
        expect = {'details': 'Bat - inning', 'message': InvalidField.message}
        error_message = (Routes['bat'] +
                         " POST: request with invalid inning")
        self.postInvalidTest(Routes['bat'],
                             params,
                             InvalidField.status_code,
                             self.assertEqual,
                             expect,
                             error_message=error_message)

        # testing invalid hit
        params = {
            'game_id': INVALID_ID,
            'player_id': player['player_id'],
            'team_id': game['home_team_id'],
            'rbi': 1,
            'hit': "xx",
            'inning': 1
        }
        expect = {'details': 'Bat - hit', 'message': InvalidField.message}
        error_message = (Routes['bat'] +
                         " POST: request with invalid hit")
        self.postInvalidTest(Routes['bat'],
                             params,
                             InvalidField.status_code,
                             self.assertEqual,
                             expect,
                             error_message=error_message)

    def testBatList(self):
        # test a get with bat
        error_message = (Routes['bat'] +
                         " GET Failed to return list of bats")
        self.getListTest(Routes['bat'], error_message=error_message)

    def testBatGet(self):
        # add a bat
        bat = addBat(self, "S")
        # get on invalid id
        expect = {'details': INVALID_ID, 'message': BatDoesNotExist.message}
        self.getTest(Routes['bat'] + "/" + str(INVALID_ID),
                     BatDoesNotExist.status_code,
                     self.assertEqual,
                     expect,
                     error_message=Routes['bat'] + " GET: invalid bat id"
                     )

        # get on valid id
        self.getTest(Routes['bat'] + "/" + str(bat['bat_id']),
                     SUCCESSFUL_GET_CODE,
                     self.assertBatModelEqual,
                     bat,
                     error_message=Routes['bat'] + " GET: valid bat id")

    def testBatDelete(self):
        # add a bat
        bat = addBat(self, "S")

        # testing deleting valid bat id
        error_message = Routes['bat'] + " DELETE: valid bat id"
        self.deleteValidTest(Routes['bat'],
                             BatDoesNotExist.status_code,
                             self.assertBatModelEqual,
                             bat['bat_id'],
                             bat,
                             BatDoesNotExist.message,
                             error_message=error_message)

        # testing deleting invalid bat id
        error_message = Routes['bat'] + " DELETE: invalid bat id"
        self.deleteInvalidTest(Routes['bat'],
                               BatDoesNotExist.status_code,
                               BatDoesNotExist.message,
                               error_message=error_message)

    def testBatPut(self):
        # add a bat
        bat = addBat(self, "S")
        invalid_route = Routes['bat'] + "/" + str(INVALID_ID)
        valid_route = Routes['bat'] + "/" + str(bat['bat_id'])
        # invalid bat ID
        params = {
            'game_id': bat['game_id'],
            'player_id': bat['player_id'],
            'team_id': bat['team_id'],
            'rbi': 4,
            'hit': "HR",
            'inning': 1}
        expect = {'details': INVALID_ID, 'message': BatDoesNotExist.message}
        error_message = Routes['bat'] + " PUT: invalid Bat id"
        self.putTest(invalid_route,
                     params,
                     BatDoesNotExist.status_code,
                     self.assertEqual,
                     expect,
                     error_message=error_message)

        # test invalid game_id
        params = {
            'game_id': INVALID_ID,
            'player_id': bat['player_id'],
            'team_id': bat['team_id'],
            'rbi': 4,
            'hit': "HR",
            'inning': 1}
        expect = {'details': INVALID_ID, 'message': GameDoesNotExist.message}
        error_message = Routes['bat'] + " PUT: invalid game"
        self.putTest(valid_route,
                     params,
                     GameDoesNotExist.status_code,
                     self.assertEqual,
                     expect,
                     error_message=error_message)

        # test invalid player_id
        params = {
            'game_id': bat['game_id'],
            'player_id': INVALID_ID,
            'team_id': bat['team_id'],
            'rbi': 4,
            'hit': "HR",
            'inning': 1}
        expect = {'details': INVALID_ID, 'message': PlayerDoesNotExist.message}
        error_message = Routes['bat'] + " PUT: invalid player"
        self.putTest(valid_route,
                     params,
                     PlayerDoesNotExist.status_code,
                     self.assertEqual,
                     expect,
                     error_message=error_message)

        # test invalid team_id
        params = {
            'game_id': bat['game_id'],
            'player_id': bat['player_id'],
            'team_id': INVALID_ID,
            'rbi': 4,
            'hit': "HR",
            'inning': 1}
        expect = {'details': str(INVALID_ID),
                  'message': TeamDoesNotExist.message}
        error_message = Routes['bat'] + " PUT: invalid team"
        self.putTest(valid_route,
                     params,
                     TeamDoesNotExist.status_code,
                     self.assertEqual,
                     expect,
                     error_message=error_message)

        # test invalid rbi
        params = {
            'game_id': bat['game_id'],
            'player_id': bat['player_id'],
            'team_id': bat['team_id'],
            'rbi': 10,
            'hit': "HR",
            'inning': 1}
        expect = {'details': 'Bat - rbi', 'message': InvalidField.message}
        error_message = Routes['bat'] + " PUT: invalid rbi"
        self.putTest(valid_route,
                     params,
                     InvalidField.status_code,
                     self.assertEqual,
                     expect,
                     error_message=error_message)

        # test invalid hit
        params = {
            'game_id': bat['game_id'],
            'player_id': bat['player_id'],
            'team_id': bat['team_id'],
            'rbi': 1,
            'hit': "XX",
            'inning': 1}
        expect = {'details': 'Bat - hit', 'message': InvalidField.message}
        error_message = Routes['bat'] + " PUT: invalid hit"
        self.putTest(valid_route,
                     params,
                     InvalidField.status_code,
                     self.assertEqual,
                     expect,
                     error_message=error_message)

        # test invalid inning
        params = {
            'game_id': bat['game_id'],
            'player_id': bat['player_id'],
            'team_id': bat['team_id'],
            'rbi': 4,
            'hit': "HR",
            'inning': -1}
        expect = {'details': 'Bat - inning', 'message': InvalidField.message}
        error_message = Routes['bat'] + " PUT: invalid inning"
        self.putTest(valid_route,
                     params,
                     InvalidField.status_code,
                     self.assertEqual,
                     expect,
                     error_message=error_message)

        # valid update
        second_game = addGame(self)
        sponsor = self.add_sponsor("Second Sponsor")
        league = self.add_league("Second League")
        second_team = self.add_team("test team two",
                                    sponsor=sponsor,
                                    league=league)
        second_player = self.add_player("test player two",
                                        "testPlayerTwo@mlsb.ca",
                                        "M")
        params = {
            'game_id': second_game['game_id'],
            'player_id': second_player['player_id'],
            'team_id': second_team['team_id'],
            'rbi': 4,
            'hit': "HR",
            'inning': 1
        }
        bat['game_id'] = params['game_id']
        bat['player_id'] = params['player_id']
        bat['team_id'] = params['team_id']
        bat['rbi'] = params['rbi']
        bat['hit'] = params['hit']
        bat['inning'] = params['inning']
        expect = None
        error_message = Routes['bat'] + " PUT: valid parameters"
        self.putTest(valid_route,
                     params,
                     SUCCESSFUL_PUT_CODE,
                     self.assertEqual,
                     expect,
                     error_message=error_message)

        # test a get to make sure it was updated
        error_message = Routes['bat'] + " GET: updated bat"
        self.getTest(valid_route,
                     SUCCESSFUL_GET_CODE,
                     self.assertBatModelEqual,
                     bat,
                     error_message=error_message)
