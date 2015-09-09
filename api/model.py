'''
@author: Dallas Fraser
@author: 2015-08-27
@organization: MLSB API
@summary: Holds the model for the database
'''
from api import DB
from werkzeug.security import generate_password_hash, check_password_hash
GENDERS = ['f', 'm']
HITS = ['s','ss', 'd', 'hr', 'k']
from datetime import date, datetime


roster = DB.Table('roster',
                  DB.Column('player_id', DB.Integer, DB.ForeignKey('player.id')),
                  DB.Column('team_id', DB.Integer, DB.ForeignKey('team.id')),
                  DB.Column('year', DB.Integer),
                  DB.Column('captain', DB.Boolean)
                )

def insertPlayer(team_id, player_id, year, captain=False):
    if year > 2013 and year <= date.today().year:
        DB.session.execute(roster.insert(), params={"player_id": player_id,
                                            "team_id": team_id,
                                            "year": year,
                                            "captain": captain})
        DB.session.commit()
    else:
        raise Exception("Invalid year")

class Player(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(80))
    email = DB.Column(DB.String(120), unique=True)
    gender = DB.Column(DB.String(1))
    password = DB.Column(DB.String(120))
    bats = DB.relationship('Bat',
                             backref='player', lazy='dynamic')
    def __init__(self, name, email, gender=None, password="default"):
        self.name = name
        self.email = email
        if gender is None or gender.lower() in GENDERS:
            self.gender = gender.lower()
        else:
            raise Exception("Invalid Gender")
        self.set_password(password)
     
    def set_password(self, password):
        self.password = generate_password_hash(password)
 
    def check_password(self, password):
        return check_password_hash(self.password, password)
 
    def __repr__(self):
        return self.name + " email:" + self.email

    def json(self):
        return {"player_id": self.id,
                "player_name":self.name,
                "email": self.email,
                "gender": self.gender}
class Team(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    color = DB.Column(DB.String(120))
    sponsor_id = DB.Column(DB.Integer, DB.ForeignKey('sponsor.id'))
    home_games = DB.relationship('Game',
                                backref='home_team',
                                lazy = 'dynamic',
                                foreign_keys='[Game.home_team_id]')
    away_games = DB.relationship('Game',
                                backref='away_team',
                                lazy = 'dynamic',
                                foreign_keys='[Game.away_team_id]')
    players = DB.relationship('Player',
                              secondary=roster,
                              backref=DB.backref('teams', lazy='dynamic'))
    bats = DB.relationship('Bat',
                            backref='team',
                            lazy = 'dynamic')
    league_id = DB.Column(DB.Integer, DB.ForeignKey('league.id'))
    def __init__(self, color=None, sponsor_id=None, league_id=None):
        self.color = color
        self.sponsor_id = sponsor_id
        self.league_id = league_id

    def __repr__(self):
        result = []
        if self.color is not None:
            result.append( self.color)
        if self.sponsor_id is not None:
            result.append(str( Sponsor.query.get(self.sponsor_id)))
        return " ".join(result)

    def json(self):
        return{
               'team_id': self.id,
               'color': self.color,
               'sponsor_id': self.sponsor_id,
               'league_id': self.league_id}


class Sponsor(DB.Model):
    __tablename__ = 'sponsor'
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(120))
    teams = DB.relationship('Team', backref='sponsor',
                                lazy='dynamic')
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def json(self):
        return {'sponsor_id': self.id,
                'sponsor_name': self.name}

class League(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(120))
    games = DB.relationship('Game', backref='league', lazy='dynamic')
    teams = DB.relationship('Team', backref='league', lazy='dynamic')
    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return self.name

    def json(self):
        return {'league_id': self.id,
                'league_name': self.name}

class Game(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    home_team_id = DB.Column(DB.Integer, DB.ForeignKey('team.id',
                                                       use_alter=True,
                                                       name='fk_home_team_game'))
    away_team_id = DB.Column(DB.Integer, DB.ForeignKey('team.id',
                                                       use_alter=True,
                                                       name='fk_away_team_game'))
    league_id = DB.Column(DB.Integer, DB.ForeignKey('league.id'))
    bats = DB.relationship("Bat", backref="game", lazy='dynamic')
    date = DB.Column(DB.DateTime)
 
    def __init__(self, date, home_team_id, away_team_id, league_id):
        self.date = date
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.league_id = league_id

    def __repr__(self):
        home = str(Team.query.get(self.home_team_id))
        away = str(Team.query.get(self.away_team_id))
        return home + " vs " + away + " on " + self.date.strftime("%Y-%m-%d %H:%M")
    
    def json(self):
        return {
                'game_id': self.id,
                'home_team_id': self.home_team_id,
                'away_team_id': self.away_team_id,
                'league_id': self.league_id,
                'date': self.date.strftime("%Y-%m-%d %H:%M")}

class Bat(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    game_id = DB.Column(DB.Integer, DB.ForeignKey('game.id'))
    team_id = DB.Column(DB.Integer, DB.ForeignKey('team.id'))
    player_id = DB.Column(DB.Integer, DB.ForeignKey('player.id'))
    rbi = DB.Column(DB.Integer)
    inning = DB.Column(DB.Integer)
    classification =  DB.Column(DB.String(2))
  
    def __init__(self,
                 player_id,
                 team_id,
                 game_id,
                 classification,
                 inning,
                 rbi=0):
        classification = classification.lower().strip()
        if classification not in HITS:
            raise Exception("Not a proper hit")
        gender = Player.query.get(player_id)
        if classification == "SS" and gender != "f":
            raise Exception("Guys do not get SS")
        self.classification = classification
        self.rbi = rbi
        self.player_id = player_id
        self.team_id = team_id
        self.game_id = game_id
        if inning <= 0:
            raise Exception("Improper Inning")
        self.inning = inning
  
    def __repr__(self):
        player = Player.query.get(self.player_id)
        return (player.name  + "-" + self.classification + " in " 
                + str(self.inning))

import unittest
class BaseTest(unittest.TestCase):
    def setUp(self):
        DB.engine.execute('''   
                                DROP TABLE IF EXISTS roster;
                                DROP TABLE IF EXISTS bat;
                                DROP TABLE IF EXISTS game;
                                DROP TABLE IF EXISTS team;
                                DROP TABLE IF EXISTS player;
                                DROP TABLE IF EXISTS sponsor;
                                DROP TABLE IF EXISTS league;
                        ''')
        print("Starting Test")
        DB.create_all()

    def tearDown(self):
        pass

class TestPlayer(BaseTest):
    def testPlayerInsert(self):
        print("Player Test")
        test = Player("Dallas",
                      "fras2560@mylaurier.ca",
                      gender="m",
                      password="Password")
        DB.session.add(test)
        DB.session.commit()
        
        print("Player Added")
        self.assertEqual(str(test), "Dallas email:fras2560@mylaurier.ca")
        try:
            test = Player("Dallas", "fras2560@mylaurier.ca", gender="fuck")
            DB.session.add(test)
            DB.session.commit()
            self.assertEqual(False, True, "Should have raised exception")
        except:
            pass
        DB.sessision.delete(test)
    
    def testPlayerPassword(self):
        test = Player("Dallas",
                      "fras2560@mylaurier.ca",
                      gender="m",
                      password="Password")
        DB.session.add(test)
        DB.session.commit()
        dallas = Player.query.get(1)
        self.assertEqual(dallas.check_password("shit"), False)
        self.assertEqual(dallas.check_password("Password"), True)
        DB.session.delete(test)

class TestTeam(BaseTest):
    def insertData(self):
        self.player = Player("Dallas",
                             "fras2560@mylaurier.ca",
                             gender="m",
                             password="Password")
        DB.session.add(self.player)
        self.team = Team(color="Green")
        DB.session.add(self.team)
        self.sponsor = Sponsor("Domus")
        DB.session.add(self.sponsor)
        DB.session.commit()
        self.team.sponsor_id = self.sponsor.id

    def testRep(self):
        self.insertData()
        print(self.team)

    def testAddPlayer(self):
        self.insertData()
        insertPlayer(1, 1, 2015)
        self.assertEqual(self.team.players, [self.player])
        self.assertEqual(self.player.teams.all(), [self.team])

class TestGame(BaseTest):
    def insertData(self):
        self.teams = [Team(color="Green"), Team(color="Black")]
        for team in self.teams:
            DB.session.add(team)
        self.sponsors = [Sponsor("Domus"), Sponsor("Fat Bastards")]
        for sponsor in self.sponsors:
            DB.session.add(sponsor)
        DB.session.commit()
        for i in range(len(self.teams)):
            self.teams[i].sponsor_id = self.sponsors[i].id
        self.league = League(name="Monday/Wednesday")
        DB.session.add(self.league)
        DB.session.commit()
        
    def testGame(self):
        self.insertData()
        game = Game(datetime.now(),
                    self.teams[0].id,
                    self.teams[1].id,
                     self.league,id)
        DB.session.add(game)
        DB.session.commit()
        self.assertEqual("Green Domus vs Black Fat Bastards" in str(game), True)

class TestBat(BaseTest):
    def insertData(self):
        self.players = [Player("Dallas", "fras2560@mylaurier.ca", gender="m"),
                        Player("Girl", "rockon@hotmail.com", gender="f")]
        for player in self.players:
            DB.session.add(player)
        self.teams = [Team(color="Green"), Team(color="Black")]
        for team in self.teams:
            DB.session.add(team)
        self.sponsors = [Sponsor("Domus"), Sponsor("Fat Bastards")]
        for sponsor in self.sponsors:
            DB.session.add(sponsor)
        DB.session.commit()
        for i in range(len(self.teams)):
            self.teams[i].sponsor_id = self.sponsors[i].id
        self.league = League(name="Monday/Wednesday")
        DB.session.add(self.league)
        DB.session.commit()
        self.game = Game(datetime.now(),
                         self.teams[0].id,
                         self.teams[1].id,
                         self.league.id)
        DB.session.add(self.game)
        DB.session.commit()
    
    def testBat(self):
        self.insertData()
        bat = Bat(self.players[0].id,
                  self.teams[0].id,
                   self.game.id,
                   "HR",
                   1,
                   rbi=1)
        DB.session.add(bat)
        DB.session.commit()
        self.assertEqual("Dallas-hr in 1", str(bat))

    def testBadBat(self):
        self.insertData()
        try:
            bat = Bat(self.players[0].id,
                      self.teams[0].id,
                       self.game.id,
                       "SS",
                       1,
                       rbi=1)
            self.assertEqual(True, False, "Should have raised an exception")
        except:
            pass
    def testGoodBat(self):
        self.insertData()
        try:
            bat = Bat(self.players[1].id,
                      self.teams[0].id,
                       self.game.id,
                       "SS",
                       1,
                       rbi=1)
            self.assertEqual(True, True, "Should have raised an exception")
        except:
            self.assertEqual(True, False, "Should have not raised an exception")
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()