'''
@author: Dallas Fraser
@author: 2017-05-03
@organization: MLSB API
@summary: Tests all the bot APIs
'''
import unittest
from api.helper import loads
from api import DB
from api.routes import Routes
from api.model import Player, Espys
from api.credentials import ADMIN, PASSWORD
from base64 import b64encode
from datetime import date, datetime, timedelta
from api.BaseTest import TestSetup
from api.errors import TeamDoesNotExist, NotTeamCaptain,\
                       TeamAlreadyHasCaptain,\
                       PlayerNotSubscribed, GameDoesNotExist,\
                       InvalidField, SponsorDoesNotExist, PlayerDoesNotExist
headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' +
                                                  PASSWORD, "utf-8")
                                            ).decode("ascii")
}


class testAuthenticateCaptain(TestSetup):
    def testMain(self):
        self.addCaptainToTeam()
        # valid request
        data = {
                "player_id": 1,
                "team": 1
                }
        expect = 1
        rv = self.app.post(Routes['botcaptain'], data=data, headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, 200, Routes['botcaptain'] +
                         " POST: Authenticate Captain"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['botcaptain'] + " Post: Authenticate Captain")
        # invalid team
        data = {
                "player_id": 1,
                "team": -1
                }
        expect = {'details': -1, 'message': TeamDoesNotExist.message}
        rv = self.app.post(Routes['botcaptain'], data=data, headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, TeamDoesNotExist.status_code,
                         Routes['botcaptain'] +
                         " POST: invalid team"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['botcaptain'] + " Post: invalid team")
        # captain name does not match
        data = {
                "player_id": 2,
                "team": 1
                }
        expect = {'details': 'Dallas Fraser',
                  'message': NotTeamCaptain.message}
        rv = self.app.post(Routes['botcaptain'], data=data, headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, NotTeamCaptain.status_code,
                         Routes['botcaptain'] +
                         " POST: name of captain does not match"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['botcaptain'] +
                         " Post: name of captain does not match")
        # if someone else tries to say captain with same name but different
        # bot name than one previously stated
        data = {
                'player_id': 2,
                "team": 1
                }
        expect = {'details': 'frase2560',
                  'message': TeamAlreadyHasCaptain.message}
        rv = self.app.post(Routes['botcaptain'], data=data, headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, TeamAlreadyHasCaptain.status_code,
                         Routes['botcaptain'] +
                         " POST: sketchy shit"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['botcaptain'] + " Post: sketchy shit")
        # invalid credentials
        data = {
                'player_id': 3,
                "team": 1
                }
        rv = self.app.post(Routes['botcaptain'], data=data, headers={})
        self.assertEqual(rv.status_code, 401, Routes['botcaptain'] +
                         " POST: invalid credentials"
                         )


class testSubmitScores(TestSetup):
    def testMain(self):
        self.mockScoreSubmission()
        # invalid captain
        data = {
                "player_id": 1,
                'game_id': 1,
                'score': 1,
                'hr': [1, 2],
                'ss': []
                }
        expect = {'details': 'frase2560',
                  'message': PlayerNotSubscribed.message}
        rv = self.app.post(Routes['botsubmitscore'],
                           data=data,
                           headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, PlayerNotSubscribed.status_code,
                         Routes['botsubmitscore'] +
                         " POST: invalid bot user name"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['botsubmitscore'] +
                         " POST: invalid bot user name")
        player = Player.query.get(1)
        player.bot = "frase2560"  # add the bot name to the captain
        DB.session.commit()
        # invalid game
        data = {
                "player_id": 1,
                'game_id': -1,
                'score': 1,
                'hr': [1, 2],
                'ss': []
                }
        expect = {'details': -1, 'message': GameDoesNotExist.message}
        rv = self.app.post(Routes['botsubmitscore'],
                           data=data,
                           headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, GameDoesNotExist.status_code,
                         Routes['botsubmitscore'] +
                         " POST: invalid game id"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['botsubmitscore'] + " POST: invalid game id")
        # more hr than runs scored
        data = {
                "player_id": 1,
                'game_id': 1,
                'score': 1,
                'hr': [1, 2],
                'ss': []
                }
        expect = {'details': 'More hr than score',
                  'message': InvalidField.message}
        rv = self.app.post(Routes['botsubmitscore'],
                           data=data,
                           headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, InvalidField.status_code,
                         Routes['botsubmitscore'] +
                         " POST: more hr than runs"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['botsubmitscore'] + " POST: more hr than runs")
        # normal request
        data = {
                "player_id": 1,
                'game_id': 1,
                'score': 5,
                'hr': [1, 2],
                'ss': []
                }
        expect = True
        rv = self.app.post(Routes['botsubmitscore'],
                           data=data,
                           headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, 200, Routes['botsubmitscore'] +
                         " POST: valid request"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['botsubmitscore'] + " POST: valid request")
        # game = Game.query.get(1)
        # print(game.summary())
        # used to check the runs went through


class testCaptainGames(TestSetup):
    def testMain(self):
        self.mockScoreSubmission()
        # valid request
        data = {
                "player_id": 1,
                "team": 1
                }
        expect = [{'away_team': 'Chainsaw Black',
                   'away_team_id': 2,
                   'date': '2014-08-23',
                   'field': '',
                   'game_id': 1,
                   'home_team': 'Domus Green',
                   'home_team_id': 1,
                   'league_id': 1,
                   'status': '',
                   'time': '11:37'}]
        rv = self.app.post(Routes['botcaptaingames'],
                           data=data,
                           headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, 200, Routes['botcaptaingames'] +
                         " POST: Valid Captain's games"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['botcaptain'] +
                         " Post: Invalid Captain's games")
        # submit score
        data = {
                "player_id": 1,
                'game_id': 1,
                'score': 5,
                'hr': [1, 2],
                'ss': []
                }
        expect = True
        rv = self.app.post(Routes['botsubmitscore'],
                           data=data,
                           headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, 200, Routes['botsubmitscore'] +
                         " POST: valid request"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['botsubmitscore'] + " POST: valid request")
        # second valid request
        data = {
                "player_id": 1,
                "team": 1
                }
        expect = []
        rv = self.app.post(Routes['botcaptaingames'],
                           data=data,
                           headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, 200, Routes['botcaptaingames'] +
                         " POST: Invalid Captain's games"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['botcaptain'] +
                         " Post: Invalid Captain's games")


class testUpcomingGames(TestSetup):
    def testMain(self):
        # non-subscribed player
        self.mockUpcomingGames()
        data = {
                'player_id': 'DoesNotExist'
                }
        expect = {'details': 'DoesNotExist',
                  'message': PlayerDoesNotExist.message}
        rv = self.app.post(Routes['botupcominggames'],
                           data=data,
                           headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, PlayerDoesNotExist.status_code,
                         Routes['botupcominggames'] +
                         " POST: Player DNE for upcoming games"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['botupcominggames'] +
                         " Post: Unsubscribed player for upcoming games")
        # subscribed player upcoming games
        data = {
                'player_id': 1
                }
        d = date.today().strftime("%Y-%m-%d")
        d2 = (date.today() + timedelta(1)).strftime("%Y-%m-%d")
        d3 = (date.today() + timedelta(5)).strftime("%Y-%m-%d")
        expect = [{'away_team': 'Chainsaw Black',
                   'away_team_id': 2,
                   'date': d,
                   'field': '',
                   'game_id': 1,
                   'home_team': 'Domus Green',
                   'home_team_id': 1,
                   'league_id': 1,
                   'status': '',
                   'time': '11:45'},
                  {'away_team': 'Domus Green',
                   'away_team_id': 1,
                   'date': d2,
                   'field': '',
                   'game_id': 2,
                   'home_team': 'Chainsaw Black',
                   'home_team_id': 2,
                   'league_id': 1,
                   'status': '',
                   'time': '11:45'},
                  {'away_team': 'Chainsaw Black',
                   'away_team_id': 2,
                   'date': d3,
                   'field': '',
                   'game_id': 3,
                   'home_team': 'Domus Green',
                   'home_team_id': 1,
                   'league_id': 1,
                   'status': '',
                   'time': '11:45'}]
        rv = self.app.post(Routes['botupcominggames'],
                           data=data,
                           headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, 200, Routes['botupcominggames'] +
                         " POST: Subscribed player for upcoming games"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['botupcominggames'] +
                         " Post: Unsubscribed player for upcoming games")

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
