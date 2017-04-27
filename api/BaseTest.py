'''
Created on Apr 12, 2016

@author: Dallas
'''
from api import app
import unittest
import tempfile
from api import DB
from pprint import PrettyPrinter
from api.model import Player, Team, Sponsor, League, Game, Bat, Espys, Fun
from datetime import datetime, timedelta
import os
try:
    # running local
    local = True
    from api.credentials import ADMIN, PASSWORD, KIK, KIKPW
except:
    ADMIN = os.environ['ADMIN']
    PASSWORD = os.environ['PASSWORD']
    KIK = os.environ['KIK']
    KIKPW = os.environ['KIKPW']
from base64 import b64encode
headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' + PASSWORD, "utf-8")).decode("ascii")
}

kik = {
    'Authorization': 'Basic %s' % b64encode(bytes(KIK + ':' + KIKPW, "utf-8")).decode("ascii")
}


class TestSetup(unittest.TestCase):
    def setUp(self):
        self.show_results = False
        self.pp = PrettyPrinter(indent=4)
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        self.d = "2014-8-23"
        self.t = "11:37"
        app.config['TESTING'] = True
        self.app = app.test_client()
        DB.engine.execute('''   
                                DROP TABLE IF EXISTS fun;
                                DROP TABLE IF EXISTS roster;
                                DROP TABLE IF EXISTS bat;
                                DROP TABLE IF EXISTS espys;
                                DROP TABLE IF EXISTS game;
                                DROP TABLE IF EXISTS team;
                                DROP TABLE IF EXISTS player;
                                DROP TABLE IF EXISTS sponsor;
                                DROP TABLE IF EXISTS league;
                        ''')
        DB.create_all()

    def tearDown(self):
        DB.session.commit()
        DB.engine.execute('''   
                                DROP TABLE IF EXISTS fun;
                                DROP TABLE IF EXISTS roster;
                                DROP TABLE IF EXISTS bat;
                                DROP TABLE IF EXISTS espys;
                                DROP TABLE IF EXISTS game;
                                DROP TABLE IF EXISTS team;
                                DROP TABLE IF EXISTS player;
                                DROP TABLE IF EXISTS sponsor;
                                DROP TABLE IF EXISTS league;
                        ''')

    def output(self, data):
        if self.show_results:
            self.pp.pprint(data)

    def addFun(self):
        FUNS = {
               2002:89,
               2003: 100,
               2004: 177,
               2005:186,
               2006:176,
               2007: 254,
               2008: 290,
               2009: 342,
               2010: 304,
               2011: 377,
               2012: 377,
               2013: 461,
               2014: 349,
               2015: 501
               }
        for year, count in FUNS.items():
            DB.session.add(Fun(year=year, count=count))
        DB.session.commit()

    def addSponsors(self):
        self.sponsors = [Sponsor("Domus"),
                         Sponsor("Chainsaw")
                         ]
        for s in range(0,len(self.sponsors)):
            DB.session.add(self.sponsors[s])
        DB.session.commit()

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

    def addTeamWithLegaue(self):
        self.addLeagues()
        self.addPlayers()
        self.addSponsors()
        # team one
        self.teams = [Team(
                           color="Green",
                           sponsor_id=self.sponsors[0].id,
                           league_id=1
                           
                           ),
                      Team(
                           color="Black",
                           sponsor_id=self.sponsors[1].id,
                           league_id=1
                           ),
                      Team(
                           color="Diamon",
                           sponsor_id=self.sponsors[0].id,
                           league_id=1
                           )
                      ]
        for t in range(0, len(self.teams)):
            DB.session.add(self.teams[t])
        DB.session.commit()

    def addTeams(self):
        self.addPlayers()
        self.addSponsors()
        # team one
        self.teams = [Team(
                           color="Green",
                           sponsor_id=self.sponsors[0].id
                           ),
                      Team(
                           color="Black",
                           sponsor_id=self.sponsors[1].id
                           ),
                      Team(
                           color="Diamon",
                           sponsor_id=self.sponsors[0].id
                           )
                      ]
        for t in range(0, len(self.teams)):
            DB.session.add(self.teams[t])
        DB.session.commit()

    def addLeagues(self):
        self.leagues = [League("Monday & Wedneday"), League("Tuesday & Thursday")]
        for t in range(0, len(self.leagues)):
            DB.session.add(self.leagues[t])
        DB.session.commit()

    def addGames(self):
        self.addTeams()
        self.addLeagues()
        self.games = [Game(
                           self.d,
                           self.t,
                           self.teams[0].id,
                           self.teams[1].id,
                           self.leagues[0].id
                           ),
                      Game(
                           self.d,
                           self.t,
                           self.teams[0].id,
                           self.teams[1].id,
                           self.leagues[1].id
                           )
                      ]
        DB.session.add(self.games[0])
        DB.session.add(self.games[1])
        DB.session.commit()

    def addBunchGames(self):
        self.addTeams()
        self.addLeagues()
        self.teams.append(Team("Blue"))
        DB.session.add(self.teams[-1])
        self.games = [Game(
                           self.d,
                           self.t,
                           self.teams[0].id,
                           self.teams[1].id,
                           self.leagues[0].id),
                      Game(
                           self.d,
                           self.t,
                           self.teams[0].id,
                           self.teams[1].id,
                           self.leagues[1].id),
                      Game(
                           self.d,
                           self.t,
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
        self.addTeams()
        team = Team.query.get(1)
        team.insert_player(1, captain=True)
        DB.session.commit()

    def addPlayersToTeam(self):
        self.addTeams()
        team = Team.query.get(1)
        team.insert_player(1, captain=True)
        team.insert_player(1, captain=False)
        DB.session.commit()

    def mockScoreSubmission(self):
        self.addLeagues()
        self.addPlayersToTeam()
        team = Team.query.get(1)
        team.insert_player(2)
        self.game = Game(self.d,
                         self.t,
                         self.teams[0].id,
                         self.teams[1].id,
                         self.leagues[0].id)
        DB.session.add(self.game)
        DB.session.commit()

    def mockUpcomingGames(self):
        self.addLeagues()
        self.addPlayersToTeam()
        t = "11:45"
        today = datetime.today()
        previous_game = (today+timedelta(-1)).strftime("%Y-%m-%d")
        game_one_day = today.strftime("%Y-%m-%d")
        game_two_day = (today+timedelta(1)).strftime("%Y-%m-%d")
        game_five_day = (today+timedelta(5)).strftime("%Y-%m-%d")
        # few upcoming games, one in the past, and one the player is not on
        games = [
                 Game(game_one_day, t, self.teams[0].id, self.teams[1].id, self.leagues[0].id),
                 Game(game_two_day, t, self.teams[1].id, self.teams[0].id, self.leagues[0].id),
                 Game(game_five_day, t, self.teams[0].id, self.teams[1].id, self.leagues[0].id),
                 Game(previous_game, t, self.teams[0].id, self.teams[1].id, self.leagues[0].id),
                 Game(game_one_day, t, self.teams[1].id, self.teams[2].id, self.leagues[0].id),
                 ]
        for game in games:
            DB.session.add(game)
        DB.session.commit()

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
        self.games = [Game(
                           self.d,
                           self.t,
                           1,
                           2,
                           1),
                     Game(
                          self.d,
                          self.t,
                          2,
                          1,
                          1),
                     Game(
                          self.d,
                          self.t,
                          2,
                          1,
                          1),
                    Game(
                         self.d,
                         self.t,
                         3,
                         4,
                         2),
                     Game(
                          self.d,
                          self.t,
                          4,
                          3,
                          2),
                     Game(
                          self.d,
                          self.t,
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

    def mockLeaders(self):
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
        self.games = [Game(
                           "2014-8-23",
                           self.t,
                           1,
                           2,
                           1),
                     Game(
                          "2015-8-23",
                          self.t,
                          2,
                          1,
                          1),
                     Game(
                          "2016-8-23",
                          self.t,
                          2,
                          1,
                          1),
                    Game(
                         self.d,
                         self.t,
                         3,
                         4,
                         2),
                     Game(
                          self.d,
                          self.t,
                          4,
                          3,
                          2),
                     Game(
                          self.d,
                          self.t,
                          4,
                          3,
                          2),
                      ]
        for g in self.games:
            DB.session.add(g)
        self.players = [Player("UNASSIGNED",
                               "doNotUse",
                               gender="f"),
                        Player("Dallas Fraser", 
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
        self.bats = [Bat(   2, 
                            1, 
                            1, 
                            "HR", 
                            1, 
                            rbi=2),
                     Bat(   3, 
                            2, 
                            1, 
                            "HR", 
                            1, 
                            rbi=1),
                     Bat(   2, 
                            1, 
                            2, 
                            "HR", 
                            1, 
                            rbi=1),
                     Bat(   3, 
                            2, 
                            2, 
                            "HR", 
                            1, 
                            rbi=2),
                     Bat(   2, 
                            1, 
                            3, 
                            "HR", 
                            1, 
                            rbi=1),
                     Bat(   3, 
                            2, 
                            3, 
                            "HR", 
                            1, 
                            rbi=1),
                     Bat(   2, 
                            3, 
                            4, 
                            "HR", 
                            1, 
                            rbi=2),
                     Bat(   3, 
                            4, 
                            4, 
                            "HR", 
                            1, 
                            rbi=1),
                     Bat(   2, 
                            3, 
                            5, 
                            "HR", 
                            1, 
                            rbi=1),
                     Bat(   3, 
                            4, 
                            5, 
                            "HR", 
                            1, 
                            rbi=2),
                     Bat(   2, 
                            3, 
                            6, 
                            "HR", 
                            1, 
                            rbi=1),
                     Bat(   3, 
                            4, 
                            6, 
                            "HR", 
                            1, 
                            rbi=1),
                     ]
        for b in self.bats:
            DB.session.add(b)
        DB.session.commit()

    def addEspys(self):
        self.addTeams()
        espys = [Espys( 1, 
                        sponsor_id=None, 
                        description="Kik transaction", 
                        points=1, 
                        receipt=None),
                 Espys( 2, 
                        sponsor_id=1, 
                        description="Purchase", 
                        points=2, 
                        receipt="12019209129"),
                 ]
        for espy in espys:
            DB.session.add(espy)
        DB.session.commit()