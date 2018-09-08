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
                         INVALID_ID
from api.testData import bat
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
        # Note Valid Requests are tested in BaseTest method add_fun

        # missing parameters
        params = {}
        rv = self.app.post(Routes['fun'], data=params, headers=headers)
        result = {'message': {'year': MISSING_PARAMETER}}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['fun'] +
                         " POST: POST request with missing parameter"
                         )
        self.assertEqual(rv.status_code, InvalidField.status_code,
                         Routes['fun'] +
                         " POST: POST request with invalid parameters")

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
        rv = self.app.put(Routes['fun'] + "/" + str(INVALID_ID),
                          data=params, headers=headers)
        expect = {'details': INVALID_ID, "message": FunDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['fun'] + " Put: Invalid Fun")
        self.assertEqual(FunDoesNotExist.status_code, rv.status_code,
                         Routes['fun'] + " Put: Invalid Fun")

        # valid year
        rv = self.app.put(Routes['fun'] + "/" + str(fun['year']),
                          data=params, headers=headers)
        expect = None
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['fun'] + " Put: valid Fun")
        self.assertEqual(200, rv.status_code,
                         Routes['fun'] + " Put: valid Fun")

        # now try to get it
        rv = self.app.get(Routes['fun'] + "/" + str(fun['year']))
        fun['count'] = updated_count
        self.output(loads(rv.data))
        self.output(fun)
        self.assertFunModelEqual(fun, loads(rv.data),
                                 error_message=(Routes['fun'] +
                                                " Get: valid Fun"))
        self.assertEqual(200, rv.status_code,
                         Routes['fun'] + " Get: valid Fun")

    def testFunAPIPost(self):
        pass


class TestSponsor(TestSetup):
    def testSponsorInvalidPost(self):
        # Note Valid Requests are tested in BaseTest method add_sponsor
        # missing parameters
        params = {}
        rv = self.app.post(Routes['sponsor'], data=params, headers=headers)
        result = {'message': {'sponsor_name': MISSING_PARAMETER}}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['sponsor'] +
                         " POST: POST request with missing parameter"
                         )
        self.assertEqual(rv.status_code, InvalidField.status_code,
                         Routes['sponsor'] +
                         " POST: POST request with invalid parameters")

        # testing with improper name parameters
        params = {'sponsor_name': 1}
        rv = self.app.post(Routes['sponsor'], data=params, headers=headers)
        result = {'details': 'Sponsor - name', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['sponsor'] +
                         " POST: POST request with invalid parameters")
        self.assertEqual(rv.status_code, InvalidField.status_code,
                         Routes['sponsor'] +
                         " POST: POST request with invalid parameters")

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
        rv = self.app.put(Routes['sponsor'] + '/' + str(INVALID_ID),
                          data=params, headers=headers)
        expect = {'details': INVALID_ID,
                  'message': SponsorDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['sponsor'] + " PUT: given invalid sponsor ID")
        self.assertEqual(SponsorDoesNotExist.status_code, rv.status_code,
                         Routes['sponsor'] + " PUT: given invalid sponsor ID")

        # invalid parameters
        params = {'sponsor_name': 1}
        rv = self.app.put(Routes['sponsor'] + '/' + str(sponsor['sponsor_id']),
                          data=params, headers=headers)
        expect = {'details': 'Sponsor - name', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['sponsor'] + " PUT: given invalid parameters")
        self.assertEqual(InvalidField.status_code, rv.status_code,
                         Routes['sponsor'] + " PUT: given invalid parameters")

        # successful update
        params = {'sponsor_name': sponsor_updated_name}
        sponsor['sponsor_name'] = sponsor_updated_name
        rv = self.app.put(Routes['sponsor'] + '/' + str(sponsor['sponsor_id']),
                          data=params,
                          headers=headers)
        result = None
        self.output(loads(rv.data))
        self.output(sponsor)
        self.assertEqual(result, loads(rv.data),
                         Routes['sponsor'] + " PUT: Failed to update Sponsor")
        self.assertEqual(200, rv.status_code,
                         Routes['sponsor'] + " PUT: Failed to update Sponsor")

        # now try to get it
        rv = self.app.get(Routes['sponsor'] + "/" + str(sponsor['sponsor_id']))
        self.output(loads(rv.data))
        self.output(sponsor)
        self.assertSponsorModelEqual(sponsor, loads(rv.data),
                                     error_message=(Routes['sponsor'] +
                                                    " Get: valid Fun"))
        self.assertEqual(200, rv.status_code,
                         Routes['fun'] + " Get: valid Fun")

    def testSponsorAPIPost(self):
        pass


class TestLeague(TestSetup):
    def testLeagueInvalidPost(self):
        # Note Valid Requests are tested in BaseTest method add_league
        # missing parameters
        params = {}
        rv = self.app.post(Routes['league'], data=params, headers=headers)
        result = {'message': {
                              'league_name': MISSING_PARAMETER
                              }
                  }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['league'] +
                         " POST: request with missing parameter")
        self.assertEqual(loads(rv.data), result, Routes['league'] +
                         " POST: request with missing parameter")

        # testing a league name parameter
        params = {'league_name': 1}
        rv = self.app.post(Routes['league'], data=params, headers=headers)
        result = {'details': 'League - name', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['league'] +
                         " POST: request with invalid league_name")
        self.assertEqual(rv.status_code, InvalidField.status_code,
                         Routes['league'] +
                         " POST: request with invalid league_name")

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
        rv = self.app.put(Routes['league'] + '/' + str(INVALID_ID),
                          data=params, headers=headers)
        result = {'details': INVALID_ID, 'message': LeagueDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['league'] +
                         ' PUT: Invalid league ID')
        self.assertEqual(rv.status_code, LeagueDoesNotExist.status_code,
                         Routes['league'] +
                         ' PUT: Invalid league ID')

        # invalid league_name type
        params = {'league_name': 1}
        rv = self.app.put(Routes['league'] + '/' + str(league['league_id']),
                          data=params, headers=headers)
        result = {'details': 'League - name', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['league'] +
                         ' PUT: Invalid parameters')
        self.assertEqual(rv.status_code, InvalidField.status_code,
                         Routes['league'] +
                         ' PUT: Invalid parameters')

        # successfully update
        league['league_name'] = "Updated league name"
        params = {'league_name': league['league_name']}
        rv = self.app.put(Routes['league'] + '/' + str(league['league_id']),
                          data=params, headers=headers)
        result = None
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['league'] +
                         ' PUT: Successful Update')
        self.assertEqual(rv.status_code, 200, Routes['league'] +
                         ' PUT: Successful Update')

    def testLeagueAPIPost(self):
        pass


class TestPlayer(TestSetup):
    def testPlayerInvalidPost(self):
        # Note Valid Requests are tested in BaseTest method add_player
        # missing parameters
        params = {}
        rv = self.app.post(Routes['player'], data=params, headers=headers)
        result = {'message': {
                              'player_name': MISSING_PARAMETER,
                              'email': MISSING_PARAMETER
                              }
                  }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         " POST: POST request with missing parameter"
                         )
        self.assertEqual(rv.status_code, 400, Routes['player'] +
                         " POST: POST request with missing parameter"
                         )

        # testing a gender parameter
        params = {'player_name': 'Dallas Fraser',
                  'gender': 'X',
                  'email': "new@mlsb.ca"}
        rv = self.app.post(Routes['player'], data=params, headers=headers)
        result = {'details': 'Player - gender',
                  'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         " POST: POST request with invalid gender"
                         )
        self.assertEqual(rv.status_code, InvalidField.status_code,
                         Routes['player'] +
                         " POST: POST request with invalid gender"
                         )

        # testing player_name parameter
        params = {'player_name': 1, 'gender': 'M', 'email': 'new@mlsb.ca'}
        rv = self.app.post(Routes['player'], data=params, headers=headers)
        result = {'details': 'Player - name', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         " POST: POST request with invalid name"
                         )
        self.assertEqual(rv.status_code, InvalidField.status_code,
                         Routes['player'] +
                         " POST: POST request with invalid name"
                         )

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
        rv = self.app.put(Routes['player'] + '/' + str(INVALID_ID),
                          data=params,
                          headers=headers)
        result = {'details': INVALID_ID, 'message': PlayerDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         ' PUT: Invalid Player ID')
        self.assertEqual(rv.status_code, PlayerDoesNotExist.status_code,
                         Routes['player'] +
                         ' PUT: Invalid Player ID')

        # invalid player_name type
        params = {'player_name': 1, 'gender': "F"}
        rv = self.app.put(Routes['player'] + "/" + str(player['player_id']),
                          data=params, headers=headers)
        result = {'details': 'Player - name', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         ' PUT: Invalid Player name')
        self.assertEqual(rv.status_code, InvalidField.status_code,
                         Routes['player'] +
                         ' PUT: Invalid Player name')
        # invalid gender
        params = {'player_name': "David Duchovny", 'gender': "X"}
        rv = self.app.put(Routes['player'] + "/" + str(player['player_id']),
                          data=params, headers=headers)
        result = {'details': 'Player - gender',
                  'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         ' PUT: Invalid Player gender')
        self.assertEqual(rv.status_code, InvalidField.status_code,
                         Routes['player'] +
                         ' PUT: Invalid Player gender')

        # successfully update
        params = {'player_name': "David Duchovny", 'gender': "F"}
        rv = self.app.put(Routes['player'] + "/" + str(player['player_id']),
                          data=params, headers=headers)
        result = None
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         ' PUT: Valid player update')
        self.assertEqual(rv.status_code, 200, Routes['player'] +
                         ' PUT: Valid player update')

    def testPlayerApiPutDuplicateEmail(self):
        # add two player
        player_one = self.add_player("Test Player",
                                     "TestPlayer@mlsb.ca",
                                     gender="M")
        player_two_email = "TestPlayerTwo@mlsb.ca"
        self.add_player("Test Player", player_two_email, gender="M")

        # try to update the first player to have the same email as the second
        params = {'email': player_two_email}
        rv = self.app.put(Routes['player'] + '/' +
                          str(player_one['player_id']),
                          data=params, headers=headers)
        result = {'details': player_two_email,
                  'message': NonUniqueEmail.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         ' PUT: Valid player update')
        self.assertEqual(rv.status_code, NonUniqueEmail.status_code,
                         Routes['player'] +
                         ' PUT: Valid player update')

    def testPlayerAPIPost(self):
            pass


class TestTeam(TestSetup):
    def testTeamInvalidPost(self):
        # Note Valid Requests are tested in BaseTest method add_team
        # missing parameters
        params = {}
        rv = self.app.post(Routes['team'], data=params, headers=headers)
        result = {'message': {
                              'color': MISSING_PARAMETER,
                              'league_id': MISSING_PARAMETER,
                              'sponsor_id': MISSING_PARAMETER,
                              'year': MISSING_PARAMETER}
                  }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['team'] +
                         " POST: request with missing parameter"
                         )
        self.assertEqual(rv.status_code, 400, Routes['team'] +
                         " POST: request with missing parameter"
                         )
        sponsor = self.add_sponsor("New Sponsor")
        league = self.add_league("New League")

        # testing a all invalid color
        params = {'color': 1,
                  'sponsor_id': sponsor['sponsor_id'],
                  'league_id': league['league_id'],
                  'year': VALID_YEAR}
        rv = self.app.post(Routes['team'], data=params, headers=headers)
        result = {'details': 'Team - color', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['team'] +
                         " POST: request with invalid parameters")
        self.assertEqual(rv.status_code, InvalidField.status_code,
                         Routes['team'] +
                         " POST: request with invalid parameters")

        # test invalid sponsor
        params = {'color': "Green",
                  'sponsor_id': INVALID_ID,
                  'league_id': league['league_id'],
                  'year': VALID_YEAR}
        rv = self.app.post(Routes['team'], data=params, headers=headers)
        result = {'details': INVALID_ID,
                  'message': SponsorDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['team'] +
                         " POST: request with invalid parameters")
        self.assertEqual(rv.status_code, SponsorDoesNotExist.status_code,
                         Routes['team'] +
                         " POST: request with invalid parameters")

        # test invalid league
        params = {'color': "Green",
                  'sponsor_id': sponsor['sponsor_id'],
                  'league_id': INVALID_ID,
                  'year': VALID_YEAR}
        rv = self.app.post(Routes['team'], data=params, headers=headers)
        result = {'details': INVALID_ID, 'message': LeagueDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['team'] +
                         " POST: request with invalid parameters")
        self.assertEqual(rv.status_code, LeagueDoesNotExist.status_code,
                         Routes['team'] +
                         " POST: request with invalid parameters")

        # test invalid year
        params = {'color': "Green",
                  'sponsor_id': sponsor['sponsor_id'],
                  'league_id': league['league_id'],
                  'year': -1}
        rv = self.app.post(Routes['team'], data=params, headers=headers)
        result = {'details': 'Team - year', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['team'] +
                         " POST: request with invalid parameters")
        self.assertEqual(rv.status_code, InvalidField.status_code,
                         Routes['team'] +
                         " POST: request with invalid parameters")

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

        # invalid team id
        params = {'sponsor_id': str(sponsor['sponsor_id']),
                  'league_id': str(league['league_id']),
                  'color': "Black",
                  'year': VALID_YEAR}
        rv = self.app.put(Routes['team'] + '/' + str(INVALID_ID),
                          data=params, headers=headers)
        expect = {'details': INVALID_ID, 'message': TeamDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['team'] + " PUT: given invalid team ID")
        self.assertEqual(TeamDoesNotExist.status_code, rv.status_code,
                         Routes['team'] + " PUT: given invalid team ID")

        # invalid sponsor_id
        params = {'sponsor_id': INVALID_ID,
                  'league_id': str(league['league_id']),
                  'color': "Black",
                  'year': VALID_YEAR}
        rv = self.app.put(Routes['team'] + '/' + str(team['team_id']),
                          data=params, headers=headers)
        expect = {'details': INVALID_ID,
                  'message': SponsorDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['team'] + " PUT: given invalid sponsor")
        self.assertEqual(SponsorDoesNotExist.status_code, rv.status_code,
                         Routes['team'] + " PUT: given invalid sponsor")

        # invalid league_id
        params = {'sponsor_id': str(sponsor['sponsor_id']),
                  'league_id': INVALID_ID,
                  'color': "Black",
                  'year': VALID_YEAR}
        rv = self.app.put(Routes['team'] + '/' + str(team['team_id']),
                          data=params, headers=headers)
        expect = {'details': INVALID_ID, 'message': LeagueDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['team'] + " PUT: given invalid sponsor")
        self.assertEqual(LeagueDoesNotExist.status_code, rv.status_code,
                         Routes['team'] + " PUT: given invalid league")

        # invalid color
        params = {'sponsor_id': str(sponsor['sponsor_id']),
                  'league_id': str(league['league_id']),
                  'color': 1,
                  'year': VALID_YEAR}
        rv = self.app.put(Routes['team'] + '/' + str(team['team_id']),
                          data=params, headers=headers)
        expect = {'details': 'Team - color', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['team'] + " PUT: given invalid color")
        self.assertEqual(InvalidField.status_code, rv.status_code,
                         Routes['team'] + " PUT: given invalid color")

        # invalid year
        params = {'sponsor_id': str(sponsor['sponsor_id']),
                  'league_id': str(league['league_id']),
                  'color': "Black",
                  'year': -1}
        rv = self.app.put(Routes['team'] + '/' + str(team['team_id']),
                          data=params, headers=headers)
        expect = {'details': 'Team - year', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['team'] + " PUT: given invalid year")
        self.assertEqual(InvalidField.status_code, rv.status_code,
                         Routes['team'] + " PUT: given invalid year")

        # successful update
        sponsor_two = self.add_sponsor("second sponsor")
        league_two = self.add_league("second league")

        # valid update
        params = {
                  'sponsor_id': sponsor_two['sponsor_id'],
                  'league_id': league_two['league_id'],
                  'color': "Black"}
        rv = self.app.put(Routes['team'] + '/' + str(team['team_id']),
                          data=params, headers=headers)
        expect = None
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, Routes['team'] +
                         " PUT: Failed to update a team")
        self.assertEqual(rv.status_code, 200, Routes['team'] +
                         " PUT: Failed to update a team")


class TestGame(TestSetup):
    def testGameInvalidPost(self):
        # Note Valid Requests are tested in BaseTest method add_game
        # missing parameters
        params = {}
        rv = self.app.post(Routes['game'], data=params, headers=headers)
        expect = {'message': {
                              'away_team_id': MISSING_PARAMETER,
                              'date': MISSING_PARAMETER,
                              'home_team_id': MISSING_PARAMETER,
                              'league_id': MISSING_PARAMETER,
                              'time': MISSING_PARAMETER}}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['game'] +
                         " POST: request with missing parameters")
        self.assertEqual(400, rv.status_code, Routes['game'] +
                         " POST: request with missing parameters")

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
        rv = self.app.post(Routes['game'], data=params, headers=headers)
        expect = {'details': 'Game - date', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['game'] +
                         " POST: request with invalid date")
        self.assertEqual(InvalidField.status_code, rv.status_code,
                         Routes['game'] +
                         " POST: request with invalid date")

        # testing invalid time
        params = {
                  'home_team_id': home_team['team_id'],
                  'away_team_id': away_team['team_id'],
                  'date': "2014-02-10",
                  'time': "22:66",
                  'league_id': league['league_id']
                              }
        rv = self.app.post(Routes['game'], data=params, headers=headers)
        expect = {'details': 'Game - time', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['game'] +
                         " POST: request with invalid time")
        self.assertEqual(InvalidField.status_code, rv.status_code,
                         Routes['game'] + " POST: request with invalid time")

        # testing invalid home team id
        params = {
                  'home_team_id': INVALID_ID,
                  'away_team_id': away_team['team_id'],
                  'date': "2014-02-10",
                  'time': "22:40",
                  'league_id': league['league_id']
                              }
        rv = self.app.post(Routes['game'], data=params, headers=headers)
        expect = {'details': INVALID_ID, 'message': TeamDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['game'] +
                         " POST: request with invalid home team")
        self.assertEqual(TeamDoesNotExist.status_code, rv.status_code,
                         Routes['game'] +
                         " POST: request with invalid home team")

        # testing invalid away team id
        params = {
                  'home_team_id': home_team['team_id'],
                  'away_team_id': INVALID_ID,
                  'date': "2014-02-10",
                  'time': "22:40",
                  'league_id': league['league_id']
                              }
        rv = self.app.post(Routes['game'], data=params, headers=headers)
        expect = {'details': INVALID_ID, 'message': TeamDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['game'] +
                         " POST: request with invalid away team")
        self.assertEqual(TeamDoesNotExist.status_code, rv.status_code,
                         Routes['game'] +
                         " POST: request with invalid away team")

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
        rv = self.app.put(Routes['game'] + "/" + str(INVALID_ID),
                          data=params, headers=headers)
        expect = {'details': INVALID_ID, 'message': GameDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['game'] + " PUT: invalid game id")
        self.assertEqual(GameDoesNotExist.status_code, rv.status_code,
                         Routes['game'] + " PUT: invalid game id")

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
        rv = self.app.put(Routes['game'] + "/" + str(game['game_id']),
                          data=params, headers=headers)
        expect = {'details': INVALID_ID, 'message': TeamDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['game'] + " PUT: invalid home team")
        self.assertEqual(TeamDoesNotExist.status_code, rv.status_code,
                         Routes['game'] + " PUT: invalid home team")

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
        rv = self.app.put(Routes['game'] + "/" + str(game['game_id']),
                          data=params, headers=headers)
        expect = {'details': INVALID_ID, 'message': TeamDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['game'] + " PUT: invalid away team")
        self.assertEqual(TeamDoesNotExist.status_code, rv.status_code,
                         Routes['game'] + " PUT: invalid away team")

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
        rv = self.app.put(Routes['game'] + "/" + str(game['game_id']),
                          data=params, headers=headers)
        expect = {'details': INVALID_ID, 'message': LeagueDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['game'] + " PUT: invalid league")
        self.assertEqual(LeagueDoesNotExist.status_code, rv.status_code,
                         Routes['game'] + " PUT: invalid league")

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
        rv = self.app.put(Routes['game'] + "/" + str(game['game_id']),
                          data=params, headers=headers)
        expect = {'details': 'Game - date', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['game'] + " PUT: invalid date")
        self.assertEqual(InvalidField.status_code, rv.status_code,
                         Routes['game'] + " PUT: invalid date")

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
        rv = self.app.put(Routes['game'] + "/" + str(game['game_id']),
                          data=params, headers=headers)
        expect = {'details': 'Game - time', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['game'] + " PUT: invalid time")
        self.assertEqual(InvalidField.status_code, rv.status_code,
                         Routes['game'] + " PUT: invalid time")

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
        rv = self.app.put(Routes['game'] + "/" + str(game['game_id']),
                          data=params, headers=headers)
        expect = {'details': 'Game - status', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['game'] + " PUT: invalid status")
        self.assertEqual(InvalidField.status_code, rv.status_code,
                         Routes['game'] + " PUT: invalid status")

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
        rv = self.app.put(Routes['game'] + "/" + str(game['game_id']),
                          data=params, headers=headers)
        expect = {'details': 'Game - field', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['game'] + " PUT: invalid field")
        self.assertEqual(InvalidField.status_code, rv.status_code,
                         Routes['game'] + " PUT: invalid field")

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
        rv = self.app.put(Routes['game'] + "/" + str(game['game_id']),
                          data=params, headers=headers)
        expect = None
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['game'] + " PUT: valid update")
        self.assertEqual(200, rv.status_code,
                         Routes['game'] + " PUT: valid update")


class TestBat(TestSetup):
    def testBateInvalidPost(self):
        # Note Valid Requests are tested in BaseTest method add_bat
        # missing parameters
        game = addGame(self)
        player = self.add_player("Test Player",
                                 "TestPLayer@mlsb.ca",
                                 gender="M")
        params = {}
        rv = self.app.post(Routes['bat'], data=params, headers=headers)
        expect = {
                  'message': {
                              'game_id': MISSING_PARAMETER,
                              'hit': MISSING_PARAMETER,
                              'player_id': MISSING_PARAMETER,
                              'team_id': MISSING_PARAMETER
                              }
                  }
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['bat'] +
                         " POST: request with missing parameters")
        self.assertEqual(400, rv.status_code, Routes['bat'] +
                         " POST: request with missing parameters")

        # testing invalid player
        params = {
                  'game_id': game['game_id'],
                  'player_id': INVALID_ID,
                  'team_id': game['home_team_id'],
                  'rbi': 2,
                  'hit': "hr",
                  'inning': 1
                              }
        rv = self.app.post(Routes['bat'], data=params, headers=headers)
        expect = {'details': INVALID_ID, 'message': PlayerDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['bat'] +
                         " POST: request with invalid player")
        self.assertEqual(PlayerDoesNotExist.status_code, rv.status_code,
                         Routes['bat'] +
                         " POST: request with invalid player")

        # testing invalid game
        params = {
                  'game_id': INVALID_ID,
                  'player_id': player['player_id'],
                  'team_id': game['home_team_id'],
                  'rbi': 2,
                  'hit': "hr",
                  'inning': 1
                              }
        rv = self.app.post(Routes['bat'], data=params, headers=headers)
        expect = {'details': INVALID_ID, 'message': GameDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['bat'] +
                         " POST: request with invalid game")
        self.assertEqual(GameDoesNotExist.status_code, rv.status_code,
                         Routes['bat'] +
                         " POST: request with invalid game")

        # testing invalid team
        params = {
                  'game_id': game['game_id'],
                  'player_id': player['player_id'],
                  'team_id': INVALID_ID,
                  'rbi': 2,
                  'hit': "hr",
                  'inning': 1
                              }
        rv = self.app.post(Routes['bat'], data=params, headers=headers)
        expect = {'details': str(INVALID_ID), 'message': TeamDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['bat'] +
                         " POST: request with invalid team")
        self.assertEqual(TeamDoesNotExist.status_code, rv.status_code,
                         Routes['bat'] +
                         " POST: request with invalid team")
        # testing invalid rbi
        params = {
                  'game_id': INVALID_ID,
                  'player_id': player['player_id'],
                  'team_id': game['home_team_id'],
                  'rbi': 100,
                  'hit': "hr",
                  'inning': 1
                              }
        rv = self.app.post(Routes['bat'], data=params, headers=headers)
        expect = {'details': 'Bat - rbi', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['bat'] +
                         " POST: request with invalid rbi")
        self.assertEqual(InvalidField.status_code, rv.status_code,
                         Routes['bat'] +
                         " POST: request with invalid rbi")
        # testing invalid inning
        params = {
                  'game_id': INVALID_ID,
                  'player_id': player['player_id'],
                  'team_id': game['home_team_id'],
                  'rbi': 1,
                  'hit': "hr",
                  'inning': -1
                              }
        rv = self.app.post(Routes['bat'], data=params, headers=headers)
        expect = {'details': 'Bat - inning', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['bat'] +
                         " POST: request with invalid inning")
        self.assertEqual(InvalidField.status_code, rv.status_code,
                         Routes['bat'] +
                         " POST: request with invalid inning")
        # testing invalid hit
        params = {
                  'game_id': INVALID_ID,
                  'player_id': player['player_id'],
                  'team_id': game['home_team_id'],
                  'rbi': 1,
                  'hit': "xx",
                  'inning': 1
                              }
        rv = self.app.post(Routes['bat'], data=params, headers=headers)
        expect = {'details': 'Bat - hit', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['bat'] +
                         " POST: request with invalid hit")
        self.assertEqual(InvalidField.status_code, rv.status_code,
                         Routes['bat'] +
                         " POST: request with invalid hit")

    def testBatList(self):
        # TODO Pagination
        # add a game
        game = addGame(self)
        player = self.add_player("Test Player",
                                 "TestPLayer@mlsb.ca",
                                 gender="M")

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

        # invalid bat ID
        params = {
                  'game_id': bat['game_id'],
                  'player_id': bat['player_id'],
                  'team_id': bat['team_id'],
                  'rbi': 4,
                  'hit': "HR",
                  'inning': 1}
        rv = self.app.put(Routes['bat'] + "/" + str(INVALID_ID),
                          data=params, headers=headers)
        expect = {'details': INVALID_ID, 'message': BatDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['bat'] + " PUT: invalid Bat id")
        self.assertEqual(BatDoesNotExist.status_code, rv.status_code,
                         Routes['bat'] + " PUT: invalid Bat id")
        # test invalid game_id
        params = {
                  'game_id': bat['game_id'],
                  'player_id': bat['player_id'],
                  'team_id': bat['team_id'],
                  'rbi': 4,
                  'hit': "HR",
                  'inning': 1}
        params = {
                  'game_id': -1,
                  'player_id': 1,
                  'team_id': 1,
                  'rbi': 4,
                  'hit': "HR",
                  'inning': 1
                              }
        rv = self.app.put(Routes['bat'] + "/" + str(bat['bat_id']),
                          data=params, headers=headers)
        expect = {'details': -1, 'message': GameDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['bat'] + " PUT: invalid game")
        self.assertEqual(GameDoesNotExist.status_code, rv.status_code,
                         Routes['bat'] + " PUT: invalid game")
        # test invalid game_id
        params = {
                  'game_id': bat['game_id'],
                  'player_id': bat['player_id'],
                  'team_id': bat['team_id'],
                  'rbi': 4,
                  'hit': "HR",
                  'inning': 1}
        params = {
                  'game_id': 1,
                  'player_id': -1,
                  'team_id': 1,
                  'rbi': 4,
                  'hit': "HR",
                  'inning': 1
                              }
        rv = self.app.put(Routes['bat'] + "/" + str(bat['bat_id']),
                          data=params, headers=headers)
        expect = {'details': -1, 'message': PlayerDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['bat'] + " PUT: invalid player")
        self.assertEqual(PlayerDoesNotExist.status_code, rv.status_code,
                         Routes['bat'] + " PUT: invalid player")
        # test invalid game_id
        params = {
                  'game_id': bat['game_id'],
                  'player_id': bat['player_id'],
                  'team_id': bat['team_id'],
                  'rbi': 4,
                  'hit': "HR",
                  'inning': 1}
        params = {
                  'game_id': 1,
                  'player_id': 1,
                  'team_id': -1,
                  'rbi': 4,
                  'hit': "HR",
                  'inning': 1
                              }
        rv = self.app.put(Routes['bat'] + "/1", data=params, headers=headers)
        expect = {'details': '-1', 'message': TeamDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['bat'] + " PUT: invalid team")
        self.assertEqual(TeamDoesNotExist.status_code, rv.status_code,
                         Routes['bat'] + " PUT: invalid team")
        # test invalid rbi
        params = {
                  'game_id': bat['game_id'],
                  'player_id': bat['player_id'],
                  'team_id': bat['team_id'],
                  'rbi': 4,
                  'hit': "HR",
                  'inning': 1}
        params = {
                  'game_id': 1,
                  'player_id': 1,
                  'team_id': 1,
                  'rbi': 99,
                  'hit': "HR",
                  'inning': 1
                              }
        rv = self.app.put(Routes['bat'] + "/" + str(bat['bat_id']),
                          data=params, headers=headers)
        expect = {'details': 'Bat - rbi', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['bat'] + " PUT: invalid rbi")
        self.assertEqual(InvalidField.status_code, rv.status_code,
                         Routes['bat'] + " PUT: invalid rbi")
        # test invalid hit
        params = {
                  'game_id': bat['game_id'],
                  'player_id': bat['player_id'],
                  'team_id': bat['team_id'],
                  'rbi': 4,
                  'hit': "HR",
                  'inning': 1}
        params = {
                  'game_id': 1,
                  'player_id': 1,
                  'team_id': 1,
                  'rbi': 4,
                  'hit': "XX",
                  'inning': 1
                              }
        rv = self.app.put(Routes['bat'] + "/" + str(bat['bat_id']),
                          data=params, headers=headers)
        expect = {'details': 'Bat - hit', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['bat'] + " PUT: invalid hit")
        self.assertEqual(InvalidField.status_code, rv.status_code,
                         Routes['bat'] + " PUT: invalid hit")
        # test invalid inning
        params = {
                  'game_id': bat['game_id'],
                  'player_id': bat['player_id'],
                  'team_id': bat['team_id'],
                  'rbi': 4,
                  'hit': "HR",
                  'inning': 1}
        params = {
                  'game_id': 1,
                  'player_id': 1,
                  'team_id': 1,
                  'rbi': 4,
                  'hit': "hr",
                  'inning': -1
                              }
        rv = self.app.put(Routes['bat'] + "/" + str(bat['bat_id']),
                          data=params, headers=headers)
        expect = {'details': 'Bat - inning', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['bat'] + " PUT: invalid inning")
        self.assertEqual(InvalidField.status_code, rv.status_code,
                         Routes['bat'] + " PUT: invalid inning")
        # valid update
        params = {
                  'game_id': 1,
                  'player_id': 1,
                  'team_id': 1,
                  'rbi': 4,
                  'hit': "HR",
                  'inning': 1
                              }
        rv = self.app.put(Routes['bat'] + "/" + str(bat['bat_id']),
                          data=params, headers=headers)
        expect = None
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['bat'] + " PUT: valid parameters")
        self.assertEqual(200, rv.status_code,
                         Routes['bat'] + " PUT: valid parameters")


class TestEspys(TestSetup):
    def testEspysApiGet(self):
        # proper insertion
        self.addEspys()
        # invalid player id
        rv = self.app.get(Routes['espy'] + "/100")
        result = {'details': 100, 'message': EspysDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['espy'] +
                         " GET invalid espy id")
        self.assertEqual(rv.status_code, EspysDoesNotExist.status_code,
                         Routes['espy'] + " GET invalid espy id")
        # valid user
        d = datetime.today().strftime("%Y-%m-%d")
        t = datetime.today().strftime("%H:%M")
        rv = self.app.get(Routes['espy'] + "/1")
        result = {'date': d,
                  'description': 'Kik transaction',
                  'espy_id': 1,
                  'points': 1.0,
                  'receipt': None,
                  'sponsor': None,
                  'team': 'Domus Green',
                  'time': t}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['espy'] +
                         " GET valid espy id")
        self.assertEqual(rv.status_code, 200, Routes['espy'] +
                         " GET valid player id")
        rv = self.app.get(Routes['espy'] + "/2")
        d = datetime.today().strftime("%Y-%m-%d")
        t = datetime.today().strftime("%H:%M")
        result = {'date': d,
                  'description': 'Purchase',
                  'espy_id': 2,
                  'points': 2.0,
                  'receipt': '12019209129',
                  'sponsor': 'Domus',
                  'team': 'Chainsaw Black',
                  'time': t}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['espy'] +
                         " GET valid espy id")
        self.assertEqual(rv.status_code, 200, Routes['espy'] +
                         " GET valid player id")

    def testEspysApiDelete(self):
        # proper insertion with post
        self.addEspys()
        # delete of invalid espy id
        rv = self.app.delete(Routes['espy'] + "/100", headers=headers)
        result = {'details': 100, 'message': EspysDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['espy'] +
                         " DELETE Invalid espy id ")
        self.assertEqual(rv.status_code, EspysDoesNotExist.status_code,
                         Routes['espy'] + " DELETE Invalid espy id ")
        rv = self.app.delete(Routes['espy'] + "/1", headers=headers)
        result = None
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['espy'] +
                         ' DELETE Valid espy id')
        self.assertEqual(rv.status_code, 200, Routes['espy'] +
                         ' DELETE Valid espy id')

    def testEspysApiPut(self):
        # must add a espy
        self.addEspys()
        # invalid espy id
        params = {'team_id': 1,
                  'sponsor_id': 1,
                  'description': "Transaction",
                  'points': 10,
                  'receipt': "212309"}
        rv = self.app.put(Routes['espy'] + '/100',
                          data=params, headers=headers)
        result = {'details': 100, 'message': EspysDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['espy'] +
                         ' PUT: Invalid espy ID')
        self.assertEqual(rv.status_code, EspysDoesNotExist.status_code,
                         Routes['espy'] + ' PUT: Invalid espy ID')
        # invalid team id
        params = {'team_id': 100,
                  'sponsor_id': 1,
                  'description': "Transaction",
                  'points': 10,
                  'receipt': "212309"}
        rv = self.app.put(Routes['espy'] + '/1', data=params, headers=headers)
        result = {'details': 100, 'message': TeamDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['espy'] +
                         ' PUT: Invalid espy team')
        self.assertEqual(rv.status_code, TeamDoesNotExist.status_code,
                         Routes['player'] + ' PUT: Invalid espy team')
        # invalid sponsor id
        params = {'team_id': 1,
                  'sponsor_id': 100,
                  'description': "Transaction",
                  'points': 10,
                  'receipt': "212309"}
        rv = self.app.put(Routes['espy'] + '/1', data=params, headers=headers)
        result = {'details': 100, 'message': SponsorDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['espy'] +
                         ' PUT: Invalid sponsor for Espy')
        self.assertEqual(rv.status_code, SponsorDoesNotExist.status_code,
                         Routes['espy'] + ' PUT: Invalid sponsor Espy')
        # successfully update
        params = {'team_id': 1,
                  'sponsor_id': 1,
                  'description': "Transaction",
                  'points': 10,
                  'receipt': "212309"}
        rv = self.app.put(Routes['espy'] + '/1', data=params, headers=headers)
        result = None
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['espy'] +
                         ' PUT: Valid espy update')
        self.assertEqual(rv.status_code, 200, Routes['espy'] +
                         ' PUT: Valid espy update')

    def testEspysApiPost(self):
        # test an empty get
        rv = self.app.get(Routes['espy'])
        empty = loads(rv.data)
        self.assertEqual([], empty, Routes['espy'] +
                         " GET: did not return empty list")
        self.assertEqual(rv.status_code, 200, Routes['espy'] +
                         " GET: did not return empty list")
        # missing parameters
        params = {}
        rv = self.app.post(Routes['espy'], data=params, headers=headers)
        result = {'message': {
                              'points': MISSING_PARAMETER,
                              'team_id': MISSING_PARAMETER
                              }
                  }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['espy'] +
                         " POST: POST request with missing parameter"
                         )
        self.assertEqual(rv.status_code, 400, Routes['espy'] +
                         " POST: POST request with missing parameter"
                         )
        # testing a team id parameter
        self.addTeams()
        params = {'team_id': 100,
                  'sponsor_id': 1,
                  'points': 5}
        rv = self.app.post(Routes['espy'], data=params, headers=headers)
        result = {'details': 100, 'message': TeamDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['espy'] +
                         " POST: POST request with invalid team")
        self.assertEqual(rv.status_code, TeamDoesNotExist.status_code,
                         Routes['espy'] +
                         " POST: POST request with invalid team")
        # testing sponsor id parameter
        params = {'team_id': 1,
                  'sponsor_id': 100,
                  'points': 5}
        rv = self.app.post(Routes['espy'], data=params, headers=headers)
        result = {'details': 100, 'message': SponsorDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['espy'] +
                         " POST: POST request with invalid sponsor"
                         )
        self.assertEqual(rv.status_code, SponsorDoesNotExist.status_code,
                         Routes['espy'] +
                         " POST: POST request with invalid sponsor")
        # testing points parameter
        params = {'team_id': 1,
                  'sponsor_id': 100,
                  'points': "XX"}
        rv = self.app.post(Routes['espy'], data=params, headers=headers)
        result = {'details': 'Game - points', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['espy'] +
                         " POST: POST request with invalid points")
        self.assertEqual(rv.status_code, InvalidField.status_code,
                         Routes['espy'] +
                         " POST: POST request with invalid points")
        # proper insertion with post
        params = {'team_id': 1,
                  'sponsor_id': 1,
                  'points': 1}
        rv = self.app.post(Routes['espy'], data=params, headers=headers)
        result = 1
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['espy'] +
                         " POST: POST request with valid data")
        self.assertEqual(rv.status_code, 201, Routes['espy'] +
                         " POST: POST request with valid data")
        rv = self.app.get(Routes['espy'])
        empty = loads(rv.data)
        d = datetime.today().strftime("%Y-%m-%d")
        t = datetime.today().strftime("%H:%M")
        expect = [{'date': d,
                   'description': None,
                   'espy_id': 1,
                   'points': 1.0,
                   'receipt': None,
                   'sponsor': 'Domus',
                   'team': 'Domus Green',
                   'time': t}]
        self.output(empty)
        self.output(expect)
        self.assertEqual(expect, empty, Routes['espy'] +
                         " GET: did not receive espy list")


def addGame(tester):
    # add two teams, a sponsor and a league
    league = tester.add_league("New League")
    sponsor = tester.add_sponsor("Sponsor")
    home_team = tester.add_team("Black", sponsor, league, VALID_YEAR)
    away_team = tester.add_team("White", sponsor, league, VALID_YEAR)
    game = tester.add_game("2014-02-10",
                           "22:40",
                           home_team,
                           away_team,
                           league)
    return game


def addBat(tester, classification):
    league = tester.add_league("New League")
    sponsor = tester.add_sponsor("Sponsor")
    home_team = tester.add_team("Black", sponsor, league, VALID_YEAR)
    away_team = tester.add_team("White", sponsor, league, VALID_YEAR)
    game = tester.add_game("2014-02-10",
                           "22:40",
                           home_team,
                           away_team,
                           league)
    player = tester.add_player("Test Player", "TestPlayer@mlsb.ca", gender="M")
    bat = tester.add_bat(player, home_team, game, classification)
    return bat


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
