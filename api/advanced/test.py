'''
@author: Dallas Fraser
@author: 2015-08-25
@organization: MLSB API
@summary: Tests all the basic APIs
'''
from api import app
import unittest
import os
import tempfile
from api.helper import loads
from api import DB
from pprint import PrettyPrinter
from api.routes import Routes
from api.model import Player, Team, Sponsor, League, Game, Bat, roster
from api.model import insertPlayer
from datetime import datetime, date, time
from api.credentials import ADMIN, PASSWORD
from base64 import b64encode
headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' + PASSWORD, "utf-8")).decode("ascii")
}


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.show_results = False
        self.pp = PrettyPrinter(indent=4)
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        self.d = date(2014, 8, 23)
        self.t = time(11, 37)
        app.config['TESTING'] = True
        self.app = app.test_client()
        DB.engine.execute('''   
                                DROP TABLE IF EXISTS roster;
                                DROP TABLE IF EXISTS bat;
                                DROP TABLE IF EXISTS game;
                                DROP TABLE IF EXISTS team;
                                DROP TABLE IF EXISTS player;
                                DROP TABLE IF EXISTS sponsor;
                                DROP TABLE IF EXISTS league;
                        ''')
        DB.create_all()

    def tearDown(self):
        DB.engine.execute('''   
                                DROP TABLE IF EXISTS roster;
                                DROP TABLE IF EXISTS bat;
                                DROP TABLE IF EXISTS game;
                                DROP TABLE IF EXISTS team;
                                DROP TABLE IF EXISTS player;
                                DROP TABLE IF EXISTS sponsor;
                                DROP TABLE IF EXISTS league;
                        ''')

    def output(self, data):
        if self.show_results:
            self.pp.pprint(data)

    def addSponsor(self):
        self.sponsor = Sponsor("Domus")
        DB.session.add(self.sponsor)
        DB.session.commit()
        self.assertEqual(self.sponsor.id, 1, "Could not add sponsor")

    def addSponsors(self):
        self.sponsors = [Sponsor("Domus"),
                         Sponsor("Chainsaw")
                         ]
        for s in range(0,len(self.sponsors)):
            DB.session.add(self.sponsors[s])
        DB.session.commit()

    def addPlayer(self):
        p = Player("Dallas Fraser",
                   "fras2560@mylaurier.ca",
                   gender="m")
        DB.session.add(p)
        DB.session.commit()
        self.assertEqual(p.id, 1, "Could not add player")

    def addPlayers(self):
        self.players = [Player("Dallas Fraser",
                   "fras2560@mylaurier.ca",
                   gender="m"),
                   Player("My Dream Girl",
                   "dream@mylaurier.ca",
                   gender="f"),
                   Player("Barry Bonds",
                          "bonds@hallOfFame.ca",
                          gender="M")]
        for player in range(0, len(self.players)):
            DB.session.add(self.players[player])
        DB.session.commit()

    def addTeam(self):
        self.addPlayer()
        self.addSponsor()
        self.team = Team(color="Green")
        self.team.sponsor_id = self.sponsor.id
        DB.session.add(self.team)
        DB.session.commit()
        self.assertEqual(self.team.id, 1)

    def addTeams(self):
        self.addPlayers()
        self.addSponsors()
        # team one
        self.teams = [Team(color="Green"),
                      Team(color="Black")
                      ]
        self.teams[0].sponsor_id = self.sponsors[0].id
        self.teams[1].sponsor_id = self.sponsors[1].id
        for t in range(0, len(self.teams)):
            DB.session.add(self.teams[t])
        DB.session.commit()

    def addLeague(self):
        self.league = League("Monday & Wedneday")
        DB.session.add(self.league)
        DB.session.commit()
        self.assertEqual(1, self.league.id)

    def addLeagues(self):
        self.leagues = [League("Monday & Wedneday"), League("Tuesday & Thursday")]
        for t in range(0, len(self.leagues)):
            DB.session.add(self.leagues[t])
        DB.session.commit()

    def addGame(self):
        self.addTeams()
        self.addLeague()
        self.game = Game(datetime.combine(self.d, self.t),
                         self.teams[0].id,
                         self.teams[1].id,
                         self.league.id)
        DB.session.add(self.game)
        DB.session.commit()
        self.assertEqual(1, self.game.id)

    def addGames(self):
        self.addTeams()
        self.addLeagues()
        self.games = [Game(datetime.combine(self.d, self.t),
                         self.teams[0].id,
                         self.teams[1].id,
                         self.leagues[0].id),
                      Game(datetime.combine(self.d, self.t),
                         self.teams[0].id,
                         self.teams[1].id,
                         self.leagues[1].id)
                      ]
        DB.session.add(self.games[0])
        DB.session.add(self.games[1])
        DB.session.commit()

    def addBunchGames(self):
        self.addTeams()
        self.addLeagues()
        self.teams.append(Team("Blue"))
        DB.session.add(self.teams[-1])
        self.games = [Game(datetime.combine(self.d, self.t),
                         self.teams[0].id,
                         self.teams[1].id,
                         self.leagues[0].id),
                      Game(datetime.combine(self.d, self.t),
                         self.teams[0].id,
                         self.teams[1].id,
                         self.leagues[1].id),
                      Game(datetime.combine(self.d, self.t),
                         self.teams[1].id,
                         self.teams[2].id,
                         self.leagues[1].id)
                      ]
        DB.session.add(self.games[0])
        DB.session.add(self.games[1])
        DB.session.add(self.games[2])
        DB.session.commit()

    def addBunchBats(self):
        self.addBunchGames()
        self.bats = [Bat(self.players[0].id,
                       self.teams[0].id,
                       self.games[0].id,
                       "S",
                       5,
                       
                       rbi=1),
                     Bat(self.players[1].id,
                         self.teams[0].id,
                         self.games[1].id,
                         "K",
                         5),
                    Bat(self.players[1].id,
                         self.teams[1].id,
                         self.games[2].id,
                         "K",
                         5),
                     ]
        for i in range(0, len(self.bats)):
            DB.session.add(self.bats[i])
        DB.session.commit()

    def addBat(self):
        self.addGame()
        self.bat = Bat(self.players[0].id,
                       self.teams[0].id,
                       self.game.id,
                       "S",
                       5,
                       rbi=1)
        DB.session.add(self.bat)
        DB.session.commit()
        self.assertEqual(self.bat.id, 1)
    
    def addBats(self):
        self.addGames()
        self.bats = [Bat(self.players[0].id,
                       self.teams[0].id,
                       self.games[0].id,
                       "S",
                       5,
                       
                       rbi=1),
                     Bat(self.players[1].id,
                         self.teams[0].id,
                         self.games[1].id,
                         "K",
                         5)
                     ]
        for i in range(0, len(self.bats)):
            DB.session.add(self.bats[i])
        DB.session.commit()

    def addCaptainToTeam(self):
        self.addTeam()
        insertPlayer(1, 1, captain=True)
    
    def addPlayersToTeam(self):
        self.addTeams()
        insertPlayer(1, 1, captain=True)
        insertPlayer(1, 2, captain=False)

    def addSeason(self):
        self.sponsors = [Sponsor("Domus"),
                         Sponsor("Sentry"),
                         Sponsor("Nightschool"),
                         Sponsor("Brick")]
        for s in self.sponsors:
            DB.session.add(s)
        DB.session.add(League("Monday & Wednesday"))
        DB.session.add(League("Tuesday & Thursday"))
        self.teams = [Team("Green",
                           sponsor_id=1, 
                           league_id=1),
                      Team("Sky Blue",
                           sponsor_id=2, 
                           league_id=1),
                      Team("Navy",
                           sponsor_id=3, 
                           league_id=2),
                      Team('Blue',
                           sponsor_id=4,
                           league_id=2)]
        for t in self.teams:
            DB.session.add(t)
        self.games = [Game(datetime.combine(self.d, self.t),
                             1,
                             2,
                             1),
                     Game(datetime.combine(self.d, self.t),
                             2,
                             1,
                             1),
                     Game(datetime.combine(self.d, self.t),
                             2,
                             1,
                             1),
                    Game(datetime.combine(self.d, self.t),
                             3,
                             4,
                             2),
                     Game(datetime.combine(self.d, self.t),
                             4,
                             3,
                             2),
                     Game(datetime.combine(self.d, self.t),
                             4,
                             3,
                             2),
                      ]
        for g in self.games:
            DB.session.add(g)
        self.addPlayers()
        self.bats = [Bat(   1, 
                            1, 
                            1, 
                            "HR", 
                            1, 
                            rbi=2),
                     Bat(   2, 
                            2, 
                            1, 
                            "HR", 
                            1, 
                            rbi=1),
                     Bat(   1, 
                            1, 
                            2, 
                            "HR", 
                            1, 
                            rbi=1),
                     Bat(   2, 
                            2, 
                            2, 
                            "HR", 
                            1, 
                            rbi=2),
                     Bat(   1, 
                            1, 
                            3, 
                            "HR", 
                            1, 
                            rbi=1),
                     Bat(   2, 
                            2, 
                            3, 
                            "HR", 
                            1, 
                            rbi=1),
                     Bat(   1, 
                            3, 
                            4, 
                            "HR", 
                            1, 
                            rbi=2),
                     Bat(   2, 
                            4, 
                            4, 
                            "HR", 
                            1, 
                            rbi=1),
                     Bat(   1, 
                            3, 
                            5, 
                            "HR", 
                            1, 
                            rbi=1),
                     Bat(   2, 
                            4, 
                            5, 
                            "HR", 
                            1, 
                            rbi=2),
                     Bat(   1, 
                            3, 
                            6, 
                            "HR", 
                            1, 
                            rbi=1),
                     Bat(   2, 
                            4, 
                            6, 
                            "HR", 
                            1, 
                            rbi=1),
                     ]
        for b in self.bats:
            DB.session.add(b)
        DB.session.commit()

class GameTest(BaseTest):
    def testPost(self):
        self.show_results = True
        rv = self.app.post(Routes['vgame'])
        expect = {'data': [],
                  'failures': [],
                  'message': '',
                  'success': True}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['vgame'] + " Post: View of Game")
        self.addBats()
        rv = self.app.post(Routes['vgame'], data={"league_id": 1})
        expect = {   'data': [   {  'away_bats': [],
                                    'away_score': 0,
                                    'away_team': {'color': 'Black',
                                                  'league_id': None,
                                                  'sponsor_id': 2,
                                                  'team_id': 2,
                                                  'year': 2015},
                                    'date': '2014-08-23 11:37',
                                    'home_bats': [   {'hit': 's',
                                                      'inning': 5,
                                                      'name': 'Dallas Fraser',
                                                      'rbi': 1},
                                                     {'hit': 'k',
                                                      'inning': 5,
                                                      'name': 'My Dream Girl',
                                                      'rbi': 0}],
                                    'home_score': 1,
                                    'home_team': {'color': 'Green',
                                                  'league_id': None,
                                                  'sponsor_id': 1,
                                                  'team_id': 1,
                                                  'year': 2015},
                                    'league': {'league_id': 1,
                                               'league_name': 'Monday & Wedneday'}
                                  }
                              ],
                    'failures': [],
                    'message': '',
                    'success': True}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['vgame'] + " Post: View of Game")

        rv = self.app.post(Routes['vgame'], data={})
        expect = {   'data': [   {  'away_bats': [],
                                    'away_score': 0,
                                    'away_team': {   'color': 'Black',
                                                     'league_id': None,
                                                     'sponsor_id': 2,
                                                     'team_id': 2,
                                                     'year': 2015},
                                    'date': '2014-08-23 11:37',
                                    'home_bats': [   {   'hit': 's',
                                                         'inning': 5,
                                                         'name': 'Dallas Fraser',
                                                         'rbi': 1},
                                                     {   'hit': 'k',
                                                         'inning': 5,
                                                         'name': 'My Dream Girl',
                                                         'rbi': 0}],
                                    'home_score': 1,
                                    'home_team': {   'color': 'Green',
                                                     'league_id': None,
                                                     'sponsor_id': 1,
                                                     'team_id': 1,
                                                     'year': 2015},
                                    'league': {   'league_id': 1,
                                                  'league_name': 'Monday & Wedneday'}},
                                {   'away_bats': [],
                                    'away_score': 0,
                                    'away_team': {   'color': 'Black',
                                                     'league_id': None,
                                                     'sponsor_id': 2,
                                                     'team_id': 2,
                                                     'year': 2015},
                                    'date': '2014-08-23 11:37',
                                    'home_bats': [   {   'hit': 's',
                                                         'inning': 5,
                                                         'name': 'Dallas Fraser',
                                                         'rbi': 1},
                                                     {   'hit': 'k',
                                                         'inning': 5,
                                                         'name': 'My Dream Girl',
                                                         'rbi': 0}],
                                    'home_score': 1,
                                    'home_team': {   'color': 'Green',
                                                     'league_id': None,
                                                     'sponsor_id': 1,
                                                     'team_id': 1,
                                                     'year': 2015},
                                    'league': {   'league_id': 2,
                                                  'league_name': 'Tuesday & Thursday'}}],
                'failures': [],
                'message': '',
                'success': True}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['vgame'] + " Post: View of Game")

class PlayerTest(BaseTest):
    def testPost(self):
        self.show_results = True
        rv = self.app.post(Routes['vplayer'])
        expect = {'data': {},
                  'failures': [],
                  'message': '',
                  'success': True}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['vplayer'] + " Post: View of Game")
        self.addBats()
        rv = self.app.post(Routes['vplayer'])
        expect = {   'data': {   'Dallas Fraser': {   'avg': 1.0,
                                                     'bats': 1,
                                                     'd': 0,
                                                     'go': 0,
                                                     'hr': 0,
                                                     'k': 0,
                                                     'pf': 0,
                                                     's': 1},
                                'My Dream Girl': {   'avg': 0.0,
                                                     'bats': 1,
                                                     'd': 0,
                                                     'go': 0,
                                                     'hr': 0,
                                                     'k': 1,
                                                     'pf': 0,
                                                     's': 0}},
                'failures': [],
                'message': '',
                'success': True}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['vplayer'] + " Post: View of Game")

    def testPost2(self):
        self.show_results = True
        self.addBunchBats()
        rv = self.app.post(Routes['vplayer'])
        expect = {   'data': {   'Dallas Fraser': {   'avg': 1.0,
                                                     'bats': 1,
                                                     'd': 0,
                                                     'go': 0,
                                                     'hr': 0,
                                                     'k': 0,
                                                     'pf': 0,
                                                     's': 1},
                                'My Dream Girl': {   'avg': 0.0,
                                                     'bats': 2,
                                                     'd': 0,
                                                     'go': 0,
                                                     'hr': 0,
                                                     'k': 2,
                                                     'pf': 0,
                                                     's': 0}},
                    'failures': [],
                    'message': '',
                    'success': True}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['vplayer'] + " Post: View of Game")
        rv = self.app.post(Routes['vplayer'], data={'league_id': 1})
        expect = {   'data': {   'Dallas Fraser': {   'avg': 1.0,
                                                     'bats': 1,
                                                     'd': 0,
                                                     'go': 0,
                                                     'hr': 0,
                                                     'k': 0,
                                                     'pf': 0,
                                                     's': 1}},
                    'failures': [],
                    'message': '',
                    'success': True}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['vplayer'] + " Post: View of Game")
        rv = self.app.post(Routes['vplayer'], data={'team_id': 1})
        expect = {   'data': {   'Dallas Fraser': {   'avg': 1.0,
                                                     'bats': 1,
                                                     'd': 0,
                                                     'go': 0,
                                                     'hr': 0,
                                                     'k': 0,
                                                     'pf': 0,
                                                     's': 1},
                                'My Dream Girl': {   'avg': 0.0,
                                                     'bats': 1,
                                                     'd': 0,
                                                     'go': 0,
                                                     'hr': 0,
                                                     'k': 1,
                                                     'pf': 0,
                                                     's': 0}},
                    'failures': [],
                    'message': '',
                    'success': True}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['vplayer'] + " Post: View of Game")

class TeamTest(BaseTest):
    def TestPostNoParameters(self):
        self.show_results = True
        rv = self.app.post(Routes['vteam'])
        expect = {'data': {},
                  'failures': [],
                  'message': '',
                  'success': True}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                 Routes['vteam'] + " Post: View of Team")
        self.addSeason()
        rv = self.app.post(Routes['vteam'])
        expect = {'data': {     '1': {   'away_losses': 1,
                                         'away_wins': 0,
                                         'games': 0,
                                         'hits_allowed': 3,
                                         'hits_for': 3,
                                         'home_losses': 0,
                                         'home_wins': 1,
                                         'losses': 1,
                                         'runs_against': 4,
                                         'runs_for': 4,
                                         'ties': 1,
                                         'wins': 1},
                                '2': {   'away_losses': 1,
                                         'away_wins': 0,
                                         'games': 0,
                                         'hits_allowed': 3,
                                         'hits_for': 3,
                                         'home_losses': 0,
                                         'home_wins': 1,
                                         'losses': 1,
                                         'runs_against': 4,
                                         'runs_for': 4,
                                         'ties': 1,
                                         'wins': 1},
                                '3': {   'away_losses': 1,
                                         'away_wins': 0,
                                         'games': 0,
                                         'hits_allowed': 3,
                                         'hits_for': 3,
                                         'home_losses': 0,
                                         'home_wins': 1,
                                         'losses': 1,
                                         'runs_against': 4,
                                         'runs_for': 4,
                                         'ties': 1,
                                         'wins': 1},
                                '4': {   'away_losses': 1,
                                         'away_wins': 0,
                                         'games': 0,
                                         'hits_allowed': 3,
                                         'hits_for': 3,
                                         'home_losses': 0,
                                         'home_wins': 1,
                                         'losses': 1,
                                         'runs_against': 4,
                                         'runs_for': 4,
                                         'ties': 1,
                                         'wins': 1},
                           },
                  'failures': [],
                  'message': '',
                  'success': True}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                 Routes['vteam'] + " Post: View of Team")
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()