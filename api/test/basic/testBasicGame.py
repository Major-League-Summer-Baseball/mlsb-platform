'''
@author: Dallas Fraser
@date: 2019-03-13
@organization: MLSB API
@summary: Tests all the basic game APIS
'''
from api.helper import loads
from api.routes import Routes
from api.errors import \
    InvalidField, TeamDoesNotExist, \
    LeagueDoesNotExist, GameDoesNotExist, DivisionDoesNotExist
from uuid import uuid1
from base64 import b64encode
from api.test.BaseTest import \
    TestSetup, ADMIN, PASSWORD, SUCCESSFUL_GET_CODE, \
    INVALID_ID, SUCCESSFUL_PUT_CODE, addGame, VALID_YEAR


headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' +
                                                  PASSWORD, "utf-8")
                                            ).decode("ascii")
}
MISSING_PARAMETER = ('Missing required parameter in the JSON body ' +
                     'or the post body or the query string')


class TestGame(TestSetup):

    def testGameInvalidPost(self):
        # Note Valid Requests are tested in BaseTest method add_game
        # missing parameters
        params = {}
        expect = {'message': {
            'away_team_id': MISSING_PARAMETER,
            'date': MISSING_PARAMETER,
            'home_team_id': MISSING_PARAMETER,
            'league_id': MISSING_PARAMETER,
            'time': MISSING_PARAMETER,
            'division_id': MISSING_PARAMETER}}
        error_message = (Routes['game'] +
                         " POST: request with missing parameter")
        self.postInvalidTest(Routes['game'],
                             params,
                             InvalidField.status_code,
                             self.assertEqual,
                             expect,
                             error_message=error_message)

        # add two teams, a sponsor and a league
        division = self.add_division(str(uuid1()))
        league = self.add_league(str(uuid1()))
        sponsor = self.add_sponsor(str(uuid1()))
        home_team = self.add_team(str(uuid1()), sponsor, league, VALID_YEAR)
        away_team = self.add_team(str(uuid1()), sponsor, league, VALID_YEAR)

        # testing invalid date
        params = {
            'home_team_id': home_team['team_id'],
            'away_team_id': away_team['team_id'],
            'date': "2014-02-2014",
            'time': "22:40",
            'league_id': league['league_id'],
            'division_id': division['division_id']
        }
        expect = {'details': 'Game - date', 'message': InvalidField.message}
        error_message = (Routes['game'] +
                         " POST: request with invalid date")
        self.postInvalidTest(Routes['game'],
                             params,
                             InvalidField.status_code,
                             self.assertEqual,
                             expect,
                             error_message=error_message)

        # testing invalid time
        params = {
            'home_team_id': home_team['team_id'],
            'away_team_id': away_team['team_id'],
            'date': "2014-02-10",
            'time': "22:66",
            'league_id': league['league_id'],
            'division_id': division['division_id']
        }
        expect = {'details': 'Game - time', 'message': InvalidField.message}
        error_message = (Routes['game'] +
                         " POST: request with invalid time")
        self.postInvalidTest(Routes['game'],
                             params,
                             InvalidField.status_code,
                             self.assertEqual,
                             expect,
                             error_message=error_message)

        # testing invalid home team id
        params = {
            'home_team_id': INVALID_ID,
            'away_team_id': away_team['team_id'],
            'date': "2014-02-10",
            'time': "22:40",
            'league_id': league['league_id'],
            'division_id': division['division_id']
        }
        expect = {'details': INVALID_ID, 'message': TeamDoesNotExist.message}
        error_message = (Routes['game'] +
                         " POST: request with invalid home team id")
        self.postInvalidTest(Routes['game'],
                             params,
                             TeamDoesNotExist.status_code,
                             self.assertEqual,
                             expect,
                             error_message=error_message)

        # testing invalid away team id
        params = {
            'home_team_id': home_team['team_id'],
            'away_team_id': INVALID_ID,
            'date': "2014-02-10",
            'time': "22:40",
            'league_id': league['league_id'],
            'division_id': division['division_id']
        }
        expect = {'details': INVALID_ID, 'message': TeamDoesNotExist.message}
        error_message = (Routes['game'] +
                         " POST: request with invalid away team id")
        self.postInvalidTest(Routes['game'],
                             params,
                             TeamDoesNotExist.status_code,
                             self.assertEqual,
                             expect,
                             error_message=error_message)

        # testing invalid division id
        params = {
            'home_team_id': home_team['team_id'],
            'away_team_id': away_team['team_id'],
            'date': "2014-02-10",
            'time': "22:40",
            'league_id': league['league_id'],
            'division_id': INVALID_ID
        }
        expect = {'details': INVALID_ID,
                  'message': DivisionDoesNotExist.message}
        error_message = (Routes['game'] +
                         " POST: request with invalid away team id")
        self.postInvalidTest(Routes['game'],
                             params,
                             TeamDoesNotExist.status_code,
                             self.assertEqual,
                             expect,
                             error_message=error_message)

    def testGameListAPI(self):
        # add two teams, a sponsor and a league
        division = self.add_division(str(uuid1()))
        league = self.add_league(str(uuid1()))
        sponsor = self.add_sponsor(str(uuid1()))
        home_team = self.add_team(str(uuid1()), sponsor, league, VALID_YEAR)
        away_team = self.add_team(str(uuid1()), sponsor, league, VALID_YEAR)

        # add a game
        self.add_game("2014-02-10",
                      "22:40",
                      home_team,
                      away_team,
                      league,
                      division)

        # test a get with games
        error_message = (Routes['game'] +
                         " GET Failed to return list of games")
        self.getListTest(Routes['game'], error_message=error_message)

    def testGameGet(self):
        # add a game
        game = addGame(self)

        # invalid Game id
        expect = {'details': INVALID_ID, "message": GameDoesNotExist.message}
        self.getTest(Routes['game'] + "/" + str(INVALID_ID),
                     GameDoesNotExist.status_code,
                     self.assertEqual,
                     expect,
                     error_message=Routes['game'] + " Get: Invalid Game")

        # valid Game id
        self.getTest(Routes['game'] + "/" + str(game['game_id']),
                     SUCCESSFUL_GET_CODE,
                     self.assertGameModelEqual,
                     game,
                     error_message=Routes['game'] + " Get: valid Game")

    def testGameDelete(self):

        # delete invalid game id
        rv = self.app.delete(Routes['game'] + "/" + str(INVALID_ID),
                             headers=headers)
        expect = {'details': INVALID_ID, 'message': GameDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, Routes['game'] +
                         " DELETE: on invalid game id")
        self.assertEqual(rv.status_code, GameDoesNotExist.status_code,
                         Routes['game'] +
                         " DELETE: on invalid game id")

        # add a game
        game = addGame(self)

        # delete valid game id
        rv = self.app.delete(Routes['game'] + "/" + str(game['game_id']),
                             headers=headers)
        expect = None
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, Routes['game'] +
                         " DELETE: on valid game id")
        self.assertEqual(rv.status_code, 200, Routes['game'] +
                         " DELETE: on valid game id")

    def testGamePut(self):
        # add a game
        game = addGame(self)
        invalid_route = Routes['game'] + "/" + str(INVALID_ID)
        valid_route = Routes['game'] + "/" + str(game['game_id'])

        # invalid game id
        params = {
            'home_team_id': game['home_team_id'],
            'away_team_id': game['away_team_id'],
            'date': "2014-08-22",
            'time': "11:37",
            'league_id': game['league_id'],
            'status': "Championship",
            'field': "WP1"
        }
        expect = {'details': INVALID_ID, 'message': GameDoesNotExist.message}
        error_message = Routes['game'] + " PUT: invalid game id"
        self.putTest(invalid_route,
                     params,
                     GameDoesNotExist.status_code,
                     self.assertEqual,
                     expect,
                     error_message=error_message)

        # invalid home team
        params = {
            'home_team_id': INVALID_ID,
            'away_team_id': game['away_team_id'],
            'date': "2014-08-22",
            'time': "11:37",
            'league_id': game['league_id'],
            'status': "Championship",
            'field': "WP1"
        }
        expect = {'details': INVALID_ID, 'message': TeamDoesNotExist.message}
        error_message = Routes['game'] + " PUT: invalid home team"
        self.putTest(valid_route,
                     params,
                     TeamDoesNotExist.status_code,
                     self.assertEqual,
                     expect,
                     error_message=error_message)

        # invalid away team
        params = {
            'home_team_id': game['home_team_id'],
            'away_team_id': INVALID_ID,
            'date': "2014-08-22",
            'time': "11:37",
            'league_id': game['league_id'],
            'status': "Championship",
            'field': "WP1"
        }
        expect = {'details': INVALID_ID, 'message': TeamDoesNotExist.message}
        error_message = Routes['game'] + " PUT: invalid away team"
        self.putTest(valid_route,
                     params,
                     TeamDoesNotExist.status_code,
                     self.assertEqual,
                     expect,
                     error_message=error_message)

        # invalid league
        params = {
            'home_team_id': game['home_team_id'],
            'away_team_id': game['away_team_id'],
            'date': "2014-08-22",
            'time': "11:37",
            'league_id': INVALID_ID,
            'status': "Championship",
            'field': "WP1"
        }
        expect = {'details': INVALID_ID, 'message': LeagueDoesNotExist.message}
        error_message = Routes['game'] + " PUT: invalid league"
        self.putTest(valid_route,
                     params,
                     LeagueDoesNotExist.status_code,
                     self.assertEqual,
                     expect,
                     error_message=error_message)

        # invalid date
        params = {
            'home_team_id': game['home_team_id'],
            'away_team_id': game['away_team_id'],
            'date': "xx-08-22",
            'time': "11:37",
            'league_id': game['league_id'],
            'status': "Championship",
            'field': "WP1"
        }
        expect = {'details': 'Game - date', 'message': InvalidField.message}
        error_message = Routes['game'] + " PUT: invalid date"
        self.putTest(valid_route,
                     params,
                     InvalidField.status_code,
                     self.assertEqual,
                     expect,
                     error_message=error_message)

        # invalid time
        params = {
            'home_team_id': game['home_team_id'],
            'away_team_id': game['away_team_id'],
            'date': "2014-08-22",
            'time': "XX:37",
            'league_id': game['league_id'],
            'status': "Championship",
            'field': "WP1"
        }
        expect = {'details': 'Game - time', 'message': InvalidField.message}
        error_message = Routes['game'] + " PUT: invalid time"
        self.putTest(valid_route,
                     params,
                     InvalidField.status_code,
                     self.assertEqual,
                     expect,
                     error_message=error_message)

        # invalid status
        params = {
            'home_team_id': game['home_team_id'],
            'away_team_id': game['away_team_id'],
            'date': "2014-08-22",
            'time': "11:37",
            'league_id': game['league_id'],
            'status': 1,
            'field': "WP1"
        }
        expect = {'details': 'Game - status', 'message': InvalidField.message}
        error_message = Routes['game'] + " PUT: invalid status"
        self.putTest(valid_route,
                     params,
                     InvalidField.status_code,
                     self.assertEqual,
                     expect,
                     error_message=error_message)

        # invalid field
        params = {
            'home_team_id': game['home_team_id'],
            'away_team_id': game['away_team_id'],
            'date': "2014-08-22",
            'time': "11:37",
            'league_id': game['league_id'],
            'status': "Championship",
            'field': 1
        }
        expect = {'details': 'Game - field', 'message': InvalidField.message}
        error_message = Routes['game'] + " PUT: invalid field"
        self.putTest(valid_route,
                     params,
                     InvalidField.status_code,
                     self.assertEqual,
                     expect,
                     error_message=error_message)

        # valid update parameters
        params = {
            'home_team_id': game['home_team_id'],
            'away_team_id': game['away_team_id'],
            'date': "2014-08-22",
            'time': "11:37",
            'league_id': game['league_id'],
            'status': "Championship",
            'field': "WP1"
        }
        game['home_team_id'] = params['home_team_id']
        game['away_team_id'] = params['away_team_id']
        game['date'] = params['date']
        game['time'] = params['time']
        game['league_id'] = params['league_id']
        game['status'] = params['status']
        game['field'] = params['field']
        expect = None
        error_message = Routes['game'] + " PUT: valid update"
        self.putTest(valid_route,
                     params,
                     SUCCESSFUL_PUT_CODE,
                     self.assertEqual,
                     expect,
                     error_message=error_message)

        # test a valid get
        error_message = Routes['game'] + " GET: just updated game"
        self.getTest(valid_route,
                     SUCCESSFUL_GET_CODE,
                     self.assertGameModelEqual,
                     game,
                     error_message=error_message)
