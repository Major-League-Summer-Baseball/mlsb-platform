'''
@author: Dallas Fraser
@author: 2019-03-13
@organization: MLSB API
@summary: Tests all the bot submit scores APIs
'''
from api.helper import loads
from api.routes import Routes
from api.model import Team
from base64 import b64encode
from api.test.BaseTest import TestSetup, ADMIN, PASSWORD, INVALID_ID,\
    addGame
from api.errors import PlayerNotSubscribed, GameDoesNotExist,\
    InvalidField
headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' +
                                                  PASSWORD, "utf-8")
                                            ).decode("ascii")
}


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
        rv = self.app.post(route, json=data, headers=headers)
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
        rv = self.app.post(route, json=data, headers=headers)
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
        rv = self.app.post(route, json=data, headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        error = Routes['botsubmitscore'] + " POST: more hr than runs"
        self.assertEqual(rv.status_code, InvalidField.status_code, error)
        self.assertEqual(expect, loads(rv.data), error)

        # normal request
        self.submit_a_score(player, game, 1, hr=[player['player_id']])
