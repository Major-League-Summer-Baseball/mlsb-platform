'''
@author: Dallas Fraser
@author: 2016-04-12
@organization: MLSB API
@summary: Holds the model for the database
'''
from api import DB
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, datetime, time
from api.variables import HITS, KIKPOINTS
from api.errors import  TeamDoesNotExist, PlayerDoesNotExist, GameDoesNotExist,\
                        InvalidField, LeagueDoesNotExist, SponsorDoesNotExist,\
                        NonUniqueEmail, PlayerNotOnTeam
from api.validators import  rbi_validator, hit_validator, inning_validator,\
                            string_validator, date_validator, time_validator,\
                            field_validator, year_validator, gender_validator
roster = DB.Table('roster',
                  DB.Column('player_id', DB.Integer, DB.ForeignKey('player.id')),
                  DB.Column('team_id', DB.Integer, DB.ForeignKey('team.id'))
                )

SUBSCRIBED = "{} SUBSCRIBED"

class Fun(DB.Model):
    '''
        A class used to store the amount of fun had by all
        Columns:
            id: the unique id
            year: the year the fun count is for
            count: the total count for the year
    '''
    id = DB.Column(DB.Integer, primary_key=True)
    year = DB.Column(DB.Integer)
    count = DB.Column(DB.Integer)
    def __init__(self, year=date.today().year):
        self.year = year
        self.count = 0

    def increment(self, change):
        '''
        increasement the fun count
        Paramenters:
            change: the amount the fun count has changed by (int)
        '''
        self.count += change

class Espys(DB.Model):
    '''
        A class that stores transaction for ESPY points
        Columns:
            id: the unique id
            description: the description of the transaction (used for additional notes)
            sponsor_id: the id of sponsor that was involved in the transaction
            points: the amount of points awarded for the transaction ($1 is 1 point)
            date: the date of the transaction
            receipt: any information regarding the receipt (receipt number)
    '''
    id = DB.Column(DB.Integer, primary_key=True)
    team_id = DB.Column(DB.Integer, DB.ForeignKey('team.id'))
    description = DB.Column(DB.String(120))
    sponsor_id = DB.Column(DB.Integer, DB.ForeignKey('sponsor.id'))
    points = DB.Column(DB.Integer)
    date = DB.Column(DB.DateTime)
    receipt = DB.Column(DB.String(30))

    def __init__(self,
                 team_id,
                 sponsor_id=None,
                 description=None,
                 points=0,
                 receipt=None):
        '''
            Raises:
                SponsorDoesNotExist
                TeamDoesNotExist
        '''
        self.points = points
        self.date = datetime.now()
        sponsor = None
        if sponsor_id is not None:
            sponsor = Sponsor.query.get(sponsor_id)
        self.receipt = receipt
        if sponsor_id is not None and sponsor is None:
            raise SponsorDoesNotExist(payload={"details": sponsor_id})
        team = Team.query.get(team_id)
        if team is None:
            raise TeamDoesNotExist(payload={"details": team_id})
        self.description = description
        self.team_id = team_id
        self.sponsor_id = sponsor_id
        self.kik = None

    def update(self,
               team_id=None,
               sponsor_id=None,
               description=None,
               points=None,
               receipt=None):
        '''
            used to update an existing espy transaction
            Raises:
                TeamDoesNotExist
                SponsorDoesNotExist
        '''
        if points is not None:
            self.points = points
        if description is not None:
            self.description = description
        if team_id is not None:
            if Team.query.get(team_id) is not None:
                self.team_id = team_id
            else:
                raise TeamDoesNotExist(payload={"details": team_id})
        if sponsor_id is not None:
            if Sponsor.query.get(sponsor_id) is not None:
                self.sponsor_id = sponsor_id
            else:
                raise SponsorDoesNotExist(payload={"details": sponsor_id})
        if receipt is not None:
            self.receipt = receipt

    def json(self):
        '''
            returns a jsonserializable object
        '''
        if self.sponsor_id is not None:
            sponsor = str(Sponsor.query.get(self.sponsor_id))
        else:
            sponsor = None
        return {
                'espy_id': self.id,
                'team': str(Team.query.get(self.team_id)),
                'sponsor': sponsor,
                'description': self.description,
                'points': self.points,
                'receipt': self.receipt
                }

class Player(DB.Model):
    '''
    A class that stores a player's information
        id: the player's unique id
        name: the name of the player
        email: the unique player's email
        gender: the player's gender
        password: the password for the player
        team: the teams the player plays for
        active: a boolean to say whether the player is active currently or not (retired or not)
        kik: the kik user name associated with the player
    '''
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
    active = DB.Column(DB.Boolean)
    kik = DB.Column(DB.String(120))

    def __init__(self,
                 name,
                 email,
                 gender=None,
                 password="default",
                 active=True):
        '''
            Raises:
                InvalidField
                NonUniqueEmail
        '''
        if not string_validator(name):
            raise InvalidField(payload={"details": "Player - name"})
        # check if email is unique
        if not string_validator(email):
            raise InvalidField(payload={'details':"Player - email"})
        player = Player.query.filter_by(email=email).first()
        if player is not None:
            raise NonUniqueEmail(payload={'details':email})
        if gender is not None and not gender_validator(gender):
            raise InvalidField(payload={'details':"Player - gender"})
        self.name = name
        self.email = email
        if gender is not None:
            gender = gender.lower()
        self.gender = gender
        self.set_password(password)
        self.active = active

    def set_password(self, password):
        '''
            update a player's password
            Parameters:
                password: the player's new password (str)
        '''
        self.password = generate_password_hash(password)
 
    def check_password(self, password):
        '''
            check a player's password
            Paramters:
                password: attempted password (str)
            Returns:
                True passwords match
                False otherwise
        '''
        return check_password_hash(self.password, password)
 
    def __repr__(self):
        '''
            the string representation of the player
        '''
        return self.name + " email:" + self.email

    def update_kik(self, kik):
        '''
        update the player's kik profile
        '''
        self.kik = kik

    def json(self):
        '''
            returns a jsonserializable object
        '''
        return {"player_id": self.id,
                "player_name":self.name,
                "email": self.email,
                "gender": self.gender}

    def update(self,
               name=None,
               email=None,
               gender=None,
               password=None):
        '''
        updates an existing player
            Parameters:
                name: the name of the player
                email: the unique email of the player
                gender: the gender of the player
                password: the password of the player
            Raises:
                InvalidField
                NonUniqueEmail
        '''
        if email is not None:   
            # check if email is unique
            if not string_validator(email):
                raise InvalidField(payload="Player - email")
            player = Player.query.filter_by(email=email).first()
            if player is not None:
                raise NonUniqueEmail(payload={'details':email})
            self.email = email
        if gender is not None and gender_validator(gender):
            self.gender = gender.lower()
        elif gender is not None:
            raise InvalidField(payload={'details':"Player - gender"})
        if name is not None and string_validator(name):
            self.name = name
        elif name is not None:
            raise InvalidField(payload={'details':"Player - name"})

    def activate(self):
        '''
        activate the player
        '''
        self.active = True

    def deactivate(self):
        '''
        deactivate the player (retire them)
        '''
        self.active = False

class Team(DB.Model):
    '''
    A class that stores information about a team
    Columns:
        id: the unique team id
        sponsor_id: the sponsor id the team is associated with
        home_games: the home games of the team
        away_games: the away games of the team
        players: the players on the team's roster
        bats: the bats of the team
        league_id: the league id the team is part of
        year: the year the team played
        espys: the espy transaction that team has
    '''
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
    espys = DB.relationship('Espys',
                            backref='team',
                            lazy='dynamic')

    def __init__(self,
                 color=None,
                 sponsor_id=None,
                 league_id=None,
                 year=date.today().year):
        '''
        Raises
            InvalidField
            SponsorDoesNotExist
            LeagueDoesNotExist
        '''
        if color is not None and not string_validator(color):
            raise InvalidField(payload={'details':"Team - color"})
        if sponsor_id is not None and Sponsor.query.get(sponsor_id) is None:
            raise SponsorDoesNotExist(payload={'details':sponsor_id})
        if league_id is not None and League.query.get(league_id) is None:
            raise LeagueDoesNotExist(payload={'details':league_id})
        if year is not None and not year_validator(year):
            raise InvalidField(payload={'details':"Team - year"})
        self.color = color
        self.sponsor_id = sponsor_id
        self.league_id = league_id
        self.year = year
        self.kik = None

    def __repr__(self):
        '''
            the string representation
        '''
        result = []
        if self.sponsor_id is not None:
            result.append(str( Sponsor.query.get(self.sponsor_id)))
        if self.color is not None:
            result.append( self.color)
        return " ".join(result)

    def espys_awarded(self):
        '''
            returns the number of espy ponts the team has
        '''
        count = 0
        for espy in self.espys:
            count += espy.points
        return count

    def json(self):
        '''
            returns a jsonserializable object
        '''
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
               'espys': self.espys_awarded(),
               'captain': captain}

    def update(self,
               color=None,
               sponsor_id=None,
               league_id=None,
               year=None):
        '''
        updates an existing team
        Raises:
            InvalidField
            SponsorDoesNotExist
            LeagueDoesNotExist
        '''
        # does nothing with espys given
        if color is not None and string_validator(color):
            self.color = color
        elif color is not None:
            raise InvalidField(payload={'details':"Team - color"})
        if sponsor_id is not None and Sponsor.query.get(sponsor_id) is not None:
            self.sponsor_id = sponsor_id
        elif sponsor_id is not None:
            raise SponsorDoesNotExist(payload={'details':sponsor_id})
        if league_id is not None and League.query.get(league_id) is not None:
            self.league_id = league_id
        elif league_id  is not None:
            raise LeagueDoesNotExist(payload={'details':league_id})
        if year is not None and year_validator(year):
            self.year = year
        elif year is not None:
            raise InvalidField(payload={'details':"Team - year"})

    def insert_player(self, player_id, captain=False):
        '''
        insert a player on to the team
        Parameter:
            player_id: the id of the player to add
            captain: True if the player is the team's captain
        Returns:
            True if player was added
            False otherwise
        Raises:
            PlayerDoesNotExist
        '''
        valid = False
        player = Player.query.get(player_id)
        if player is None:
            raise PlayerDoesNotExist(payload={'details':player_id})
        if captain:
            self.player_id = player_id
        else:
            self.players.append(player)
        return valid

    def remove_player(self, player_id):
        '''
        removes a player from a team
        Parameter:
            player_id: the id of the player to remove
        Raises:
            MissingPlayer
        '''
        if self.player_id == player_id:
            self.player_id = None
        else:
            player = Player.query.get(player_id)
            if player not in self.players:
                raise PlayerNotOnTeam(payload={'details':player_id})
            self.players.remove(player)
        
    def check_captain(self, player_name, password):
        '''
        checks if the player is the captain of the team
        Parameters:
            player_name: the name of the player (str)
            password: the password of the player (str)
        Return:
            True of player is the captain
            False otherwise
        '''
        player = Player.query.get(self.player_id)
        return player.name == player_name and player.check_password(password)

    def team_stats(self):
        pass

class Sponsor(DB.Model):
    '''
    A class that stores information about a sponsor
    Columns:
        id: the sponsor's unique id
        name: the name of the sponsor
        teams: the teams the sponsor is associated with
        description: a description of the sponsor
        link: a link to the sponsor's website or facebook
        active: a boolean telling whether the sponsor is currently sponsoring a team
        espys: all the espys transaction associated with the sponsor
    '''
    __tablename__ = 'sponsor'
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(120), unique=True)
    teams = DB.relationship('Team', backref='sponsor',
                                lazy='dynamic')
    description = DB.Column(DB.String(200))
    link = DB.Column(DB.String(100))
    active = DB.Column(DB.Boolean)
    espys = DB.relationship('Espys', backref='sponsor', lazy='dynamic')
    def __init__(self, name, link=None, description=None, active=True):
        if not string_validator(name):
            raise InvalidField(payload={'details':"Sponsor - name"})
        if not string_validator(link):
            raise InvalidField(payload={'details':"Sponsor - link"})
        if not string_validator(description):
            raise InvalidField(payload={'details':"Sponsor - description"})
        self.name = name
        self.description = description
        self.link = link
        self.active = True

    def __repr__(self):
        '''
            the string representation of the sponsor
        '''
        return self.name

    def json(self):
        '''
            returns a jsonserializable object
        '''
        return {'sponsor_id': self.id,
                'sponsor_name': self.name,
                'link': self.link,
                'description': self.description}

    def update(self, name=None, link=None, description=None):
        '''
            updates an existing sponsor
            Raises:
                InvalidField
        '''
        if name is not None and string_validator(name):
            self.name = name
        elif name is not None:
            raise InvalidField(payload={'details':"Sponsor - name"})
        if description is not None and string_validator(description):
            self.description = description
        elif description is not None:
            raise InvalidField(payload={'details':"Sponsor - description"})
        if link is not None and string_validator(link):
            self.link = link
        elif link is not None:
            raise InvalidField(payload={'details':"Sponsor - link"})

    def activate(self):
        '''
        activate a sponsor (they are back baby)
        '''
        self.active = True

    def deactivate(self):
        '''
        deactivate a sponsor (they are no longer sponsoring)
        '''
        self.active = False

class League(DB.Model):
    '''
    a class that holds all the information for a league
    Columns:
        id: the league unique id
        name: the name of the league
        games: the games associated with the league
        teams: the teams part of the league
    '''
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(120))
    games = DB.relationship('Game', backref='league', lazy='dynamic')
    teams = DB.relationship('Team', backref='league', lazy='dynamic')
    def __init__(self, name=None):
        '''
        Raises:
            InvalidField
        '''
        if not string_validator(name):
            raise InvalidField(payload={'details':"League - name"})
        self.name = name

    def __repr__(self):
        return self.name

    def json(self):
        return {'league_id': self.id,
                'league_name': self.name}

    def update(self, league):
        '''
        updates an existing league
        Raises:
            InvalidField
        '''
        if not string_validator(league):
            raise InvalidField(payload={'details':"League - name"})
        self.name= league

class Game(DB.Model):
    '''
    A class that holds information about a Game
    Columns:
        id: the game id
        home_team_id: the home team's id
        away_team_id: the away team's id
        league_id: the league id the game is part of
        date: the date of the game
        status: the status of the game
        field: the field the game is to be played on
    '''
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
        '''
        Raises:
            InvalidField
            TeamDoesNotExist
            LeagueDoesNotExist
        '''
        # check for all the invalid parameters
        if not date_validator(date):
            raise InvalidField(payload={'details':"Game - date"})
        if not time_validator(time):
            raise InvalidField(payload={'details':"Game - time"})
        self.date = datetime.strptime(date + "-" +time, '%Y-%m-%d-%H:%M')
        if (Team.query.get(home_team_id) is None):
            raise TeamDoesNotExist(payload={'details':home_team_id})
        if Team.query.get(away_team_id) is None:
            raise TeamDoesNotExist(payload={'details':away_team_id})
        if League.query.get(league_id) is None:
            raise LeagueDoesNotExist(payload={'details':league_id})
        if ((status != "" and  not string_validator(status)) 
            or (field != "" and not field_validator(field))):
            raise InvalidField(payload={'details':"Game - field/status"})
        # must be good now
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.league_id = league_id
        self.status = status
        self.field = field

    def __repr__(self):
        '''
            the string representation of the game
        '''
        home = str(Team.query.get(self.home_team_id))
        away = str(Team.query.get(self.away_team_id))
        result = (home + " vs " + away + " on " +
                  self.date.strftime("%Y-%m-%d %H:%M"))
        if self.field != "":
            result += " at " + self.field
        return result

    def json(self):
        '''
            returns a jsonserializable object
        '''
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
        '''
        updates an existing game
        Raises:
            InvalidField
            TeamDoesNotExist
            LeagueDoesNotExist
        '''
        d = self.date.strftime("%Y-%m-%d")
        t = self.date.strftime("%H:%M")
        if date is not None and date_validator(date):
            d = date
        elif date is not None:
            raise InvalidField(payload={'details':"Game - date"})
        if time is not None and time_validator(time):
            t = time
        elif time is not None:
            raise InvalidField(payload={'details':"Game - time"})
        if (home_team_id is not None
            and Team.query.get(home_team_id) is not None):
            self.home_team_id = home_team_id
        elif home_team_id is not None:
            raise TeamDoesNotExist(payload={'details':home_team_id})
        if (away_team_id is not None
            and Team.query.get(away_team_id) is not None):
            self.away_team_id = away_team_id
        elif away_team_id is not None:
            raise TeamDoesNotExist(payload={'details':away_team_id})
        if league_id is not None and League.query.get(league_id) is not None:
            self.league_id = league_id
        elif league_id is not None:
            raise LeagueDoesNotExist(payload={'details':league_id})
        if status is not None and string_validator(status):
            self.status = status
        elif status is not None:
            raise InvalidField(payload={'details':"Game - status"})
        if field is not None and field_validator(field):
            self.field = field
        elif field is not None:
            raise InvalidField(payload={'details':"Game - field"})
        # worse case just overwrites it with same date or time
        self.date = datetime.strptime(d + "-" +t, '%Y-%m-%d-%H:%M')

    def summary(self):
        '''
        returns a game summary
        Returns:
            {
            away_score: int,
            away_bat: [Bat,],
            home_score: int,
            home_bats: [Bat, ]
            }
        '''
        away_score = DB.session.query(
                                      func.sum(Bat.rbi)
                                      .filter(Bat.game_id==self.id)
                                      .filter(Bat.team_id==self.away_team_id)
                                      ).first()[0]
        away_bats  = DB.session.query(
                                      func.count(Bat.classification)
                                      .filter(Bat.game_id==self.id)
                                      .filter(Bat.team_id==self.away_team_id)
                                      .filter(Bat.classification.in_(HITS))
                                      ).first()[0]
        home_score = DB.session.query(
                                      func.sum(Bat.rbi)
                                      .filter(Bat.game_id==self.id)
                                      .filter(Bat.team_id==self.home_team_id)
                                      ).first()[0]

        home_bats  = DB.session.query(
                                      func.count(Bat.classification)
                                      .filter(Bat.game_id==self.id)
                                      .filter(Bat.team_id==self.home_team_id)
                                      .filter(Bat.classification.in_(HITS))
                                      ).first()[0]
        if away_score is None:
            away_score = 0
        if home_score is None:
            home_score = 0
        if away_bats is None:
            away_bats = 0
        if home_bats is None:
            home_bats = 0
        return {
                'away_score': away_score,
                'away_bats': away_bats,
                'home_score': home_score,
                'home_bats': home_bats
                }

class Bat(DB.Model):
    '''
    A class that stores information about a Bat
    Columns:
        id: the bat id
        game_id: the game that bat took place in
        team_id: the team the bat was for
        player_id: the player who took the bat
        rbi: the number of runs batted in
        inning: the inning the bat took place
        classification: how the bat would be classified (see BATS)
    '''
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
        '''
        Raises:
            PlayerDoesNotExist
            InvalidField
            TeamDoesNotExist
            GameDoesNotExist
        '''
        # check for exceptions
        classification = classification.lower().strip()
        player = Player.query.get(player_id)
        if player is None:
            raise PlayerDoesNotExist(payload={'details':player_id})
        if not hit_validator(classification, player.gender):
            raise InvalidField(payload={'details':"Bat - hit"})
        if not rbi_validator(rbi):
            raise InvalidField(payload={'details':"Bat - rbi"})
        if not inning_validator(inning):
            raise InvalidField(payload={'details':"Bat - inning"})
        if Team.query.get(team_id) is None:
            raise TeamDoesNotExist(payload={'details':team_id})
        if Game.query.get(game_id) is None:
            raise GameDoesNotExist(payload={'details':game_id})
        # otherwise good and a valid object
        self.classification = classification
        self.rbi = rbi
        self.player_id = player_id
        self.team_id = team_id
        self.game_id = game_id
        self.inning = inning

    def __repr__(self):
        '''
            the string representation of the Bat
        '''        
        player = Player.query.get(self.player_id)
        return (player.name  + "-" + self.classification + " in " 
                + str(self.inning))

    def json(self):
        '''
            returns a jsonserializable object
        '''
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
        '''
        update a existing bat
        Raises:
            TeamDoesNotExist
            GameDoesNotExist
            PlayerDoesNotExist
            InvalidField
        '''
        if team_id is not None and Team.query.get(team_id) is not None:
            self.team_id = team_id
        elif team_id is not None:
            raise TeamDoesNotExist(payload={'details':team_id})
        if game_id is not None and Game.query.get(game_id) is not None:
            self.game_id = game_id
        elif game_id is not None:
            raise GameDoesNotExist(payload={'details':game_id})
        if player_id is not None and Player.query.get(player_id) is not None:
            self.player_id = player_id
        elif player_id is not None:
            raise PlayerDoesNotExist(payload={'details':player_id})
        if rbi is not None and rbi_validator(rbi):
            self.rbi = rbi
        elif rbi is not None:
            raise InvalidField(payload={'details':"Bat - rbi"})
        if hit is not None and hit_validator(hit):
            self.hit = hit
        elif hit is not None:
            raise InvalidField(payload={'details':"Bat - hit"})
        if inning is not None and inning_validator(inning):
            self.inning = inning
        elif inning is not None:
            raise InvalidField(payload={'details':"Bat - inning"})

def subscribe(kik, name, team_id):
    '''
    a function used to subscribe a kik user name to a player
    Parameters:
        kik: the kik user name
        name: the name of the player
        team_id: the id of the team the player belongs to
    Returns:
        True
    Raises:
        TeamDoesNotExist
        PlayerNotOnTeam
    '''
    team = Team.query.get(team_id)
    if team is None:
        # wrong team was given
        raise TeamDoesNotExist(payload={'details':team_id})
    found = False
    player = None
    for p in team.players:
        if p.name == name:
            found = True
            player = p
            break
    if not found:
        # player is not on the team
        raise PlayerNotOnTeam(payload={'details':"{}".format(name, str(team))})
    player.kik = kik
    espy = Espys.query.filter_by(team_id=team_id).filter_by(description=SUBSCRIBED.format(str(player))).first()
    points = KIKPOINTS
    if espy is not None:
        # player already subscribed to this team
        # no points awarded
        points = 0
    espy = Espys(team_id, description = SUBSCRIBED.format(str(player)), points=points)
    DB.session.add(espy)
    DB.session.commit()
    return True

def find_team_subscribed(kik):
    '''
    a function to find the team the kik user name is subscribed to
    Parameters;
        kik: the kik user name
    Returns:
        result: a list of team's id

    '''
    result = []
    t1 = time(0, 0)
    t2 = time(0 , 0)
    d1 = date(date.today().year, 1, 1)
    d2 = date(date.today().year, 12, 30)
    start = datetime.combine(d1, t1)
    end = datetime.combine(d2, t2)
    player = Player.query.filter_by(kik=kik).one()
    if player is not None:
        teams = DB.session.query(Espys).filter(Espys.data.between(start, end))
        teams = teams.filter_by(description=SUBSCRIBED.format(str(player))).order_by("date").all()
        for team in teams:
            result.append(team.team_id)
    return result

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()