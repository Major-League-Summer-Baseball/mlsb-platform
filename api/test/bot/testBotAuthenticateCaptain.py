'''
@author: Dallas Fraser
@author: 2019-03-13
@organization: MLSB API
@summary: Tests all the bot authenticate captain APIs
'''
from api.helper import loads
from api.routes import Routes
from base64 import b64encode
from api.test.BaseTest import \
    TestSetup, ADMIN, PASSWORD, INVALID_ID, \
    VALID_YEAR, SUCCESSFUL_GET_CODE, UNAUTHORIZED
from api.errors import TeamDoesNotExist, NotTeamCaptain
headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' +
                                                  PASSWORD, "utf-8")
                                            ).decode("ascii")
}


class testAuthenticateCaptain(TestSetup):

    def testMain(self):
        """Tests whether the API can authenticate if a person is captain"""
        # add some background
        league = self.add_league("Test Bot League")
        sponsor = self.add_sponsor("Test Bot Sponsor")
        team = self.add_team("Black", sponsor, league, VALID_YEAR)
        player = self.add_player("Test Captain", "testBot@mlsb.ca", "m")
        self.add_player_to_team(team, player, captain=True)

        # valid request
        data = {'player_id': player['player_id'],
                'team': team['team_id']}
        expect = team['team_id']
        rv = self.app.post(Routes['botcaptain'], json=data, headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        error = Routes['botcaptain'] + " POST: Authenticate Captain"
        self.assertEqual(rv.status_code, SUCCESSFUL_GET_CODE, error)
        self.assertEqual(expect, loads(rv.data), error)

        # invalid team
        data = {'player_id': player['player_id'],
                'team': INVALID_ID}
        expect = {'details': INVALID_ID, 'message': TeamDoesNotExist.message}
        rv = self.app.post(Routes['botcaptain'], json=data, headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        error = Routes['botcaptain'] + " POST: invalid team"
        self.assertEqual(rv.status_code, TeamDoesNotExist.status_code, error)
        self.assertEqual(expect, loads(rv.data), error)

        # captain name does not match
        player_two = self.add_player("Test Two", "testBot2@mlsb.ca", "m")
        data = {'player_id': player_two['player_id'],
                'team': team['team_id']}
        expect = {'details': player['player_name'],
                  'message': NotTeamCaptain.message}
        rv = self.app.post(Routes['botcaptain'], json=data, headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        error = Routes['botcaptain'] + " POST: name of captain does not match"
        self.assertEqual(rv.status_code,
                         NotTeamCaptain.status_code,
                         error)
        self.assertEqual(expect, loads(rv.data), error)

        # invalid credentials
        data = {'player_id': player['player_id'],
                'team': team['team_id']}
        rv = self.app.post(Routes['botcaptain'], json=data, headers={})
        error = Routes['botcaptain'] + " POST: invalid credentials"
        self.assertEqual(rv.status_code, UNAUTHORIZED, error)
