'''
@author: Dallas Fraser
@date: 2016-04-12
@organization: MLSB API
@summary: Tests all the basic APIs
'''
import unittest
from api.helper import loads
from api import DB
from api.routes import Routes
from api.model import Player
from datetime import datetime
from api.errors import \
    SponsorDoesNotExist, InvalidField, EspysDoesNotExist, TeamDoesNotExist,\
    PlayerDoesNotExist, NonUniqueEmail, LeagueDoesNotExist, GameDoesNotExist,\
    BatDoesNotExist, FunDoesNotExist
from datetime import date
from base64 import b64encode
from api.BaseTest import TestSetup, ADMIN, PASSWORD, SUCCESSFUL_GET_CODE,\
                         INVALID_ID, SUCCESSFUL_DELETE_CODE,\
                         SUCCESSFUL_PUT_CODE
from api.testData import bat, espys
headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' +
                                                  PASSWORD, "utf-8")
                                            ).decode("ascii")
}
MISSING_PARAMETER = ('Missing required parameter in the JSON body ' +
                     'or the post body or the query string')
VALID_YEAR = date.today().year


class TestFun(TestSetup):
    def testFunInvalidPost(self):
        # Note Valid Requests are testedasdin BaseTest method add_fun

        # missing parameters
        params = {}
        result = {'message': {'year': MISSING_PARAMETER}}
        error_message = Routes['fun'] + " POST: request with missing parameter"
        self.postInvalidTest(Routes['fun'],
                             params,
                             InvalidField.status_code,
                             self.assertEqual,
                             result,
                             error_message=error_message)

    def testFunListAPI(self):
        # TODO pagination

        # add some fun
        fun = self.add_fun(100, year=1900)

        # test a get with funs
        rv = self.app.get(Routes['fun'])
        self.output(loads(rv.data))
        self.output(fun)
        message = " GET Failed to return list of funs"
        self.assertTrue(len(loads(rv.data)) > 0, Routes['fun'] + message)
        self.assertFunModelEqual(fun, loads(rv.data)[-1],
                                 error_message=(Routes['fun'] + message))
        self.assertEqual(200, rv.status_code, Routes['fun'] +
                         " GET Failed to return list of funs")

    def testFunAPIGet(self):
        # insert a fun object
        fun = self.add_fun(100, year=1900)

        # invalid year
        expect = {'details': INVALID_ID, "message": FunDoesNotExist.message}
        self.getTest(Routes['fun'] + "/" + str(INVALID_ID),
                     FunDoesNotExist.status_code,
                     self.assertEqual,
                     expect,
                     error_message=Routes['fun'] + " Get: Invalid Fun")

        # valid year
        self.getTest(Routes['fun'] + "/" + str(fun['year']),
                     SUCCESSFUL_GET_CODE,
                     self.assertFunModelEqual,
                     fun,
                     error_message=Routes['fun'] + " Get: valid Fun")

    def testFunAPIDelete(self):
        # insert a fun object
        fun = self.add_fun(100, year=1900)

        # testing deleting a invalid fun year
        error_message = Routes['fun'] + "DELETE: valid fun"
        self.deleteValidTest(Routes['fun'],
                             FunDoesNotExist.status_code,
                             self.assertFunModelEqual,
                             fun['year'],
                             fun,
                             FunDoesNotExist.message,
                             error_message=error_message)

        # testing deleting invalid fun year
        error_message = Routes['fun'] + "DELETE: invalid fun"
        self.deleteInvalidTest(Routes['fun'],
                               FunDoesNotExist.status_code,
                               FunDoesNotExist.message,
                               error_message=error_message)

    def testFunAPIPut(self):
        # insert a fun object
        fun = self.add_fun(100, year=1900)
        updated_count = 50

        # invalid year
        params = {'count': updated_count}
        expect = {'details': INVALID_ID, "message": FunDoesNotExist.message}
        self.putTest(Routes['fun'] + "/" + str(INVALID_ID),
                     params,
                     FunDoesNotExist.status_code,
                     self.assertEqual,
                     expect,
                     error_message=Routes['fun'] + " Put: Invalid Fun"
                     )

        # valid year
        self.putTest(Routes['fun'] + "/" + str(fun['year']),
                     params,
                     SUCCESSFUL_PUT_CODE,
                     self.assertEqual,
                     None,
                     error_message=Routes['fun'] + " Put: valid Fun"
                     )
        fun['count'] = updated_count
        # now try to get it
        self.getTest(Routes['fun'] + "/" + str(fun['year']),
                     SUCCESSFUL_GET_CODE,
                     self.assertFunModelEqual,
                     fun,
                     error_message=Routes['fun'] + " Get: valid Fun")


class TestSponsor(TestSetup):
    def testSponsorInvalidPost(self):
        # Note Valid Requests are tested in BaseTest method add_sponsor
        # missing parameters
        params = {}
        result = {'message': {'sponsor_name': MISSING_PARAMETER}}
        error_message = (Routes['sponsor'] +
                        " POST: request with missing parameter")
        self.postInvalidTest(Routes['sponsor'],
                             params,
                             InvalidField.status_code,
                             self.assertEqual,
                             result,
                             error_message=error_message)

        # testing with improper name parameters
        params = {'sponsor_name': 1}
        result = {'details': 'Sponsor - name', 'message': InvalidField.message}
        error_message = (Routes['sponsor'] +
                        " POST: request with invalid parameters")
        self.postInvalidTest(Routes['sponsor'],
                             params,
                             InvalidField.status_code,
                             self.assertEqual,
                             result,
                             error_message=error_message)

    def testSponsorListAPI(self):
        # TODO pagination
        # add a sponsor
        sponsor = self.add_sponsor("New Sponsor")

        # test a get with sponsors
        rv = self.app.get(Routes['sponsor'])
        self.output(loads(rv.data)[-1])
        self.output(sponsor)
        self.assertTrue(len(loads(rv.data)) > 0,
                        Routes['sponsor'] +
                        " GET Failed to return list of sponsors")
        self.assertSponsorModelEqual(sponsor, loads(rv.data)[-1],
                                     error_message=Routes['sponsor'] +
                                     " GET Failed to return list of sponsors")
        self.assertEqual(200, rv.status_code, Routes['sponsor'] +
                         " GET Failed to return list of sponsrs")

    def testSponsorAPIGet(self):
        # insert a sponsor
        sponsor = self.add_sponsor("XXTEST")

        # invalid sponsor id
        expect = {'details': INVALID_ID,
                  "message": SponsorDoesNotExist.message}
        self.getTest(Routes['sponsor'] + "/" + str(INVALID_ID),
                     SponsorDoesNotExist.status_code,
                     self.assertEqual,
                     expect,
                     error_message=Routes['sponsor'] + " Get: Invalid Sponsor")

        # valid sponsor id
        self.getTest(Routes['sponsor'] + "/" + str(sponsor['sponsor_id']),
                     SUCCESSFUL_GET_CODE,
                     self.assertSponsorModelEqual,
                     sponsor,
                     error_message=Routes['sponsor'] + " Get: valid Sponsor")

    def testSponsorAPIDelete(self):
        # insert a sponsor
        sponsor = self.add_sponsor("XXTEST")

        # delete of invalid sponsor id
        error_message = Routes['sponsor'] + " DELETE Invalid Sponsor id "
        self.deleteValidTest(Routes['sponsor'],
                             SponsorDoesNotExist.status_code,
                             self.assertSponsorModelEqual,
                             sponsor['sponsor_id'],
                             sponsor,
                             SponsorDoesNotExist.message,
                             error_message=error_message)

        # delete valid sponsor id
        error_message = Routes['sponsor'] + " DELETE valid Sponsor id "
        self.deleteInvalidTest(Routes['sponsor'],
                               SponsorDoesNotExist.status_code,
                               SponsorDoesNotExist.message,
                               error_message=error_message)

    def testSponsorAPIPut(self):
        # insert a sponsor
        sponsor = self.add_sponsor("XXTEST")
        sponsor_updated_name = "YYTEST"

        # invalid sponsor id
        params = {'sponsor_name': 'New League'}
        expect = {'details': INVALID_ID,
                  'message': SponsorDoesNotExist.message}
        error_message = Routes['sponsor'] + " PUT: given invalid sponsor ID"
        self.putTest(Routes['sponsor'] + "/" + str(INVALID_ID),
                     params,
                     SponsorDoesNotExist.status_code,
                     self.assertEqual,
                     expect,
                     error_message=error_message
                     )

        # invalid parameters
        params = {'sponsor_name': 1}
        expect = {'details': "Sponsor - name",
                  'message': InvalidField.message}
        error_message = Routes['sponsor'] + " PUT: given invalid parameters"
        self.putTest(Routes['sponsor'] + "/" + str(sponsor['sponsor_id']),
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
        self.putTest(Routes['sponsor'] + "/" + str(sponsor['sponsor_id']),
                     params,
                     SUCCESSFUL_PUT_CODE,
                     self.assertEqual,
                     None,
                     error_message=error_message
                     )

        # now try to get it
        self.getTest(Routes['sponsor'] + "/" + str(sponsor['sponsor_id']),
                     SUCCESSFUL_GET_CODE,
                     self.assertSponsorModelEqual,
                     sponsor,
                     error_message=Routes['fun'] + " Get: valid Sponsor")


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
        # TODO pagination
        # proper insertion with post
        league = self.add_league("New League")

        # test a get with league
        rv = self.app.get(Routes['league'])
        self.output(loads(rv.data))
        self.assertTrue(len(loads(rv.data)) > 0,
                        Routes['league'] +
                        " GET: Failed to return list of leagues")
        self.assertLeagueModelEqual(league, loads(rv.data)[-1],
                                    error_message=Routes['league'] +
                                    " GET: Failed to return list of leagues")
        self.assertEqual(200, rv.status_code, Routes['league'] +
                         " GET: Failed to return list of leagues")

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
        # TODO Pagination
        # add a player
        player_one = self.add_player("Test Player",
                                     "TestPlayer@mlsb.ca",
                                     gender="M")
        rv = self.app.get(Routes['player'])
        player_list = loads(rv.data)
        self.assertTrue(len(player_list) > 0, Routes['player'] +
                        " GET: did not receive player list")
        self.assertPlayerModelEqual(player_one,
                                    player_list[-1],
                                    error_message=Routes['player'] +
                                    " GET: did not receive player list")

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
        result = {'details': player_two_email,
                  'message': NonUniqueEmail.message}
        error_message = Routes['player'] + ' PUT: Valid player update'
        self.putTest(Routes['player'] + "/" + str(player_one['player_id']),
                     params,
                     NonUniqueEmail.status_code,
                     self.assertEqual,
                     result,
                     error_message=error_message)


class TestTeam(TestSetup):
    def testTeamInvalidPost(self):
        # Note Valid Requests are tested in BaseTest method add_team
        # missing parameters
        params = {}
        result = {'message': {
                              'color': MISSING_PARAMETER,
                              'league_id': MISSING_PARAMETER,
                              'sponsor_id': MISSING_PARAMETER,
                              'year': MISSING_PARAMETER}
                  }
        error_message = (Routes['team'] +
                        " POST: request with missing parameter")
        self.postInvalidTest(Routes['team'],
                             params,
                             InvalidField.status_code,
                             self.assertEqual,
                             result,
                             error_message=error_message)

        sponsor = self.add_sponsor("New Sponsor")
        league = self.add_league("New League")

        # testing a all invalid color
        params = {'color': 1,
                  'sponsor_id': sponsor['sponsor_id'],
                  'league_id': league['league_id'],
                  'year': VALID_YEAR}
        result = {'details': 'Team - color', 'message': InvalidField.message}
        error_message = (Routes['team'] +
                        " POST: request with invalid color")
        self.postInvalidTest(Routes['team'],
                             params,
                             InvalidField.status_code,
                             self.assertEqual,
                             result,
                             error_message=error_message)

        # test invalid sponsor
        params = {'color': "Green",
                  'sponsor_id': INVALID_ID,
                  'league_id': league['league_id'],
                  'year': VALID_YEAR}
        result = {'details': INVALID_ID,
                  'message': SponsorDoesNotExist.message}
        error_message = (Routes['team'] +
                        " POST: request with invalid sponsor id")
        self.postInvalidTest(Routes['team'],
                             params,
                             SponsorDoesNotExist.status_code,
                             self.assertEqual,
                             result,
                             error_message=error_message)

        # test invalid league
        params = {'color': "Green",
                  'sponsor_id': sponsor['sponsor_id'],
                  'league_id': INVALID_ID,
                  'year': VALID_YEAR}
        result = {'details': INVALID_ID, 'message': LeagueDoesNotExist.message}
        error_message = (Routes['league'] +
                        " POST: request with invalid league id")
        self.postInvalidTest(Routes['team'],
                             params,
                             LeagueDoesNotExist.status_code,
                             self.assertEqual,
                             result,
                             error_message=error_message)

        # test invalid year
        params = {'color': "Green",
                  'sponsor_id': sponsor['sponsor_id'],
                  'league_id': league['league_id'],
                  'year': -1}
        result = {'details': 'Team - year', 'message': InvalidField.message}
        error_message = (Routes['team'] +
                        " POST: request with invalid year")
        self.postInvalidTest(Routes['team'],
                             params,
                             InvalidField.status_code,
                             self.assertEqual,
                             result,
                             error_message=error_message)

    def testTeamListAPI(self):
        # TODO Pagination
        # testing with all valid parameters
        sponsor = self.add_sponsor("New Sponsor")
        league = self.add_league("New League")
        team = self.add_team("Black", sponsor, league, VALID_YEAR)

        # test a get with team
        rv = self.app.get(Routes['team'])
        self.output(loads(rv.data))
        self.output(team)
        self.assertTeamModelEqual(team,
                                  loads(rv.data)[-1],
                                  error_message=Routes['team'] +
                                  " GET: Failed to return list of teams")
        self.assertEqual(200, rv.status_code, Routes['team'] +
                         " GET: Failed to return list of teams")

    def testTeamGet(self):

        # add a team
        sponsor = self.add_sponsor("New Sponsor")
        league = self.add_league("New league")
        team = self.add_team("Black", sponsor, league, year=VALID_YEAR)

        # invalid Team id
        expect = {'details': INVALID_ID, "message": TeamDoesNotExist.message}
        self.getTest(Routes['team'] + "/" + str(INVALID_ID),
                     TeamDoesNotExist.status_code,
                     self.assertEqual,
                     expect,
                     error_message=Routes['team'] + " Get: Invalid Team")

        # valid Team id
        self.getTest(Routes['team'] + "/" + str(team['team_id']),
                     SUCCESSFUL_GET_CODE,
                     self.assertTeamModelEqual,
                     team,
                     error_message=Routes['team'] + " Get: valid Team")

    def testTeamDelete(self):
        # add a team
        sponsor = self.add_sponsor("New Sponsor")
        league = self.add_league("New league")
        team = self.add_team("Black", sponsor, league, year=VALID_YEAR)

        # delete of invalid league id
        error_message = Routes['team'] + " DELETE Invalid team id "
        self.deleteValidTest(Routes['team'],
                             TeamDoesNotExist.status_code,
                             self.assertTeamModelEqual,
                             team['team_id'],
                             team,
                             TeamDoesNotExist.message,
                             error_message=error_message)

        # delete valid team id
        error_message = Routes['team'] + " DELETE valid team id "
        self.deleteInvalidTest(Routes['team'],
                               TeamDoesNotExist.status_code,
                               TeamDoesNotExist.message,
                               error_message=error_message)

    def testTeamPut(self):
        # add a team
        sponsor = self.add_sponsor("New Sponsor")
        league = self.add_league("New league")
        team = self.add_team("Black", sponsor, league, year=VALID_YEAR)
        invalid_route = Routes['team'] + '/' + str(INVALID_ID)
        valid_route = Routes['team'] + '/' + str(team['team_id'])

        # invalid team id
        params = {'sponsor_id': str(sponsor['sponsor_id']),
                  'league_id': str(league['league_id']),
                  'color': "Black",
                  'year': VALID_YEAR}
        expect = {'details': INVALID_ID, 'message': TeamDoesNotExist.message}
        error_message = Routes['team'] + " PUT: given invalid team ID"
        self.putTest(invalid_route,
                     params,
                     TeamDoesNotExist.status_code,
                     self.assertEqual,
                     expect,
                     error_message=error_message)

        # invalid sponsor_id
        params = {'sponsor_id': INVALID_ID,
                  'league_id': str(league['league_id']),
                  'color': "Black",
                  'year': VALID_YEAR}
        expect = {'details': INVALID_ID,
                  'message': SponsorDoesNotExist.message}
        error_message = Routes['team'] + " PUT: given invalid sponsor ID"
        self.putTest(valid_route,
                     params,
                     SponsorDoesNotExist.status_code,
                     self.assertEqual,
                     expect,
                     error_message=error_message)

        # invalid league_id
        params = {'sponsor_id': str(sponsor['sponsor_id']),
                  'league_id': INVALID_ID,
                  'color': "Black",
                  'year': VALID_YEAR}
        expect = {'details': INVALID_ID, 'message': LeagueDoesNotExist.message}
        error_message = Routes['team'] + " PUT: given invalid league ID"
        self.putTest(valid_route,
                     params,
                     LeagueDoesNotExist.status_code,
                     self.assertEqual,
                     expect,
                     error_message=error_message)

        # invalid color
        params = {'sponsor_id': str(sponsor['sponsor_id']),
                  'league_id': str(league['league_id']),
                  'color': 1,
                  'year': VALID_YEAR}
        expect = {'details': 'Team - color', 'message': InvalidField.message}
        error_message = Routes['team'] + " PUT: given invalid color"
        self.putTest(valid_route,
                     params,
                     InvalidField.status_code,
                     self.assertEqual,
                     expect,
                     error_message=error_message)

        # invalid year
        params = {'sponsor_id': str(sponsor['sponsor_id']),
                  'league_id': str(league['league_id']),
                  'color': "Black",
                  'year': -1}
        expect = {'details': 'Team - year', 'message': InvalidField.message}
        error_message = Routes['team'] + " PUT: given invalid year"
        self.putTest(valid_route,
                     params,
                     InvalidField.status_code,
                     self.assertEqual,
                     expect,
                     error_message=error_message)

        # successful update
        sponsor_two = self.add_sponsor("second sponsor")
        league_two = self.add_league("second league")

        # valid update
        params = {
                  'sponsor_id': sponsor_two['sponsor_id'],
                  'league_id': league_two['league_id'],
                  'color': "Black"}
        team['sponsor_id'] = sponsor_two['sponsor_id']
        team['league_id'] = league_two['league_id']
        error_message = Routes['team'] + " PUT: Failed to update a team"
        expect = None
        self.putTest(valid_route,
                     params,
                     SUCCESSFUL_PUT_CODE,
                     self.assertEqual,
                     expect,
                     error_message=error_message)


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
                              'time': MISSING_PARAMETER}}
        error_message = (Routes['game'] +
                        " POST: request with missing parameter")
        self.postInvalidTest(Routes['game'],
                             params,
                             InvalidField.status_code,
                             self.assertEqual,
                             expect,
                             error_message=error_message)

        # add two teams, a sponsor and a league
        league = self.add_league("New League")
        sponsor = self.add_sponsor("Sponsor")
        home_team = self.add_team("Black", sponsor, league, VALID_YEAR)
        away_team = self.add_team("White", sponsor, league, VALID_YEAR)

        # testing invalid date
        params = {
                  'home_team_id': home_team['team_id'],
                  'away_team_id': away_team['team_id'],
                  'date': "2014-02-2014",
                  'time': "22:40",
                  'league_id': league['league_id']
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
                  'league_id': league['league_id']
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
                  'league_id': league['league_id']
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
                  'league_id': league['league_id']
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

    def testGameListAPI(self):
        # TODO Pagination
        # add two teams, a sponsor and a league
        league = self.add_league("New League")
        sponsor = self.add_sponsor("Sponsor")
        home_team = self.add_team("Black", sponsor, league, VALID_YEAR)
        away_team = self.add_team("White", sponsor, league, VALID_YEAR)

        # add a game
        game = self.add_game("2014-02-10",
                             "22:40",
                             home_team,
                             away_team,
                             league)

        # test a get with game
        rv = self.app.get(Routes['game'])
        self.output(loads(rv.data))
        self.output(game)
        self.assertGameModelEqual(game,
                                  loads(rv.data)[-1],
                                  error_message=Routes['game'] +
                                  " GET: Failed to return list of games")
        self.assertEqual(200, rv.status_code, Routes['team'] +
                         " GET: Failed to return list of games")

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
        # TODO Pagination
        # add a game
        game = addGame(self)
        player = self.add_player("Test Player",
                                 "TestPLayer@mlsb.ca",
                                 gender="M")
        pass


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
        expect = {'details': str(INVALID_ID), 'message': TeamDoesNotExist.message}
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


def addGame(tester):
    # add two teams, a sponsor and a league
    counter = tester.get_counter()
    tester.increment_counter()
    league = tester.add_league("New League" + str(counter))
    sponsor = tester.add_sponsor("Sponsor" + str(counter))
    home_team = tester.add_team("Black" + str(counter),
                                sponsor,
                                league,
                                VALID_YEAR)
    away_team = tester.add_team("White" + str(counter),
                                sponsor,
                                league,
                                VALID_YEAR)
    game = tester.add_game("2014-02-10",
                           "22:40",
                           home_team,
                           away_team,
                           league)
    return game


def addBat(tester, classification):
    counter = tester.get_counter()
    tester.increment_counter()
    league = tester.add_league("New League" + str(counter))
    sponsor = tester.add_sponsor("Sponsor" + str(counter))
    home_team = tester.add_team("Black", sponsor, league, VALID_YEAR)
    away_team = tester.add_team("White", sponsor, league, VALID_YEAR)
    game = tester.add_game("2014-02-10",
                           "22:40",
                           home_team,
                           away_team,
                           league)
    player = tester.add_player("Test Player" + str(counter),
                               "TestPlayer" + str(counter) + "@mlsb.ca",
                               gender="M")
    bat = tester.add_bat(player, home_team, game, classification)
    return bat


def addEspy(tester, points):
    counter = tester.get_counter()
    tester.increment_counter()
    league = tester.add_league("New League" + str(counter))
    sponsor = tester.add_sponsor("Sponsor" + str(counter))
    team = tester.add_team("Black", sponsor, league, VALID_YEAR)
    espy = tester.add_espys(team, sponsor, points=points)
    return espy


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
