'''
@author: Dallas Fraser
@author: 2017-05-03
@organization: MLSB API
@summary: Tests all the bot APIs
'''
from api.helper import loads
from api.routes import Routes
from api.model import Team
from base64 import b64encode
from api.BaseTest import TestSetup, ADMIN, PASSWORD, INVALID_ID, VALID_YEAR,\
                         SUCCESSFUL_GET_CODE, UNAUTHORIZED, addGame
from api.errors import TeamDoesNotExist, NotTeamCaptain,\
                       PlayerNotSubscribed, GameDoesNotExist,\
                       InvalidField,  PlayerDoesNotExist
import unittest
import datetime
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
        rv = self.app.post(Routes['botcaptain'], data=data, headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        error = Routes['botcaptain'] + " POST: Authenticate Captain"
        self.assertEqual(rv.status_code, SUCCESSFUL_GET_CODE, error)
        self.assertEqual(expect, loads(rv.data), error)

        # invalid team
        data = {'player_id': player['player_id'],
                'team': INVALID_ID}
        expect = {'details': INVALID_ID, 'message': TeamDoesNotExist.message}
        rv = self.app.post(Routes['botcaptain'], data=data, headers=headers)
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
        rv = self.app.post(Routes['botcaptain'], data=data, headers=headers)
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
        rv = self.app.post(Routes['botcaptain'], data=data, headers={})
        error = Routes['botcaptain'] + " POST: invalid credentials"
        self.assertEqual(rv.status_code, UNAUTHORIZED, error)


class testSubmitScores(TestSetup):
    def testMain(self):
        # add some background
        game = addGame(self)
        team_model = Team.query.get(game['home_team_id'])
        team = team_model.json()
        player = self.add_player("Test Bot Captain", "testbot@mlsb.ca", "m")
        self.add_player_to_team(team, player, captain=True)
        route = Routes['botsubmitscore']

        # invalid captain
        data = {'player_id': INVALID_ID,
                'game_id': game['game_id'],
                'score': 1,
                'hr': [player['player_id']],
                'ss': []}
        expect = {'details': INVALID_ID,
                  'message': PlayerNotSubscribed.message}
        rv = self.app.post(route, data=data, headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        error = Routes['botsubmitscore'] + " POST: invalid bot user name"
        code = PlayerNotSubscribed.status_code
        self.assertEqual(rv.status_code, code, error)
        self.assertEqual(expect, loads(rv.data), error)

        # invalid game
        data = {'player_id': player['player_id'],
                'game_id': INVALID_ID,
                'score': 1,
                'hr': [player['player_id']],
                'ss': []}
        expect = {'details': INVALID_ID, 'message': GameDoesNotExist.message}
        rv = self.app.post(route, data=data, headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        error = Routes['botsubmitscore'] + " POST: invalid game id"
        self.assertEqual(rv.status_code, GameDoesNotExist.status_code, error)
        self.assertEqual(expect, loads(rv.data), error)

        # more hr than runs scored
        data = {'player_id': player['player_id'],
                'game_id': game['game_id'],
                'score': 1,
                'hr': [player['player_id'], player['player_id']],
                'ss': []}
        expect = {'details': 'More hr than score',
                  'message': InvalidField.message}
        rv = self.app.post(route, data=data, headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        error = Routes['botsubmitscore'] + " POST: more hr than runs"
        self.assertEqual(rv.status_code, InvalidField.status_code, error)
        self.assertEqual(expect, loads(rv.data), error)

        # normal request
        self.submit_a_score(player, game, 1, hr=[player['player_id']])


class testCaptainGames(TestSetup):
    def testMain(self):

        # add some background
        game = addGame(self)
        team_model = Team.query.get(game['home_team_id'])
        team = team_model.json()
        player = self.add_player("Test Bot Captain", "testbot@mlsb.ca", "m")
        self.add_player_to_team(team, player, captain=True)
        route = Routes['botcaptaingames']

        # valid request
        data = {'player_id': player['player_id'],
                'team': team['team_id']}
        rv = self.app.post(route, data=data, headers=headers)
        self.output(loads(rv.data))
        self.output(game)
        error = Routes['botcaptaingames'] + " POST: Valid Captain's games"
        self.assertTrue(len(loads(rv.data)) > 0, error)
        self.assertEqual(rv.status_code, SUCCESSFUL_GET_CODE, error)
        self.assertGameModelEqual(game, loads(rv.data)[0], error)

        # submit score
        self.submit_a_score(player, game, 1, hr=[player['player_id']])

        # second valid request
        data = {'player_id': player['player_id'],
                'team': team['team_id']}
        expect = []
        rv = self.app.post(route, data=data, headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        error = Routes['botcaptaingames'] + " POST: Invalid Captain's games"
        self.assertEqual(rv.status_code, SUCCESSFUL_GET_CODE, error)
        self.assertEqual(expect, loads(rv.data), error)


class testUpcomingGames(TestSetup):
    def testMain(self):
        # non-subscribed player
        day = datetime.date.today() + datetime.timedelta(days=1)
        game = addGame(self, day=day.strftime("%Y-%m-%d"), time="22:40")
        team_model = Team.query.get(game['home_team_id'])
        team = team_model.json()
        player = self.add_player("Test Bot Captain", "testbot@mlsb.ca", "m")
        self.add_player_to_team(team, player, captain=True)
        route = Routes['botupcominggames']

        # invalid player id
        data = {'player_id': INVALID_ID}
        expect = {'details': INVALID_ID,
                  'message': PlayerDoesNotExist.message}
        rv = self.app.post(route, data=data, headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        error = route + " POST: Player DNE for upcoming games"
        self.assertEqual(rv.status_code, PlayerDoesNotExist.status_code, error)
        self.assertEqual(expect, loads(rv.data), error)

        # subscribed player upcoming games
        data = {'player_id': player['player_id']}
        expect = [{'away_team': game['away_team'],
                   'away_team_id': game['away_team_id'],
                   'date': game['date'],
                   'field': game['field'],
                   'game_id': game['game_id'],
                   'home_team': game['home_team'],
                   'home_team_id': game['home_team_id'],
                   'league_id': game['league_id'],
                   'status': game['status'],
                   'time': game['time']}]
        rv = self.app.post(Routes['botupcominggames'],
                           data=data,
                           headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        error = route + " POST: Subscribed player for upcoming games"
        self.assertEqual(rv.status_code, SUCCESSFUL_GET_CODE, error)
        self.assertEqual(expect, loads(rv.data), error)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
