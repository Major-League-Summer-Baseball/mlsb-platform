'''
@author: Dallas Fraser
@author: 2016-04-12
@organization: MLSB API
@summary: Tests all the Kik APIs
'''
from api.helper import loads
from api import DB
from api.routes import Routes
from api.model import Player, Espys
from api.credentials import ADMIN, PASSWORD, KIK, KIKPW
from datetime import date
from base64 import b64encode
from api.errors import TDNESC, PNOT, GDNESC, PNS, SDNESC
headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' + PASSWORD, "utf-8")).decode("ascii")
}

kik = {
    'Authorization': 'Basic %s' % b64encode(bytes(KIK + ':' + KIKPW, "utf-8")).decode("ascii")
}
from api.BaseTest import TestSetup

class testAuthenticateCaptain(TestSetup):
    def testMain(self):
        self.addCaptainToTeam()
        # valid request
        data = {
                'kik': "frase2560",
                "captain": "Dallas Fraser",
                "team": 1
                }
        expect = 1
        rv = self.app.post(Routes['kikcaptain'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, 200, Routes['kikcaptain'] +
                         " POST: Authenticate Captain"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kikcaptain'] + " Post: Authenticate Captain")
        # invalid team
        data = {
                'kik': "frase2560",
                "captain": "Dallas Fraser",
                "team": -1
                }
        expect = "Team does not exist"
        rv = self.app.post(Routes['kikcaptain'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, TDNESC, Routes['kikcaptain'] +
                         " POST: invalid team"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kikcaptain'] + " Post: invalid team")
        # captain name does not match
        data = {
                'kik': "frase2560",
                "captain": "Fucker",
                "team": 1
                }
        expect = "Name of captain does not match"
        rv = self.app.post(Routes['kikcaptain'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, 401, Routes['kikcaptain'] +
                         " POST: name of captain does not match"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kikcaptain'] + " Post: name of captain does not match")
        # if someone else tries to say captain with same name but different
        # kik name than one previously stated
        data = {
                'kik': "fucker",
                "captain": "Dallas Fraser",
                "team": 1
                }
        expect = "Captain was authenticate under different kik name before"
        rv = self.app.post(Routes['kikcaptain'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, 401, Routes['kikcaptain'] +
                         " POST: sketchy shit"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kikcaptain'] + " Post: sketchy shit")
        # invalid credentials
        data = {
                'kik': "fucker",
                "captain": "Dallas Fraser",
                "team": 1
                }
        rv = self.app.post(Routes['kikcaptain'], data=data, headers=headers)
        self.assertEqual(rv.status_code, 401, Routes['kikcaptain'] +
                         " POST: invalid credentials"
                         )

class testSubscribe(TestSetup):
    def testMain(self):
        self.addPlayersToTeam()
        # valid request
        data = {
                'kik': "frase2560",
                "name": "Dallas Fraser",
                "team": 1
                }
        expect = True
        rv = self.app.post(Routes['kiksubscribe'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, 200, Routes['kikcaptain'] +
                         " POST: valid request"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kiksubscribe'] + " Post: subscribe")
        # team does not exist
        data = {
                'kik': "frase2560",
                "name": "Dallas Fraser",
                "team": -1
                }
        expect = {'message': 'Team does not Exist -1'}
        rv = self.app.post(Routes['kiksubscribe'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, TDNESC, Routes['kikcaptain'] +
                         " POST: team does not exist"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kiksubscribe'] + " Post: team does not exist")
        # player not on team
        data = {
                'kik': "frase2560",
                "name": "fucker",
                "team": 1
                }
        expect = {'message': 'Player fucker not on team Domus Green'}
        rv = self.app.post(Routes['kiksubscribe'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, PNOT, Routes['kikcaptain'] +
                         " POST: player not on team"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kiksubscribe'] + " Post: player not on team")
        # player already subscribed
        data = {
                'kik': "frase2560",
                "name": "Dallas Fraser",
                "team": 1
                }
        expect = True
        rv = self.app.post(Routes['kiksubscribe'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, 200, Routes['kikcaptain'] +
                         " POST: already subscribed"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kiksubscribe'] + " Post: already subscribed")
        espys = Espys.query.all()
        # check to make sure not additional points were rewarded
        expect = [{'points': 2, 'receipt': None, 'espy_id': 1,
                   'description': 'Dallas Fraser email:fras2560@mylaurier.ca SUBSCRIBED',
                   'sponsor': None, 'team': 'Domus Green'},
                  {'points': 0, 'receipt': None, 'espy_id': 2,
                   'description': 'Dallas Fraser email:fras2560@mylaurier.ca SUBSCRIBED',
                   'sponsor': None, 'team': 'Domus Green'}
                  ]
        for index, espy in enumerate(espys):
            self.output(espy.json())
            self.assertEqual(espy.json(), expect[index])
        # invalid credentials
        data = {
                'kik': "fucker",
                "captain": "Dallas Fraser",
                "team": 1
                }
        rv = self.app.post(Routes['kiksubscribe'], data=data, headers=headers)
        self.assertEqual(rv.status_code, 401, Routes['kiksubscribe'] +
                         " POST: invalid credentials"
                         )

class testSubmitScores(TestSetup):
    def testMain(self):
        self.mockScoreSubmission()
        # invalid captain
        data = {
                'kik': "frase2560",
                'game_id': 1,
                'score': 1,
                'hr': [1, 2],
                'ss': []
                }
        expect = 'Kik name does not match'
        rv = self.app.post(Routes['kiksubmitscore'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, 404, Routes['kiksubmitscore'] +
                         " POST: invalid kik user name"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kiksubmitscore'] + " POST: invalid kik user name")
        player = Player.query.get(1)
        player.kik = "frase2560" # add the kik name to the captain
        DB.session.commit()
        # invalid game
        data = {
                'kik': "frase2560",
                'game_id': -1,
                'score': 1,
                'hr': [1, 2],
                'ss': []
                }
        expect = 'Game not found'
        rv = self.app.post(Routes['kiksubmitscore'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, GDNESC, Routes['kiksubmitscore'] +
                         " POST: invalid game id"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kiksubmitscore'] + " POST: invalid game id")
        # more hr than runs scored
        data = {
                'kik': "frase2560",
                'game_id': 1,
                'score': 1,
                'hr': [1, 2],
                'ss': []
                }
        expect = 'More hr than runs'
        rv = self.app.post(Routes['kiksubmitscore'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, 400, Routes['kiksubmitscore'] +
                         " POST: more hr than runs"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kiksubmitscore'] + " POST: more hr than runs")
        # normal request
        data = {
                'kik': "frase2560",
                'game_id': 1,
                'score': 5,
                'hr': [1, 2],
                'ss': []
                }
        expect = True
        rv = self.app.post(Routes['kiksubmitscore'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, 200, Routes['kiksubmitscore'] +
                         " POST: valid request"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kiksubmitscore'] + " POST: valid request")
        # game = Game.query.get(1)
        # print(game.summary())
        # used to check the runs went through

class testSubmitTransaction(TestSetup):
    def testMain(self):
        self.addPlayersToTeam()
        # player not subscribed
        data = {
                'kik': "frase2560",
                "sponsor": "Domus",
                "amount": 1
                }
        expect = 'frase2560 not subscribed'
        rv = self.app.post(Routes['kiktransaction'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, PNS, Routes['kiktransaction'] +
                         " Post: transaction for player not subscribed"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kiktransaction'] + " Post: transaction for player not subscribed")
        # subscribe the player
        data = {
                'kik': "frase2560",
                "name": "Dallas Fraser",
                "team": 1
                }
        expect = True
        rv = self.app.post(Routes['kiksubscribe'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, 200, Routes['kikcaptain'] +
                         " POST: valid request"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kiksubscribe'] + " Post: subscribe")
        # sponsor does not exist
        data = {
                'kik': "frase2560",
                "sponsor": "FUCKINGDOESNOTEXIST",
                "amount": 1
                }
        expect = 'Sponsor not found'
        rv = self.app.post(Routes['kiktransaction'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, SDNESC, Routes['kiktransaction'] +
                         " Post: sponsor does not exist"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kiktransaction'] + " Post: sponsor does not exist")

class testCaptainGames(TestSetup):
    def testMain(self):
        self.mockScoreSubmission()
        # invalid captian request
        self.show_results = True
        data = {
                'kik': "frase2560",
                "team": 1
                }
        expect = 'Not the right captain for the team'
        rv = self.app.post(Routes['kikcaptaingames'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, 401, Routes['kikcaptaingames'] +
                         " POST: Invalid Captain's games"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kikcaptain'] + " Post: Invalid Captain's games")

        # subscribe the captain to a team
        data = {
                'kik': "frase2560",
                'captain': 'Dallas Fraser',
                "team": 1
                }
        expect = 1
        rv = self.app.post(Routes['kikcaptain'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, 200, Routes['kikcaptain'] +
                         " POST: Authenticate Captain"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kikcaptain'] + " Post: Authenticate Captain")
        # valid request
        data = {
                'kik': "frase2560",
                "team": 1
                }
        expect = [   {  'away_team': 'Chainsaw Black',
                        'away_team_id': 2,
                        'date': '2014-08-23',
                        'field': '',
                        'game_id': 1,
                        'home_team': 'Domus Green',
                        'home_team_id': 1,
                        'league_id': 1,
                        'status': '',
                        'time': '11:37'}]
        rv = self.app.post(Routes['kikcaptaingames'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, 200, Routes['kikcaptaingames'] +
                         " POST: Valid Captain's games"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kikcaptain'] + " Post: Invalid Captain's games")
        # submit score
        data = {
                'kik': "frase2560",
                'game_id': 1,
                'score': 5,
                'hr': [1, 2],
                'ss': []
                }
        expect = True
        rv = self.app.post(Routes['kiksubmitscore'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, 200, Routes['kiksubmitscore'] +
                         " POST: valid request"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kiksubmitscore'] + " POST: valid request")
        # second valid request
        data = {
                'kik': "frase2560",
                "team": 1
                }
        expect = []
        rv = self.app.post(Routes['kikcaptaingames'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, 200, Routes['kikcaptaingames'] +
                         " POST: Invalid Captain's games"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kikcaptain'] + " Post: Invalid Captain's games")

class testUpcomingGames(TestSetup):
    def testMain(self):
        # non-subscribed player
        self.mockUpcomingGames()
        self.show_results = True
        data = {
                'kik': 'frase2560'
                }
        expect = 'frase2560 not registered'
        rv = self.app.post(Routes['kikupcominggames'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, PNS, Routes['kikupcominggames'] +
                         " POST: Unsubscribed player for upcoming games"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kikupcominggames'] + " Post: Unsubscribed player for upcoming games")
        # subscribe the player
        data = {
                'kik': "frase2560",
                "name": "Dallas Fraser",
                "team": 1
                }
        expect = True
        rv = self.app.post(Routes['kiksubscribe'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, 200, Routes['kikcaptain'] +
                         " POST: valid request"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kiksubscribe'] + " Post: subscribe")
        # subscribed player upcoming games
        data = {
                'kik': 'frase2560'
                }
        expect = [   {   'away_team': 'Chainsaw Black',
                        'away_team_id': 2,
                        'date': '2016-04-12',
                        'field': '',
                        'game_id': 1,
                        'home_team': 'Domus Green',
                        'home_team_id': 1,
                        'league_id': 1,
                        'status': '',
                        'time': '11:45'},
                    {   'away_team': 'Domus Green',
                        'away_team_id': 1,
                        'date': '2016-04-13',
                        'field': '',
                        'game_id': 2,
                        'home_team': 'Chainsaw Black',
                        'home_team_id': 2,
                        'league_id': 1,
                        'status': '',
                        'time': '11:45'}]
        rv = self.app.post(Routes['kikupcominggames'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, 200, Routes['kikupcominggames'] +
                         " POST: Subscribed player for upcoming games"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kikupcominggames'] + " Post: Unsubscribed player for upcoming games")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()