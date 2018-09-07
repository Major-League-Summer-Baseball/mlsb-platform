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
from api.BaseTest import ADMIN, PASSWORD, KIK, KIKPW
from base64 import b64encode
from datetime import date, datetime, timedelta
from api.BaseTest import TestSetup
from api.errors import TeamDoesNotExist, NotTeamCaptain, TeamAlreadyHasCaptain,\
                       PlayerNotSubscribed, GameDoesNotExist,\
                       InvalidField, SponsorDoesNotExist, PlayerDoesNotExist
headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' +
                                                  PASSWORD, "utf-8")
                                            ).decode("ascii")
}

kik = {
    'Authorization': 'Basic %s' % b64encode(bytes(KIK + ':' +
                                                  KIKPW, "utf-8")
                                            ).decode("ascii")
}


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
        expect = {'details': -1, 'message': TeamDoesNotExist.message}
        rv = self.app.post(Routes['kikcaptain'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, TeamDoesNotExist.status_code,
                         Routes['kikcaptain'] +
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
        expect = {'details': 'Dallas Fraser',
                  'message': NotTeamCaptain.message}
        rv = self.app.post(Routes['kikcaptain'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, NotTeamCaptain.status_code,
                         Routes['kikcaptain'] +
                         " POST: name of captain does not match"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kikcaptain'] +
                         " Post: name of captain does not match")
        # if someone else tries to say captain with same name but different
        # kik name than one previously stated
        data = {
                'kik': "fucker",
                "captain": "Dallas Fraser",
                "team": 1
                }
        expect = {'details': 'frase2560',
                  'message': TeamAlreadyHasCaptain.message}
        rv = self.app.post(Routes['kikcaptain'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, TeamAlreadyHasCaptain.status_code,
                         Routes['kikcaptain'] +
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
        self.assertEqual(rv.status_code, 200, Routes['kiksubscribe'] +
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
        expect = {'details': -1, 'message': TeamDoesNotExist.message}
        rv = self.app.post(Routes['kiksubscribe'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, TeamDoesNotExist.status_code,
                         Routes['kiksubscribe'] +
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
        expect = True
        rv = self.app.post(Routes['kiksubscribe'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, 200,
                         Routes['kiksubscribe'] +
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
        self.assertEqual(rv.status_code, 200, Routes['kiksubscribe'] +
                         " POST: already subscribed"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kiksubscribe'] + " Post: already subscribed")
        espys = Espys.query.all()
        # check to make sure not additional points were rewarded
        d = datetime.today().strftime("%Y-%m-%d")
        t = datetime.today().strftime("%H:%M")
        ds1 = 'Dallas Fraser email:fras2560@mylaurier.ca awarded espy points for subscribing: 2'
        ds2 = 'Dallas Fraser email:fras2560@mylaurier.ca SUBSCRIBED'
        ds3 = 'fucker email:fucker@guest awarded espy points for subscribing: 2'
        expect = [{
                   'date': d,
                   'description': ds1,
                   'espy_id': 1,
                   'points': 2.0,
                   'receipt': None,
                   'sponsor': None,
                   'team': 'Domus Green',
                   'time': t},
                  {
                   'date': d,
                   'description': ds2,
                   'espy_id': 2,
                   'points': 0.0,
                   'receipt': None,
                   'sponsor': None,
                   'team': 'Domus Green',
                   'time': t},
                  {
                   'date': d,
                   'description': ds3,
                   'espy_id': 3,
                   'points': 2.0,
                   'receipt': None,
                   'sponsor': None,
                   'team': 'Domus Green',
                   'time': t},
                  {'date': d,
                   'description': 'fucker email:fucker@guest SUBSCRIBED',
                   'espy_id': 4,
                   'points': 0.0,
                   'receipt': None,
                   'sponsor': None,
                   'team': 'Domus Green',
                   'time': t}
                  ]
        for index, espy in enumerate(espys):
            self.output(espy.json())
            # self.output(expect[index])
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


class testUnSubscribe(TestSetup):
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
        self.assertEqual(rv.status_code, 200, Routes['kiksubscribe'] +
                         " POST: valid request"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kiksubscribe'] + " Post: subscribe")
        # player does not exist
        data = {
                'kik': "DoesNotExist",
                "team": 1
                }
        expect = {'details': 'Player is not subscribed',
                  'message': 'Player is not subscribed'}

        rv = self.app.post(Routes['kikunsubscribe'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, PlayerNotSubscribed.status_code,
                         Routes['kikunsubscribe'] +
                         " POST: team does not exist"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kikunsubscribe'] +
                         " Post: team does not exist")
        # unsubscribe
        data = {
                'kik': "frase2560",
                "team": 1
                }
        expect = True
        rv = self.app.post(Routes['kikunsubscribe'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, 200,
                         Routes['kikunsubscribe'] +
                         " POST: team does not exist"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kikunsubscribe'] +
                         " Post: team does not exist")


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
        expect = {'details': 'frase2560',
                  'message': PlayerNotSubscribed.message}
        rv = self.app.post(Routes['kiksubmitscore'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, PlayerNotSubscribed.status_code,
                         Routes['kiksubmitscore'] +
                         " POST: invalid kik user name"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kiksubmitscore'] +
                         " POST: invalid kik user name")
        player = Player.query.get(1)
        player.kik = "frase2560"  # add the kik name to the captain
        DB.session.commit()
        # invalid game
        data = {
                'kik': "frase2560",
                'game_id': -1,
                'score': 1,
                'hr': [1, 2],
                'ss': []
                }
        expect = {'details': -1, 'message': GameDoesNotExist.message}
        rv = self.app.post(Routes['kiksubmitscore'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, GameDoesNotExist.status_code,
                         Routes['kiksubmitscore'] +
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
        expect = {'details': 'More hr than score',
                  'message': InvalidField.message}
        rv = self.app.post(Routes['kiksubmitscore'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, InvalidField.status_code,
                         Routes['kiksubmitscore'] +
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
        expect = {'details': 'frase2560',
                  'message': PlayerNotSubscribed.message}
        rv = self.app.post(Routes['kiktransaction'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, PlayerNotSubscribed.status_code,
                         Routes['kiktransaction'] +
                         " Post: transaction for player not subscribed"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kiktransaction'] +
                         " Post: transaction for player not subscribed")
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
        expect = {'details': 'FUCKINGDOESNOTEXIST',
                  'message': SponsorDoesNotExist.message}
        rv = self.app.post(Routes['kiktransaction'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, SponsorDoesNotExist.status_code,
                         Routes['kiktransaction'] +
                         " Post: sponsor does not exist"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kiktransaction'] +
                         " Post: sponsor does not exist")


class testCaptainGames(TestSetup):
    def testMain(self):
        self.mockScoreSubmission()
        # invalid captian request
        data = {
                'kik': "frase2560",
                "team": 1
                }
        expect = {'details': None, 'message': NotTeamCaptain.message}
        rv = self.app.post(Routes['kikcaptaingames'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, NotTeamCaptain.status_code,
                         Routes['kikcaptaingames'] +
                         " POST: Invalid Captain's games"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kikcaptain'] +
                         " Post: Invalid Captain's games")
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
        rv = self.app.post(Routes['kikcaptaingames'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, 200, Routes['kikcaptaingames'] +
                         " POST: Valid Captain's games"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kikcaptain'] +
                         " Post: Invalid Captain's games")
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
                         Routes['kikcaptain'] +
                         " Post: Invalid Captain's games")


class testUpcomingGames(TestSetup):
    def testMain(self):
        # non-subscribed player
        self.mockUpcomingGames()
        data = {
                'name': 'DoesNotExist'
                }
        expect = {'details': 'DoesNotExist',
                  'message': PlayerDoesNotExist.message}
        rv = self.app.post(Routes['kikupcominggames'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, PlayerDoesNotExist.status_code,
                         Routes['kikupcominggames'] +
                         " POST: Player DNE for upcoming games"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kikupcominggames'] +
                         " Post: Unsubscribed player for upcoming games")
        # subscribed player upcoming games
        data = {
                'name': 'Dallas Fraser'
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
        rv = self.app.post(Routes['kikupcominggames'], data=data, headers=kik)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(rv.status_code, 200, Routes['kikupcominggames'] +
                         " POST: Subscribed player for upcoming games"
                         )
        self.assertEqual(expect, loads(rv.data),
                         Routes['kikupcominggames'] +
                         " Post: Unsubscribed player for upcoming games")

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
