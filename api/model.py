'''
@author: Dallas Fraser
@author: 2015-08-27
@organization: MLSB API
@summary: Holds the model for the database
'''
from api import DB
from werkzeug.security import generate_password_hash, check_password_hash
from api.variables import BATS, GENDERS
from datetime import date, datetime


roster = DB.Table('roster',
                  DB.Column('player_id', DB.Integer, DB.ForeignKey('player.id')),
                  DB.Column('team_id', DB.Integer, DB.ForeignKey('team.id'))
                )

def insertPlayer(team_id, player_id, captain=False):
        valid = False
        if captain:
            team = Team.query.get(team_id)
            if team is not None:
                team.player_id = player_id
                DB.session.commit()
                valid = True
        else:
            player = Player.query.get(player_id)
            team = Team.query.get(team_id)
            if team is not None and player is not None:
                team.players.append(player)
                DB.session.commit()
                valid = True
        return valid

class Player(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(80))
    email = DB.Column(DB.String(120), unique=True)
    gender = DB.Column(DB.String(1))
    password = DB.Column(DB.String(120))
    bats = DB.relationship('Bat',
                             backref='player', lazy='dynamic')
    team = DB.relationship('Team',
                              backref='player',
                              lazy='dynamic')

    def __init__(self, name, email, gender=None, password="default"):
        self.name = name
        self.email = email
        if gender is not None or gender.lower() in GENDERS:
            self.gender = gender.lower()
        elif gender is None:
            self.gender = None
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
    year = DB.Column(DB.Integer)
    player_id = DB.Column(DB.Integer, DB.ForeignKey('player.id'))
    espys = DB.Column(DB.Integer)

    def __init__(self,
                 color=None,
                 sponsor_id=None,
                 league_id=None,
                 year=date.today().year,
                 espys=0):
        if year < 2013 and year > date.today().year:
            raise Exception("Invalid year")
        self.color = color
        self.sponsor_id = sponsor_id
        self.league_id = league_id
        self.year = year
        self.espys = espys

    def __repr__(self):
        result = []
        if self.sponsor_id is not None:
            result.append(str( Sponsor.query.get(self.sponsor_id)))
        if self.color is not None:
            result.append( self.color)
        return " ".join(result)

    def json(self):
        return{
               'team_id': self.id,
               'color': self.color,
               'sponsor_id': self.sponsor_id,
               'league_id': self.league_id,
               'year': self.year,
               'espys': self.espys}

class Sponsor(DB.Model):
    __tablename__ = 'sponsor'
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(120), unique=True)
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
    status = DB.Column(DB.String(120))
    field = DB.Column(DB.String(120))

    def __init__(self,
                 date,
                 home_team_id,
                 away_team_id,
                 league_id,
                 status="",
                 field=""):
        self.date = date
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.league_id = league_id
        self.status = status
        self.field = field

    def __repr__(self):
        home = str(Team.query.get(self.home_team_id))
        away = str(Team.query.get(self.away_team_id))
        result = (home + " vs " + away + " on " +
                  self.date.strftime("%Y-%m-%d %H:%M"))
        if self.field != "":
            result += " at " + self.field
        return result

    def json(self):
        return {
                'game_id': self.id,
                'home_team_id': self.home_team_id,
                'away_team_id': self.away_team_id,
                'league_id': self.league_id,
                'date': self.date.strftime("%Y-%m-%d"),
                'time': self.date.strftime("%H:%M"),
                'status':self.status,
                'field': self.field}

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
        if classification not in BATS:
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

    def json(self):
        return{
               'bat_id': self.id,
               'game_id':self.game_id,
               'team_id': self.team_id,
               'rbi': self.rbi,
               'hit': self.classification,
               'inning':self.inning,
               'player_id': self.player_id
               }

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()