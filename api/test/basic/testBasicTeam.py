from base64 import b64encode
from api.routes import Routes
from api.errors import \
    SponsorDoesNotExist, InvalidField, TeamDoesNotExist, LeagueDoesNotExist
from api.test.BaseTest import \
    TestSetup, ADMIN, PASSWORD, SUCCESSFUL_GET_CODE, \
    INVALID_ID, SUCCESSFUL_PUT_CODE, VALID_YEAR


headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' +
                                                  PASSWORD, "utf-8")
                                            ).decode("ascii")
}
MISSING_PARAMETER = ('Missing required parameter in the JSON body ' +
                     'or the post body or the query string')


class TestTeam(TestSetup):

    def testTeamInvalidPost(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # Note Valid Requests are tested in BaseTest method add_team
            # missing parameters
            params = {}
            result = {
                'message': {
                    'color': MISSING_PARAMETER,
                    'league_id': MISSING_PARAMETER,
                    'sponsor_id': MISSING_PARAMETER,
                    'year': MISSING_PARAMETER
                }
            }
            error_message = (
                Routes['team'] + " POST: request with missing parameter"
            )
            self.postInvalidTest(
                Routes['team'],
                params,
                InvalidField.status_code,
                self.assertEqual,
                result,
                error_message=error_message
            )

            sponsor = self.add_sponsor("New Sponsor")
            league = self.add_league("New League")

            # testing a all invalid color
            params = {
                'color': 1,
                'sponsor_id': sponsor['sponsor_id'],
                'league_id': league['league_id'],
                'year': VALID_YEAR
            }
            result = {
                'details': 'Team - color', 'message': InvalidField.message
            }
            error_message = (
                Routes['team'] + " POST: request with invalid color"
            )
            self.postInvalidTest(
                Routes['team'],
                params,
                InvalidField.status_code,
                self.assertEqual,
                result,
                error_message=error_message
            )

            # test invalid sponsor
            params = {
                'color': "Green",
                'sponsor_id': INVALID_ID,
                'league_id': league['league_id'],
                'year': VALID_YEAR
            }
            result = {
                'details': INVALID_ID,
                'message': SponsorDoesNotExist.message
            }
            error_message = (
                Routes['team'] + " POST: request with invalid sponsor id"
            )
            self.postInvalidTest(
                Routes['team'],
                params,
                SponsorDoesNotExist.status_code,
                self.assertEqual,
                result,
                error_message=error_message
            )

            # test invalid league
            params = {
                'color': "Green",
                'sponsor_id': sponsor['sponsor_id'],
                'league_id': INVALID_ID,
                'year': VALID_YEAR
            }
            result = {
                'details': INVALID_ID, 'message': LeagueDoesNotExist.message
            }
            error_message = (
                Routes['league'] + " POST: request with invalid league id"
            )
            self.postInvalidTest(
                Routes['team'],
                params,
                LeagueDoesNotExist.status_code,
                self.assertEqual,
                result,
                error_message=error_message
            )

            # test invalid year
            params = {
                'color': "Green",
                'sponsor_id': sponsor['sponsor_id'],
                'league_id': league['league_id'],
                'year': -1
            }
            result = {
                'details': 'Team - year', 'message': InvalidField.message
            }
            error_message = (
                Routes['team'] + " POST: request with invalid year"
            )
            self.postInvalidTest(
                Routes['team'],
                params,
                InvalidField.status_code,
                self.assertEqual,
                result,
                error_message=error_message
            )

    def testTeamListAPI(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # testing with all valid parameters
            sponsor = self.add_sponsor("New Sponsor")
            league = self.add_league("New League")
            self.add_team("Black", sponsor, league, VALID_YEAR)

            # test a get with teams
            error_message = (
                Routes['team'] + " GET Failed to return list of teams"
            )
            self.getListTest(Routes['team'], error_message=error_message)

    def testTeamGet(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # add a team
            sponsor = self.add_sponsor("New Sponsor")
            league = self.add_league("New league")
            team = self.add_team("Black", sponsor, league, year=VALID_YEAR)

            # invalid Team id
            expect = {
                'details': INVALID_ID, "message": TeamDoesNotExist.message
            }
            self.getTest(
                Routes['team'] + "/" + str(INVALID_ID),
                TeamDoesNotExist.status_code,
                self.assertEqual,
                expect,
                error_message=Routes['team'] + " Get: Invalid Team"
            )

            # valid Team id
            self.getTest(
                Routes['team'] + "/" + str(team['team_id']),
                SUCCESSFUL_GET_CODE,
                self.assertTeamModelEqual,
                team,
                error_message=Routes['team'] + " Get: valid Team"
            )

    def testTeamDelete(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # add a team
            sponsor = self.add_sponsor("New Sponsor")
            league = self.add_league("New league")
            team = self.add_team("Black", sponsor, league, year=VALID_YEAR)

            # delete of invalid league id
            error_message = Routes['team'] + " DELETE Invalid team id "
            self.deleteValidTest(
                Routes['team'],
                TeamDoesNotExist.status_code,
                self.assertTeamModelEqual,
                team['team_id'],
                team,
                TeamDoesNotExist.message,
                error_message=error_message
            )

            # delete valid team id
            error_message = Routes['team'] + " DELETE valid team id "
            self.deleteInvalidTest(
                Routes['team'],
                TeamDoesNotExist.status_code,
                TeamDoesNotExist.message,
                error_message=error_message
            )

    def testTeamPut(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # add a team
            sponsor = self.add_sponsor("New Sponsor")
            league = self.add_league("New league")
            team = self.add_team("Black", sponsor, league, year=VALID_YEAR)
            invalid_route = Routes['team'] + '/' + str(INVALID_ID)
            valid_route = Routes['team'] + '/' + str(team['team_id'])

            # invalid team id
            params = {
                'sponsor_id': str(sponsor['sponsor_id']),
                'league_id': str(league['league_id']),
                'color': "Black",
                'year': VALID_YEAR
            }
            expect = {
                'details': INVALID_ID, 'message': TeamDoesNotExist.message
            }
            error_message = Routes['team'] + " PUT: given invalid team ID"
            self.putTest(
                invalid_route,
                params,
                TeamDoesNotExist.status_code,
                self.assertEqual,
                expect,
                error_message=error_message
            )

            # invalid sponsor_id
            params = {
                'sponsor_id': INVALID_ID,
                'league_id': str(league['league_id']),
                'color': "Black",
                'year': VALID_YEAR
            }
            expect = {
                'details': INVALID_ID,
                'message': SponsorDoesNotExist.message
            }
            error_message = Routes['team'] + " PUT: given invalid sponsor ID"
            self.putTest(
                valid_route,
                params,
                SponsorDoesNotExist.status_code,
                self.assertEqual,
                expect,
                error_message=error_message
            )

            # invalid league_id
            params = {
                'sponsor_id': str(sponsor['sponsor_id']),
                'league_id': INVALID_ID,
                'color': "Black",
                'year': VALID_YEAR
            }
            expect = {
                'details': INVALID_ID, 'message': LeagueDoesNotExist.message
            }
            error_message = Routes['team'] + " PUT: given invalid league ID"
            self.putTest(
                valid_route,
                params,
                LeagueDoesNotExist.status_code,
                self.assertEqual,
                expect,
                error_message=error_message
            )

            # invalid color
            params = {
                'sponsor_id': str(sponsor['sponsor_id']),
                'league_id': str(league['league_id']),
                'color': 1,
                'year': VALID_YEAR
            }
            expect = {
                'details': 'Team - color', 'message': InvalidField.message
            }
            error_message = Routes['team'] + " PUT: given invalid color"
            self.putTest(
                valid_route,
                params,
                InvalidField.status_code,
                self.assertEqual,
                expect,
                error_message=error_message
            )

            # invalid year
            params = {
                'sponsor_id': str(sponsor['sponsor_id']),
                'league_id': str(league['league_id']),
                'color': "Black",
                'year': -1
            }
            expect = {
                'details': 'Team - year', 'message': InvalidField.message
            }
            error_message = Routes['team'] + " PUT: given invalid year"
            self.putTest(
                valid_route,
                params,
                InvalidField.status_code,
                self.assertEqual,
                expect,
                error_message=error_message
            )

            # successful update
            sponsor_two = self.add_sponsor("second sponsor")
            league_two = self.add_league("second league")

            # valid update
            params = {
                'sponsor_id': sponsor_two['sponsor_id'],
                'league_id': league_two['league_id'],
                'color': "Black"
            }
            team['sponsor_id'] = sponsor_two['sponsor_id']
            team['league_id'] = league_two['league_id']
            error_message = Routes['team'] + " PUT: Failed to update a team"
            expect = None
            self.putTest(
                valid_route,
                params,
                SUCCESSFUL_PUT_CODE,
                self.assertEqual,
                expect,
                error_message=error_message
            )
