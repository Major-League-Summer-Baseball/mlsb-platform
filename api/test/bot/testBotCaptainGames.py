'''
@author: Dallas Fraser
@author: 2019-03-13
@organization: MLSB API
@summary: Tests all the bot captain games APIs
'''
from api.helper import loads
from api.routes import Routes
from api.model import Team
from base64 import b64encode
from api.test.BaseTest import TestSetup, ADMIN, PASSWORD, SUCCESSFUL_GET_CODE,\
                              addGame
headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' +
                                                  PASSWORD, "utf-8")
                                            ).decode("ascii")
}


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
