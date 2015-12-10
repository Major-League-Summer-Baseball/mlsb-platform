'''
@author: Dallas Fraser
@author: 2015-08-27
@organization: MLSB API
@summary: Holds the model for the database
'''
from api import DB
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, datetime
from api.errors import  TeamDoesNotExist, PlayerDoesNotExist, GameDoesNotExist,\
                        InvalidField, LeagueDoesNotExist, SponsorDoesNotExist,\
                        NonUniqueEmail, MissingPlayer
from api.validators import  rbi_validator, hit_validator, inning_validator,\
                            string_validator, date_validator, time_validator,\
                            field_validator, year_validator, int_validator,\
                            gender_validator
from nt import link
import email

roster = DB.Table('roster',
                  DB.Column('player_id', DB.Integer, DB.ForeignKey('player.id')),
                  DB.Column('team_id', DB.Integer, DB.ForeignKey('team.id'))
                )

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

    def __init__(self,
                 name,
                 email,
                 gender=None,
                 password="default"):
        if not string_validator(name):
            raise InvalidField("Invalid name for Player")
        # check if email is unique
        if not string_validator(email):
            raise InvalidField("Invalid email for Player")
        player = Player.query.filter_by(email=email).first()
        if player is not None:
            raise NonUniqueEmail("Email is a duplicate - {}".format(email))
        if not string_validator(email):
            raise InvalidField("Invalid email for Player")
        if gender is not None and not gender_validator(gender):
            raise InvalidField("Invalid gender for Player")
        self.name = name
        self.email = email
        if gender is not None:
            gender = gender.lower()
        self.gender = gender
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

    def update(self,
               name=None,
               email=None,
               gender=None,
               password=None):
        if email is not None:   
            # check if email is unique
            if not string_validator(email):
                raise InvalidField("Invalid email for Player")
            player = Player.query.filter_by(email=email).first()
            if player is not None:
                raise NonUniqueEmail("Email was a duplicate {}".format(email))
            self.email = email
        if gender is not None and gender_validator(gender):
            self.gender = gender.lower()
        elif gender is not None:
            raise InvalidField("Invalid gender for Player")
        if name is not None and string_validator(name):
            self.name = name
        elif name is not None:
            raise InvalidField("Invalid name for Player")

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
        if color is not None and not string_validator(color):
            raise InvalidField("Invalid color for Team")
        if sponsor_id is not None and Sponsor.query.get(sponsor_id) is None:
            message = "Sponsor does not Exist {}".format(sponsor_id)
            raise SponsorDoesNotExist(message)
        if league_id is not None and League.query.get(league_id) is None:
            message = "League does not Exist {}".format(league_id)
            raise LeagueDoesNotExist(message)
        if year is not None and not year_validator(year):
            raise InvalidField("Invalid year for Team")
        if espys is not None and not int_validator(espys):
            raise InvalidField("Invalid espys for Team")
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
        captain = None
        if self.player_id is not None:
            captain = Player.query.get(self.player_id).json()
        return{
               'team_id': self.id,
               'team_name': str(self),
               'color': self.color,
               'sponsor_id': self.sponsor_id,
               'league_id': self.league_id,
               'year': self.year,
               'espys': self.espys,
               'captain': captain}

    def update(self,
               color=None,
               sponsor_id=None,
               league_id=None,
               year=None,
               espys=None):
        if color is not None and string_validator(color):
            self.color = color
        elif color is not None:
            raise InvalidField("Invalid color for Team")
        if sponsor_id is not None and Sponsor.query.get(sponsor_id) is not None:
            self.sponsor_id = sponsor_id
        elif sponsor_id is not None:
            message = "Sponsor does not Exist {}".format(sponsor_id)
            raise SponsorDoesNotExist(message)
        if league_id is not None and League.query.get(league_id) is not None:
            self.league_id = league_id
        elif league_id  is not None:
            message = "League does not Exist {}".format(league_id)
            raise LeagueDoesNotExist(message)
        if year is not None and year_validator(year):
            self.year = year
        elif year is not None:
            raise InvalidField("Invalid year for Team")
        if espys is not None and int_validator(espys):
            self.espys = espys
        elif espys is not None:
            raise InvalidField("Invalid espys for Team")

    def insert_player(self, player_id, captain=False):
        valid = False
        player = Player.query.get(player_id)
        if player is None:
            raise PlayerDoesNotExist("Player does not Exist {}".format(player_id))
        if captain:
            self.player_id = player_id
        else:
            self.players.append(player)
        return valid

    def remove_player(self, player_id):
        if self.player_id == player_id:
            self.player_id = None
        else:
            player = Player.query.get(player_id)
            if player not in self.players:
                raise MissingPlayer("Player was not a member of the team")
        
    def check_captain(self, player_name, password):
        player = Player.query.get(self.player_id)
        return player.name == player_name and player.check_password(password)

class Sponsor(DB.Model):
    __tablename__ = 'sponsor'
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(120), unique=True)
    teams = DB.relationship('Team', backref='sponsor',
                                lazy='dynamic')
    description = DB.Column(DB.String(200))
    link = DB.Column(DB.String(100))
    
    def __init__(self, name, link=None, description=None):
        if not string_validator(name):
            raise InvalidField("Invalid name for Sponsor")
        if not string_validator(link):
            raise InvalidField("Invalid link for Sponsor")
        if not string_validator(description):
            raise InvalidField("Invalid description for Sponsor")
        self.name = name
        self.description = description
        self.link = link

    def __repr__(self):
        return self.name

    def json(self):
        return {'sponsor_id': self.id,
                'sponsor_name': self.name,
                'link': self.link,
                'description': self.description}

    def update(self, name=None,link=None, description=None):
        if name is not None and string_validator(name):
            self.name = name
        elif name is not None:
            raise InvalidField("Invalid name for Sponsor")
        if description is not None and string_validator(description):
            self.description = description
        elif description is not None:
            raise InvalidField("Invalid description for Sponsor")
        if link is not None and string_validator(link):
            self.link = link
        elif link is not None:
            raise InvalidField("Invalid link for Sponsor")

class League(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(120))
    games = DB.relationship('Game', backref='league', lazy='dynamic')
    teams = DB.relationship('Team', backref='league', lazy='dynamic')
    def __init__(self, name=None):
        if not string_validator(name):
            raise InvalidField("Invalid name for League")
        self.name = name

    def __repr__(self):
        return self.name

    def json(self):
        return {'league_id': self.id,
                'league_name': self.name}

    def update(self, league):
        if not string_validator(league):
            raise InvalidField("Invalid name for League")
        self.name= league

    
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
                 time,
                 home_team_id,
                 away_team_id,
                 league_id,
                 status="",
                 field=""):
        # check for all the invalid parameters
        if not date_validator(date):
            raise InvalidField("Invalid date for Game")
        if not time_validator(time):
            raise InvalidField("Invalid time for Game")
        self.date = datetime.strptime(date + "-" +time, '%Y-%m-%d-%H:%M')
        if (Team.query.get(home_team_id) is None):
            message = "Game does not Exist {}".format(home_team_id)
            raise TeamDoesNotExist(message)
        if Team.query.get(away_team_id) is None:
            message = "Game does not Exist {}".format(away_team_id)
            raise TeamDoesNotExist(message)
        if League.query.get(league_id) is None:
            raise LeagueDoesNotExist("League does not Exist {}".format(league_id))
        if ((status != "" and  not string_validator(status)) 
            or (field != "" and not field_validator(field))):
            raise InvalidField("Invalid status/field for Game")
        # must be good now
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
                'home_team': str(Team.query.get(self.home_team_id)),
                'away_team_id': self.away_team_id,
                'away_team': str(Team.query.get(self.away_team_id)),
                'league_id': self.league_id,
                'date': self.date.strftime("%Y-%m-%d"),
                'time': self.date.strftime("%H:%M"),
                'status':self.status,
                'field': self.field}

    def update(self,
               date=None,
               time=None,
               home_team_id=None,
               away_team_id=None,
               league_id=None,
               status=None,
               field=None):
        d = self.date.strftime("%Y-%m-%d")
        t = self.date.strftime("%H:%M")
        if date is not None and date_validator(date):
            d = date
        elif date is not None:
            raise InvalidField("Invalid date for Game")
        if time is not None and time_validator(time):
            t = time
        elif time is not None:
            raise InvalidField("Invalid time for Game")
        if (home_team_id is not None
            and Team.query.get(home_team_id) is not None):
            self.home_team_id = home_team_id
        elif home_team_id is not None:
            raise TeamDoesNotExist("Team does not Exist {}".format(home_team_id))
        if (away_team_id is not None
            and Team.query.get(away_team_id) is not None):
            self.away_team_id = away_team_id
        elif away_team_id is not None:
            raise TeamDoesNotExist("Team does not Exist {}".format(away_team_id))
        if league_id is not None and League.query.get(league_id) is not None:
            self.league_id = league_id
        elif league_id is not None:
            raise LeagueDoesNotExist("League does not Exist {}".format(league_id))
        if status is not None and string_validator(status):
            self.status = status
        elif status is not None:
            raise InvalidField("Invalid status for Game")
        if field is not None and field_validator(field):
            self.field = field
        elif field is not None:
            raise InvalidField("Invalid field for Game")
        # worse case just overwrites it with same date or time
        self.date = datetime.strptime(d + "-" +t, '%Y-%m-%d-%H:%M')

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
                 inning=1,
                 rbi=0):
        # check for exceptions
        classification = classification.lower().strip()
        player = Player.query.get(player_id)
        if player is None:
            raise PlayerDoesNotExist("Player does not Exist {}".format(player_id))
        print(hit_validator(classification, player.gender))
        if not hit_validator(classification, player.gender):
            raise InvalidField("Invalid hit for Bat")
        if not rbi_validator(rbi):
            raise InvalidField("Invalid rbi for Bat")
        if not inning_validator(inning):
            raise InvalidField("Invalid inning for Bat")
        if Team.query.get(team_id) is None:
            raise TeamDoesNotExist("Team does not Exist {}".format(team_id))
        if Game.query.get(game_id) is None:
            raise GameDoesNotExist("Game does not Exist {}".format(game_id))
        # otherwise good and a valid object
        self.classification = classification
        self.rbi = rbi
        self.player_id = player_id
        self.team_id = team_id
        self.game_id = game_id
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
               'team': str(Team.query.get(self.team_id)),
               'rbi': self.rbi,
               'hit': self.classification,
               'inning':self.inning,
               'player_id': self.player_id,
               'player': str(Player.query.get(self.player_id))
               }

    def update(self,
               player_id=None,
               team_id=None,
               game_id=None,
               rbi=None,
               hit=None,
               inning=None):
        if team_id is not None and Team.query.get(team_id) is not None:
            self.team_id = team_id
        elif team_id is not None:
            raise TeamDoesNotExist("Team does not Exist {}".format(team_id))
        if game_id is not None and Game.query.get(game_id) is not None:
            self.game_id = game_id
        elif game_id is not None:
            raise GameDoesNotExist("Game does not Exist {}".format(game_id))
        if player_id is not None and Player.query.get(player_id) is not None:
            self.player_id = player_id
        elif player_id is not None:
            raise PlayerDoesNotExist("Player does not Exist {}".format(player_id))
        if rbi is not None and rbi_validator(rbi):
            self.rbi = rbi
        elif rbi is not None:
            raise InvalidField("Invalid rbi for Bat")
        if hit is not None and hit_validator(hit):
            self.hit = hit
        elif hit is not None:
            raise InvalidField("Invalid hit for Bat")
        if inning is not None and inning_validator(inning):
            self.inning = inning
        elif inning is not None:
            raise InvalidField("Invalid inning for Bat")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()