'''
Created on Aug 21, 2015

@author: Dallas
'''
from api import DB
from werkzeug.security import generate_password_hash, check_password_hash
GENDERS = ['f', 'm']
HITS = ['s','ss', 'd', ',hr', 'k']

roster = DB.Table('roster',
                  DB.Column('player_id', DB.Integer, DB.ForeignKey('player.id')),
                  DB.Column('team_id', DB.Integer, DB.ForeignKey('team.id')),
                  DB.Column('year', DB.Integer)
                )

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
            self.gender = gender
        else:
            raise Exception("Invalid Gender")
        self.set_password(password)
     
    def set_password(self, password):
        self.password = generate_password_hash(password)
 
    def check_password(self, password):
        return check_password_hash(self.password, password)
 
    def __repr__(self):
        return self.name + " email:" + self.email
  
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
    def __init__(self, color=None):
        self.color = color

    def __repr__(self):
        result = []
        if self.color is not None:
            result.append( self.color)
        if self.sponsor_id is not None:
            result.append(str( Sponsor.query.get(self.sponsor_id)))
        return " ".join(result)

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
  
class League(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(120))
    games = DB.relationship('Game', backref='league', lazy='dynamic')
    teams = DB.relationship('Team', backref='league', lazy='dynamic')
    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return self.name

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
 
    def __init__(self, date):
        self.date = date

    def __rep__(self):
        return self.home_team_id + "vs" + self.away_team_id + " on " + self.date

class Bat(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    game_id = DB.Column(DB.Integer, DB.ForeignKey('game.id'))
    team_id = DB.Column(DB.Integer, DB.ForeignKey('team.id'))
    player_id = DB.Column(DB.Integer, DB.ForeignKey('player.id'))
    rbi = DB.Column(DB.Integer)
    inning = DB.Column(DB.Integer)
    classification =  DB.Column(DB.String(2))
  
    def __init__(self, classification=None, rbi=0):
        if classification is not None and classification not in HITS:
            raise Exception("Not a proper hit")
        self.classification = classification
        self.rbi = rbi
  
    def __rep__(self):
        return self.player.name  + "-" + self.classification + " in " + self.inning

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
        test = Player("Dallas", "fras2560@mylaurier.ca", gender="m", password="Don17wat")
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
        test = Player("Dallas", "fras2560@mylaurier.ca", gender="m", password="Don17wat")
        DB.session.add(test)
        DB.session.commit()
        dallas = Player.query.get(1)
        self.assertEqual(dallas.check_password("shit"), False)
        self.assertEqual(dallas.check_password("Don17wat"), True)
        DB.session.delete(test)

class TestTeam(BaseTest):
    def insertData(self):
        self.player = Player("Dallas",
                             "fras2560@mylaurier.ca",
                             gender="m",
                             password="Don17wat")
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
        self.team.players.append(self.player)
        DB.session.commit()
        print(self.team.players)
        print(self.player.teams.all())
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()