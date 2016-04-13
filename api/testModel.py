'''
@author: Dallas Fraser
@author: 2016-04-12
@organization: MLSB API
@summary: Holds the tests for the model
'''
import unittest
from api.model import Player, Team, Bat, Sponsor, League, Game
from api.errors import InvalidField,PlayerDoesNotExist,TeamDoesNotExist,\
                        LeagueDoesNotExist, SponsorDoesNotExist, NonUniqueEmail,\
                        GameDoesNotExist
from pprint import PrettyPrinter
from api import app, DB
import tempfile

class BaseModel(unittest.TestCase):
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

    def insertLeague(self):
        DB.session.add(League("Monday & Wedneday"))
        DB.session.commit()

    def insertSponsor(self):
        DB.session.add(Sponsor("Domus"))
        DB.session.commit()

    def insertSponsors(self):
        DB.session.add(Sponsor("Domus"))
        DB.session.add(Sponsor("Sentry"))
        DB.session.commit()

    def insertTeams(self):
        self.insertLeague()
        self.insertSponsors()
        DB.session.add(Team("green",
                            sponsor_id=1,
                            league_id=1))
        DB.session.add(Team("sky",
                            sponsor_id=2,
                            league_id=1))
        DB.session.commit()

    def insertPlayer(self):
        DB.session.add(Player("Dallas Fraser", "fras2560@mylaurier.ca"))
        DB.session.commit()

    def insertGame(self):
        self.insertTeams()
        self.insertPlayer()
        DB.session.add(Game(self.d, 
                            self.t, 
                            1, 
                            2, 
                            1, 
                            status="Championships", 
                            field="WP1"))

class testSponsor(BaseModel):
    def testSponsorInit(self):
        # valid data
        __ =  Sponsor("Good Sponsor")
        __ = Sponsor("Good Sponsor",
                     link="http://good-sponsor.ca",
                     description="Good Descript")
        # now bad stuff
        try:
            __ = Sponsor(1)
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass
        try:
            __ = Sponsor("Good Sponsor",
                           link=1)
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass
        try:
            __ = Sponsor("Good Sponsor",
                           link="http://good-sponsor.ca",
                           description=1)
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass

    def testSponsorUpdate(self):
        # valid sponsor
        s =  Sponsor("Good Sponsor")
        # valid update
        s.update(name="New Sponsor", link="New Link", description="new")
        
        # now bad stuff
        try:
            s.update(name=1)
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass
        try:
            s.update("Good Sponsor",
                     link=1)
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass
        try:
            s.update("Good Sponsor",
                     link="http://good-sponsor.ca",
                     description=1)
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass

class testPlayer(BaseModel):
    def testPlayerInit(self):
        __ =  Player("Good Player", "good@mlsb.ca")
        __ = Player("Good Player", "good@mlsb.ca",
                     gender="m",
                     password="Good password")
        # now bad stuff
        try:
            __ = Player(1, "good@mlsb.ca")
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass
        try:
            __ = Player("Good Player", 1)
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass
        try:
            p1 = Player("first player", "fras2560@mylaurier.ca")
            DB.session.add(p1)
            DB.session.commit()
            __ = Player("second player", "fras2560@mylaurier.ca")
            self.assertEqual(False, True, "Should raise email exception")
        except NonUniqueEmail:
            pass
        try:
            __ = Player("Good Player", "good@mlsb.ca", gender="XX")
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass

    def testPlayerUpdate(self):
        p1 =  Player("Good Player", "good@mlsb.ca")
        p1.update(name="new name",
                  email="new@mlsb.ca",
                  gender="f",
                  password="n")
        # now bad stuff
        try:
            p1.update(name=1, email="good@mlsb.ca")
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass
        try:
            p1.update(name="Good Player", email=1)
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass
        try:
            p2 = Player("first player", "fras2560@mylaurier.ca")
            DB.session.add(p2)
            DB.session.commit()
            p1.update(name="second player", email="fras2560@mylaurier.ca")
            self.assertEqual(False, True, "Should raise email exception")
        except NonUniqueEmail:
            pass
        try:
            p1.update(name="Good Player", email="good@mlsb.ca", gender="XX")
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass

class testLeague(BaseModel):
    def testLeagueInit(self):
        __ = League("Monday & Wednesday")
        # now bad stuff
        try:
            __ = League(1)
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass

    def testLeagueUpdate(self):
        l = League("Monday & Wednesday")
        l.update("Tuesday & Thursday")
        try:
            l.update(1)
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass

class testTeam(BaseModel):
    def testTeamInit(self):
        self.insertLeague()
        self.insertSponsor()
        # good Teams
        __ = Team(color="Black", 
                  sponsor_id=1, 
                  league_id=1)
        __ = Team(color="Green", 
                  sponsor_id=1, 
                  league_id=1,
                  year = 2014,
                  )
        # now for bad teams
        try:
            __ = Team(color="Black", 
                      sponsor_id=99999, 
                      league_id=1)
            self.assertEqual(False, True, "Should raise no sponsor")
        except SponsorDoesNotExist:
            pass
        try:
            __ = Team(color="Black", 
                      sponsor_id=1, 
                      league_id=99999)
            self.assertEqual(False, True, "Should raise no league")
        except LeagueDoesNotExist:
            pass
        try:
            __ = Team(color=1, 
                      sponsor_id=1, 
                      league_id=1)
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass
        try:
            __ = Team(color="Black", 
                      sponsor_id=1, 
                      league_id=1,
                      year=1)
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass

    def testTeamUpdate(self):
        self.insertLeague()
        self.insertSponsor()
        # good Teams
        l = Team(color="Black", 
                 sponsor_id=1, 
                 league_id=1)
        l.update(color="Green", 
                 sponsor_id=1, 
                 league_id=1,
                 year = 2014,
                  )
        # now for bad teams
        try:
            l.update(color="Black", 
                     sponsor_id=99999, 
                     league_id=1)
            self.assertEqual(False, True, "Should raise no sponsor")
        except SponsorDoesNotExist:
            pass
        try:
            l.update(color="Black", 
                     sponsor_id=1, 
                     league_id=99999)
            self.assertEqual(False, True, "Should raise no league")
        except LeagueDoesNotExist:
            pass
        try:
            l.update(color=1, 
                     sponsor_id=1, 
                     league_id=1)
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass
        try:
            l.update(color="Black", 
                     sponsor_id=1, 
                     league_id=1,
                     year=1)
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass

class testGame(BaseModel):
    def testGameInit(self):
        self.insertTeams()
        # good game
        __ = Game(self.d, 
                 self.t, 
                 1, 
                 2, 
                 1)
        try:
            __= Game("x", 
                     self.t, 
                     1, 
                     2, 
                     1)
            self.assertEqual(True, False, "should raise invalid field")
        except InvalidField:
            pass
        try:
            __ = Game(self.d, 
                      self.t, 
                      1, 
                      2, 
                      1,
                      status=1)
            self.assertEqual(True, False, "should raise invalid field")
        except InvalidField:
            pass
        try:
            __ = Game(self.d, 
                      self.t, 
                      1, 
                      2, 
                      1,
                      field=1)
            self.assertEqual(True, False, "should raise invalid field")
        except InvalidField:
            pass
        try:
            __ = Game(self.d, 
                      self.t, 
                      999, 
                      2, 
                      1)
            self.assertEqual(True, False, "should raise no team")
        except TeamDoesNotExist:
            pass
        try:
            __ = Game(self.d, 
                      self.t, 
                      1, 
                      999, 
                      1)
            self.assertEqual(True, False, "should raise no team")
        except TeamDoesNotExist:
            pass
        try:
            __ = Game(self.d, 
                      self.t, 
                      1, 
                      2, 
                      999)
            self.assertEqual(True, False, "should raise no league")
        except LeagueDoesNotExist:
            pass

    def testGameUpdate(self):
        self.insertTeams()
        # good game
        g = Game(self.d, 
                 self.t, 
                 1, 
                 2, 
                 1)
        try:
            __= Game("x", 
                     self.t, 
                     1, 
                     2, 
                     1)
            self.assertEqual(True, False, "should raise invalid field")
        except InvalidField:
            pass
        try:
            g.update(self.d, 
                      self.t, 
                      1, 
                      2, 
                      1,
                      status=1)
            self.assertEqual(True, False, "should raise invalid field")
        except InvalidField:
            pass
        try:
            g.update(self.d, 
                      self.t, 
                      1, 
                      2, 
                      1,
                      field=1)
            self.assertEqual(True, False, "should raise invalid field")
        except InvalidField:
            pass
        try:
            g.update(self.d, 
                      self.t, 
                      999, 
                      2, 
                      1)
            self.assertEqual(True, False, "should raise no team")
        except TeamDoesNotExist:
            pass
        try:
            g.update(self.d, 
                      self.t, 
                      1, 
                      999, 
                      1)
            self.assertEqual(True, False, "should raise no team")
        except TeamDoesNotExist:
            pass
        try:
            g.update(self.d, 
                     self.t, 
                     1, 
                     2, 
                     999)
            self.assertEqual(True, False, "should raise no league")
        except LeagueDoesNotExist:
            pass

class testBat(BaseModel):
    def testBatInit(self):
        self.insertGame()
        # good bat
        __ = Bat(1, 
                1, 
                1, 
                "s", 
                inning=1, 
                rbi=1)
        # now for the bad stuff
        try:
            __ = Bat(1, 
                     1, 
                     1, 
                     "XX", 
                     inning=1, 
                     rbi=1)
            self.assertEqual(True, False, "should raise invalid field")
        except InvalidField:
            pass
        try:
            __ = Bat(1, 
                     1, 
                     1, 
                     "s", 
                     inning=-1, 
                     rbi=1)
            self.assertEqual(True, False, "should raise invalid field")
        except InvalidField:
            pass
        try:
            __ = Bat(1, 
                     1, 
                     1, 
                     "s", 
                     inning=1, 
                     rbi=1000)
            self.assertEqual(True, False, "should raise invalid field")
        except InvalidField:
            pass
        try:
            __ = Bat(999, 
                     1, 
                     1, 
                     "s", 
                     inning=1, 
                     rbi=1)
            self.assertEqual(True, False, "should raise no player")
        except PlayerDoesNotExist:
            pass
        try:
            __ = Bat(1, 
                     999, 
                     1, 
                     "s", 
                     inning=1, 
                     rbi=1)
            self.assertEqual(True, False, "should raise no team")
        except TeamDoesNotExist:
            pass
        try:
            __ = Bat(1, 
                     1, 
                     999, 
                     "s", 
                     inning=1, 
                     rbi=1)
            self.assertEqual(True, False, "should raise no league")
        except GameDoesNotExist:
            pass

    def testBatUpdate(self):
        self.insertGame()
        # good bat
        b =  Bat(1, 
                 1, 
                 1, 
                 "s", 
                 inning=1, 
                 rbi=1)
        # now for the bad stuff
        try:
            b.update(player_id=1, 
                     team_id=1, 
                     game_id=1, 
                     hit="XX", 
                     inning=1, 
                     rbi=1)
            self.assertEqual(True, False, "should raise invalid field")
        except InvalidField:
            pass
        try:
            b.update(player_id=1, 
                     team_id=1, 
                     game_id=1, 
                     hit="s", 
                     inning=-1, 
                     rbi=1)
            self.assertEqual(True, False, "should raise invalid field")
        except InvalidField:
            pass
        try:
            b.update(player_id=1, 
                     team_id=1, 
                     game_id=1, 
                     hit="s", 
                     inning=1, 
                     rbi=1000)
            self.assertEqual(True, False, "should raise invalid field")
        except InvalidField:
            pass
        try:
            b.update(player_id=999, 
                     team_id=1, 
                     game_id=1, 
                     hit="s", 
                     inning=1, 
                     rbi=1)
            self.assertEqual(True, False, "should raise no player")
        except PlayerDoesNotExist:
            pass
        try:
            b.update(player_id=1, 
                     team_id=999, 
                     game_id=1, 
                     hit="s", 
                     inning=1, 
                     rbi=1)
            self.assertEqual(True, False, "should raise no team")
        except TeamDoesNotExist:
            pass
        try:
            b.update(player_id=1, 
                     team_id=1, 
                     game_id=999, 
                     hit="s", 
                     inning=1, 
                     rbi=1)
            self.assertEqual(True, False, "should raise no league")
        except GameDoesNotExist:
            pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()