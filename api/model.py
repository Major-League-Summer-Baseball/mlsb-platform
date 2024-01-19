from datetime import date, datetime
from sqlalchemy.orm import column_property
from sqlalchemy import and_, select, func, or_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from api.extensions import DB
from api.errors import TeamDoesNotExist, PlayerDoesNotExist, GameDoesNotExist, \
    InvalidField, LeagueDoesNotExist, SponsorDoesNotExist, \
    NonUniqueEmail, PlayerNotOnTeam, DivisionDoesNotExist, \
    HaveLeagueRequestException, LeagueEventDoesNotExist
from api.validators import rbi_validator, hit_validator, inning_validator, \
    string_validator, date_validator, time_validator, \
    field_validator, year_validator, gender_validator, \
    float_validator, boolean_validator


roster = DB.Table('roster',
                  DB.Column('player_id',
                            DB.Integer,
                            DB.ForeignKey('player.id')),
                  DB.Column('team_id', DB.Integer, DB.ForeignKey('team.id'))
                  )
attendance = DB.Table('attendance', DB.Column('player_id',
                                              DB.Integer,
                                              DB.ForeignKey('player.id')),
                      DB.Column('league_event_date_id',
                                DB.Integer,
                                DB.ForeignKey('league_event_date.id'))
                      )
SUBSCRIBED = "{} SUBSCRIBED"
AWARD_POINTS = "{} awarded espy points for subscribing: {}"


def convert_date(date_string: str, time_string: str) -> datetime:
    """Converts a date and time strings to datetime object."""
    return datetime.strptime(date_string + "-" + time_string, '%Y-%m-%d-%H:%M')


def split_datetime(date: datetime) -> tuple[str, str]:
    """Splits the datetime to their equivalent date and time string."""
    return (
        None if date is None else date.strftime("%Y-%m-%d"),
        None if date is None else date.strftime("%H:%M")
    )


class LeagueEvent(DB.Model):
    """
        A class used to store league events like Summerween.
        Columns:
            id: the unique id
            name: the name of the event
            description: the description of the
    """
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(80))
    description = DB.Column(DB.Text())
    active = DB.Column(DB.Boolean())

    def __init__(self, name: str, description: str, active: bool = True):
        """ League event constructor. """
        if not string_validator(name):
            raise InvalidField(payload={"details": "League event - name"})
        if not string_validator(description):
            payload = {"details": "League event - description"}
            raise InvalidField(payload=payload)
        if not boolean_validator(active):
            raise InvalidField(payload={"details": "League event - active"})
        self.name = name
        self.description = description
        self.active = active

    def update(self, name=None, description=None, active=None) -> None:
        """Update a league event.

            Parameters:
                name: the league event new name (optional str)
                description: the league event new description (optional str)
                active: is the event active or not (optional str)
        """
        if name is not None:
            if not string_validator(name):
                raise InvalidField(payload={"details": "League event - name"})
            self.name = name

        if description is not None:
            if not string_validator(description):
                load = {"details": "League event - description"}
                raise InvalidField(payload=load)
            self.description = description

        if active is not None:
            if not boolean_validator(active):
                raise InvalidField(payload={'detail': "League Event - active"})
            self.active = active

    def json(self) -> dict:
        """Returns a jsonserializable object."""
        return {
            "league_event_id": self.id,
            "name": self.name,
            "description": self.description,
            "active": self.active
        }

    @classmethod
    def is_league_event(cls, league_event_id: str) -> bool:
        return LeagueEvent.query.get(league_event_id) is not None


class LeagueEventDate(DB.Model):
    """
        A class used to store the dates of league events.
        Columns:
            id: the unique id
            league_event_id: the league event
            date: the date of the event for some year
    """
    id = DB.Column(DB.Integer, primary_key=True)
    event = DB.relationship('LeagueEvent',
                            backref=DB.backref('event', uselist=False))
    league_event_id = DB.Column(DB.Integer, DB.ForeignKey('league_event.id'))
    date = DB.Column(DB.DateTime)
    players = DB.relationship(
        'Player',
        secondary=attendance,
        backref=DB.backref('events', lazy='dynamic')
    )

    def __init__(self, date: str, time: str, league_event_id: int):
        """ League event date constructor. """
        if not date_validator(date):
            raise InvalidField(payload={'details': "League Event Date - date"})
        if not time_validator(time):
            raise InvalidField(payload={'details': "League Event Date - time"})
        if not LeagueEvent.is_league_event(league_event_id):
            raise LeagueEventDoesNotExist(payload={'details': league_event_id})

        self.date = convert_date(date, time)
        self.league_event_id = league_event_id

    def update(
        self,
        date: str = None,
        time: str = None,
        league_event_id: int = None
    ) -> None:
        """ League event date constructor. """
        if league_event_id is not None:
            if not LeagueEvent.is_league_event(league_event_id):
                payload = {'details': league_event_id}
                raise LeagueEventDoesNotExist(payload=payload)
            self.league_event_id = league_event_id

        temp_date, temp_time = split_datetime(self.date)
        if date is not None:
            if not date_validator(date):
                payload = {'details': "League Event Date - date"}
                raise InvalidField(payload=payload)
            temp_date = date

        if time is not None:
            if not time_validator(time):
                payload = {'details': "League Event Date - time"}
                raise InvalidField(payload=payload)
            temp_time = time

        self.date = convert_date(temp_date, temp_time)

    def is_player_signed_up(self, player_id: int) -> bool:
        """Is the given player signed up."""
        for player in self.players:
            if player.id == player_id:
                return True
        return False

    def signup_player(self, player_id: int) -> bool:
        """The player wants to signup for the given event.

        Parameter:
            player_id: the id of the player to add
        Returns:
            True if player was added
            False otherwise
        Raises:
            PlayerDoesNotExist
        """
        valid = False
        player = Player.query.get(player_id)
        if player is None:
            raise PlayerDoesNotExist(payload={'details': player_id})

        if not self.is_player_signed_up(player.id):
            self.players.append(player)
            valid = True
        return valid

    def remove_player(self, player_id: int) -> None:
        """Removes a player from a team.

        Parameter:
            player_id: the id of the player to remove
        Raises:
            MissingPlayer
        """
        player = Player.query.get(player_id)
        if player is None:
            raise PlayerDoesNotExist(payload={'details': player_id})

        if not self.is_player_signed_up(player.id):
            raise PlayerNotOnTeam(payload={'details': player_id})

        self.players.remove(player)

    def json(self) -> dict:
        """Returns a jsonserializable object."""
        date, time = split_datetime(self.date)
        return {
            'league_event_date_id': self.id,
            'league_event_id': self.event.id,
            'date': date,
            'time': time,
            'description': self.event.description,
            'name': self.event.name,
            'active': self.event.active,
            'attendance': len(self.players)
        }


class Fun(DB.Model):
    """
        A class used to store the amount of fun had by all.
        Columns:
            id: the unique id
            year: the year the fun count is for
            count: the total count for the year
    """
    id = DB.Column(DB.Integer, primary_key=True)
    year = DB.Column(DB.Integer)
    count = DB.Column(DB.Integer)

    def __init__(self, year: date = date.today().year, count: int = 0):
        """ Fun constructor. """
        self.year = year
        self.count = count

    def update(self, count=None):
        """Update an existing fun count."""
        if count is not None:
            self.count = count

    def increment(self, change):
        """Increment the fun count.

        Parameters:
            change: the amount the fun count has changed by (int)
        """
        self.count += change

    def json(self):
        """Returns a jsonserializable object."""
        return {'year': self.year, 'count': self.count}


class Espys(DB.Model):
    """
        A class that stores transaction for ESPY points.
        Columns:
            id: the unique id
            description: the description of the transaction (additional notes)
            sponsor_id: the id of sponsor that was involved in the transaction
            points: the amount of points awarded for the transaction ($1=1 pt)
            date: the date of the transaction
            receipt: any information regarding the receipt (receipt number)
    """
    id = DB.Column(DB.Integer, primary_key=True)
    team_id = DB.Column(DB.Integer, DB.ForeignKey('team.id'))
    description = DB.Column(DB.String(120))
    sponsor_id = DB.Column(DB.Integer, DB.ForeignKey('sponsor.id'))
    points = DB.Column(DB.Float)
    date = DB.Column(DB.DateTime)
    receipt = DB.Column(DB.String(30))

    def __init__(self,
                 team_id: int,
                 sponsor_id: int = None,
                 description: str = None,
                 points: float = 0.0,
                 receipt: str = None,
                 time: str = None,
                 date: str = None):
        """The constructor.

            Raises:
                SponsorDoesNotExist
                TeamDoesNotExist
        """
        if not float_validator(points):
            raise InvalidField(payload={"details": "Espys - points"})

        if description is not None and not string_validator(description):
            raise InvalidField(payload={"details": "Espys - description"})

        if receipt is not None and not string_validator(receipt):
            raise InvalidField(payload={"details": "Espys - receipt"})

        if sponsor_id is not None and not Sponsor.does_sponsor_exist(sponsor_id):
            raise SponsorDoesNotExist(payload={"details": sponsor_id})

        if not Team.does_team_exist(team_id):
            raise TeamDoesNotExist(payload={"details": team_id})

        if date is not None and not date_validator(date):
            raise InvalidField(payload={'details': "Game - date"})
        if time is not None and not time_validator(time):
            raise InvalidField(payload={'details': "Game - time"})

        if date is not None and time is not None:
            self.date = convert_date(date, time)
        else:
            self.date = datetime.today()

        self.points = float(points)
        self.receipt = receipt
        self.description = description
        self.team_id = team_id
        self.sponsor_id = sponsor_id
        self.kik = None

    def __add__(self, other) -> 'Espys':
        """Adds two Espys or an int together"""
        if (isinstance(other, Espys)):
            return self.points + other.points
        else:
            return self.points + other

    __radd__ = __add__

    def update(self,
               team_id: int = None,
               sponsor_id: int = None,
               description: str = None,
               points: float = None,
               receipt: str = None,
               date: str = None,
               time: str = None) -> None:
        """Used to update an existing espy transaction.

            Raises:
                TeamDoesNotExist
                SponsorDoesNotExist
        """
        if points is not None:
            if not float_validator(points):
                raise InvalidField(payload={"details": "Espys - points"})
            self.points = points

        if description is not None:
            if not string_validator(description):
                raise InvalidField(payload={"details": "Espys - description"})
            self.description = description

        if team_id is not None:
            if not Team.does_team_exist(team_id):
                raise TeamDoesNotExist(payload={"details": team_id})
            self.team_id = team_id

        if sponsor_id is not None:
            if not Sponsor.does_sponsor_exist(sponsor_id):
                raise SponsorDoesNotExist(payload={"details": sponsor_id})
            self.sponsor_id = sponsor_id

        if receipt is not None:
            if not string_validator(receipt):
                raise InvalidField(payload={"details": "Espys - receipt"})
            self.receipt = receipt

        temp_date, temp_time = split_datetime(self.date)
        if date is not None:
            if not date_validator(date):
                raise InvalidField(payload={'details': "Game - date"})
            temp_date = date
        if time is not None:
            if not time_validator(time):
                raise InvalidField(payload={'details': "Game - time"})
            temp_time = time
        self.date = convert_date(temp_date, temp_time)

    def json(self) -> dict:
        """Returns a jsonserializable object."""
        sponsor = (None if self.sponsor_id is None
                   else str(Sponsor.query.get(self.sponsor_id)))
        team = (None if self.team_id is None
                else str(Team.query.get(self.team_id)))
        date, time = split_datetime(self.date)
        return {
            'espy_id': self.id,
            'team': team,
            'team_id': self.team_id,
            'sponsor': sponsor,
            'sponsor_id': self.sponsor_id,
            'description': self.description,
            'points': self.points,
            'receipt': self.receipt,
            'date': date,
            'time': time
        }


class Player(UserMixin, DB.Model):
    """
    A class that stores a player's information.
        id: the player's unique id
        name: the name of the player
        email: the unique player's email
        gender: the player's gender
        password: the password for the player
        team: the teams the player plays for
        active: a boolean to say whether the player is active
                currently or not (retired or not)
        kik: the kik user name associated with the player
    """
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
                 name: str,
                 email: str,
                 gender: str = None,
                 password: str = "default",
                 active: bool = True):
        """The constructor.

            Raises:
                InvalidField
                NonUniqueEmail
        """
        # check if email is unique
        if not string_validator(email):
            raise InvalidField(payload={'details': "Player - email"})
        email = Player.normalize_email(email)
        if not Player.is_email_unique(email):
            raise NonUniqueEmail(payload={'details': email})

        if not string_validator(name):
            raise InvalidField(payload={"details": "Player - name"})

        if gender is not None and not gender_validator(gender):
            raise InvalidField(payload={'details': "Player - gender"})

        self.name = name
        self.email = email
        self.gender = gender if gender is None else gender.lower()
        self.set_password(password)
        self.active = active

    def set_password(self, password: str) -> None:
        """Update a player's password.

            Parameters:
                password: the player's new password (str)
        """
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check a player's password.

            Parameters:
                password: attempted password (str)
            Returns:
                True passwords match
                False otherwise
        """
        return check_password_hash(self.password, password)

    def __repr__(self) -> str:
        """Return the string representation of the player."""
        return self.name + " email:" + self.email

    def update_kik(self, kik: str) -> None:
        """Update the player's kik profile."""
        self.kik = kik

    def json(self) -> dict:
        """Returns a jsonserializable object."""
        return {"player_id": self.id,
                "player_name": self.name,
                "gender": self.gender,
                "active": self.active}

    def admin_json(self) -> dict:
        """Returns a jsonserializable object."""
        return {"player_id": self.id,
                "player_name": self.name,
                "gender": self.gender,
                "email": self.email,
                "active": self.active}

    def update(self,
               name: str = None,
               email: str = None,
               gender: str = None,
               password: str = None,
               active: bool = None) -> None:
        """Update an existing player

            Parameters:
                name: the name of the player
                email: the unique email of the player
                gender: the gender of the player
                password: the password of the player
            Raises:
                InvalidField
                NonUniqueEmail
        """
        if email is not None:
            # check if email is valid and unique
            if not string_validator(email):
                raise InvalidField(payload="Player - email")
            email = Player.normalize_email(email)
            if not Player.is_email_unique(email):
                raise NonUniqueEmail(payload={'details': email})
            self.email = email

        if gender is not None:
            if not gender_validator(gender):
                raise InvalidField(payload={'details': "Player - gender"})
            self.gender = gender.lower()

        if name is not None:
            if not string_validator(name):
                raise InvalidField(payload={'details': "Player - name"})
            self.name = name

        if active is not None:
            if not boolean_validator(active):
                raise InvalidField(payload={'detail': "Player - active"})
            self.active = active

    def activate(self) -> None:
        """Activate the player."""
        self.active = True

    def deactivate(self) -> None:
        """Deactivate the player (retire them)."""
        self.active = False

    @classmethod
    def does_player_exist(cls, player_id: str) -> bool:
        return Player.query.get(player_id) is not None

    @classmethod
    def normalize_email(cls, email: str) -> str:
        """Return a normalized email."""
        return email.strip().lower()

    @classmethod
    def is_email_unique(cls, email: str) -> bool:
        """Returns whether the email is unique or not."""
        player = Player.query.filter_by(email=email).first()
        return player is None


class OAuth(OAuthConsumerMixin, DB.Model):
    """A model for storing information about oauth"""
    provider_user_id = DB.Column(DB.String(256), unique=True, nullable=False)
    player_id = DB.Column(DB.Integer, DB.ForeignKey(Player.id), nullable=False)
    player = DB.relationship(Player)


class Sponsor(DB.Model):
    """
    A class that stores information about a sponsor.
    Columns:
        id: the sponsor's unique id
        name: the name of the sponsor
        teams: the teams the sponsor is associated with
        description: a description of the sponsor
        link: a link to the sponsor's website or facebook
        active: a boolean telling whether the sponsor
                is currently sponsoring a team
        espys: all the espys transaction associated with the sponsor
    """
    __tablename__ = 'sponsor'
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(120), unique=True)
    teams = DB.relationship('Team', backref='sponsor',
                            lazy='dynamic')
    description = DB.Column(DB.String(200))
    link = DB.Column(DB.String(100))
    active = DB.Column(DB.Boolean)
    espys = DB.relationship('Espys', backref='sponsor', lazy='dynamic')
    nickname = DB.Column(DB.String(100))

    def __init__(self,
                 name: str,
                 link: str = None,
                 description: str = None,
                 active: bool = True,
                 nickname: str = None):
        """The constructor.

           Raises:
               InvalidField
        """
        if not string_validator(name):
            raise InvalidField(payload={'details': "Sponsor - name"})
        if not string_validator(link):
            raise InvalidField(payload={'details': "Sponsor - link"})
        if not string_validator(description):
            raise InvalidField(payload={'details': "Sponsor - description"})

        self.name = name
        self.description = description
        self.link = link
        self.active = active
        self.nickname = nickname if nickname is not None else name

    def __repr__(self) -> str:
        """Returns the string representation of the sponsor."""
        return self.name if self.name is not None else ""

    def json(self) -> dict:
        """Returns a jsonserializable object."""
        return {'sponsor_id': self.id,
                'sponsor_name': self.name,
                'link': self.link,
                'description': self.description,
                'active': self.active}

    def update(self,
               name: str = None,
               link: str = None,
               description: str = None,
               active: bool = None) -> None:
        """Updates an existing sponsor.

           Raises:
               InvalidField
        """
        if name is not None:
            if not string_validator(name):
                raise InvalidField(payload={'details': "Sponsor - name"})
            self.name = name

        if description is not None:
            if not string_validator(description):
                raise InvalidField(payload={'details': "Sponsor - description"})
            self.description = description

        if link is not None:
            if not string_validator(link):
                raise InvalidField(payload={'details': "Sponsor - link"})
            self.link = link

        if active is not None:
            if not boolean_validator(active):
                raise InvalidField(payload={'detail': "Player - active"})
            self.active = active

    def activate(self) -> None:
        """Activate a sponsor (they are back baby)."""
        self.active = True

    def deactivate(self) -> None:
        """Deactivate a sponsor (they are no longer sponsoring). """
        self.active = False

    @classmethod
    def does_sponsor_exist(cls, sponsor_id: str) -> bool:
        return Sponsor.query.get(sponsor_id) is not None


class Team(DB.Model):
    """
    A class that stores information about a team.
    Columns:
        id: the unique team id
        sponsor_id: the sposor id the team is associated with
        home_games: the home games of the team
        away_games: the away games of the team
        players: the players on the team's roster
        bats: the bats of the team
        league_id: the league id the team is part of
        year: the year the team played
        espys: the espy transaction that team has
    """
    id = DB.Column(DB.Integer, primary_key=True)
    color = DB.Column(DB.String(120))
    sponsor_id = DB.Column(DB.Integer, DB.ForeignKey('sponsor.id'))
    home_games = DB.relationship('Game',
                                 backref='home_team',
                                 lazy='dynamic',
                                 foreign_keys='[Game.home_team_id]')
    away_games = DB.relationship('Game',
                                 backref='away_team',
                                 lazy='dynamic',
                                 foreign_keys='[Game.away_team_id]')
    players = DB.relationship('Player',
                              secondary=roster,
                              backref=DB.backref('teams', lazy='dynamic'))
    bats = DB.relationship('Bat',
                           backref='team',
                           lazy='dynamic')
    league_id = DB.Column(DB.Integer, DB.ForeignKey('league.id'))
    year = DB.Column(DB.Integer)
    player_id = DB.Column(DB.Integer, DB.ForeignKey('player.id'))
    espys = DB.relationship('Espys',
                            backref='team',
                            lazy='dynamic')
    espys_total = column_property(select([func.sum(Espys.points)]).where(
        Espys.team_id == id).correlate_except(Espys), deferred=True)
    sponsor_name = column_property(select([Sponsor.nickname]).where(
        Sponsor.id == sponsor_id).correlate_except(Sponsor))

    def __init__(self,
                 color: str = None,
                 sponsor_id: int = None,
                 league_id: int = None,
                 year: int = date.today().year):
        """ The constructor.

        Raises
            InvalidField
            SponsorDoesNotExist
            LeagueDoesNotExist
        """
        if color is not None and not string_validator(color):
            raise InvalidField(payload={'details': "Team - color"})
        if year is not None and not year_validator(year):
            raise InvalidField(payload={'details': "Team - year"})
        if sponsor_id is not None and not Sponsor.does_sponsor_exist(sponsor_id):
            raise SponsorDoesNotExist(payload={'details': sponsor_id})
        if league_id is not None and not League.does_league_exist(league_id):
            raise LeagueDoesNotExist(payload={'details': league_id})

        self.color = color
        self.sponsor_id = sponsor_id
        self.league_id = league_id
        self.year = year
        self.kik = None

    def __repr__(self) -> str:
        """Returns the string representation."""
        name_parts = []
        fallback = f"Team: {self.id}"
        if self.sponsor_name is not None:
            name_parts.append(self.sponsor_name)
        if self.color is not None:
            name_parts.append(self.color)
        return " ".join(name_parts) if len(name_parts) > 0 else fallback

    def json(self, admin: bool = False) -> dict:
        """Returns a jsonserializable object."""
        if admin:
            captain = (None if self.player_id is None
                       else Player.query.get(self.player_id).admin_json())
        else:
            captain = (None if self.player_id is None
                       else Player.query.get(self.player_id).json())
        return {
            'team_id': self.id,
            'team_name': str(self),
            'color': self.color,
            'sponsor_id': self.sponsor_id,
            'league_id': self.league_id,
            'year': self.year,
            'espys': self.espys_total if self.espys_total is not None else 0,
            'captain': captain
        }

    def update(self,
               color: str = None,
               sponsor_id: int = None,
               league_id: int = None,
               year: int = None) -> None:
        """Updates an existing team.

        Raises:
            InvalidField
            SponsorDoesNotExist
            LeagueDoesNotExist
        """
        if color is not None:
            if not string_validator(color):
                raise InvalidField(payload={'details': "Team - color"})
            self.color = color

        if sponsor_id is not None:
            if not Sponsor.does_sponsor_exist(sponsor_id):
                raise SponsorDoesNotExist(payload={'details': sponsor_id})
            self.sponsor_id = sponsor_id

        if league_id is not None:
            if not League.does_league_exist(league_id):
                raise LeagueDoesNotExist(payload={'details': league_id})
            self.league_id = league_id

        if year is not None:
            if not year_validator(year):
                raise InvalidField(payload={'details': "Team - year"})
            self.year = year

    def insert_player(self, player_id: int, captain: bool = False) -> None:
        """Insert a player on to the team.

        Parameter:
            player_id: the id of the player to add
            captain: True if the player is the team's captain
        Returns:
            True if player was added
            False otherwise
        Raises:
            PlayerDoesNotExist
        """
        player = Player.query.get(player_id)
        if player is None:
            raise PlayerDoesNotExist(payload={'details': player_id})

        valid = False
        if not self.is_player_on_team(player):
            self.players.append(player)
            valid = True
        if captain:
            self.player_id = player_id
            valid = True
        return valid

    def remove_player(self, player_id: int) -> None:
        """Removes a player from a team.

        Parameter:
            player_id: the id of the player to remove
        Raises:
            MissingPlayer
        """
        player = Player.query.get(player_id)
        if player is None:
            raise PlayerDoesNotExist(payload={'details': player_id})
        if not self.is_player_on_team(player):
            raise PlayerNotOnTeam(payload={'details': player_id})
        self.players.remove(player)

    def is_player_on_team(self, player: 'Player') -> bool:
        """Returns whether the given player is on the team

        Parameter:
            player: the player model
        Returns:
            True if player on team otherwise False (boolean)
        """
        if player is None:
            return False
        return player.id in [p.id for p in self.players]

    def check_captain(self, player_name: str, password: str) -> str:
        """Checks if the player is the captain of the team.

        Parameters:
            player_name: the name of the player (str)
            password: the password of the player (str)
        Return:
            True of player is the captain
            False otherwise
        """
        player = Player.query.get(self.player_id)
        return (
            player is not None and
            player.name == player_name and
            player.check_password(password)
        )

    def team_stats(self) -> None:
        pass

    @classmethod
    def does_team_exist(cls, team_id: str) -> bool:
        return Team.query.get(team_id) is not None


class Division(DB.Model):
    """
    a class that holds all the information for a division in a league.
    Columns:
        id: the division unique id
        name: the name of the division
        shortname: the short name of the division
        league: the league the division is part of
        games: the games that are part of division
    """
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(120))
    shortname = DB.Column(DB.String(120))
    games = DB.relationship('Game', backref='division', lazy='dynamic')

    def __init__(self, name: str, shortname: str = None):
        """The constructor

        Raises:
            InvalidField
        """
        if not string_validator(name):
            raise InvalidField(payload={'details': "Division - name"})
        if shortname is not None and not string_validator(shortname):
            raise InvalidField(payload={'details': "Division - short name"})
        self.name = name
        self.shortname = shortname

    def update(self, name: str = None, shortname: str = None) -> None:
        """Update an existing division.

        Raises:
            InvalidField
        """
        if name is not None:
            if not string_validator(name):
                raise InvalidField(payload={'details': "Division - name"})
            self.name = name
        if shortname is not None:
            if not string_validator(shortname):
                raise InvalidField(payload={'details': "Division - shortname"})
            self.shortname = shortname

    def get_shortname(self) -> str:
        """Returns the short name of the division"""
        if self.shortname is not None:
            return self.shortname
        return self.name

    def __repr__(self) -> str:
        """Returns the string representation of the League."""
        return self.name

    def json(self) -> dict:
        """Returns a jsonserializable object."""
        return {'division_id': self.id,
                'division_name': self.name,
                'division_shortname': self.shortname}


class League(DB.Model):
    """
    a class that holds all the information for a league.
    Columns:
        id: the league unique id
        name: the name of the league
        games: the games associated with the league
        teams: the teams part of the league
    """
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(120))
    games = DB.relationship('Game', backref='league', lazy='dynamic')
    teams = DB.relationship('Team', backref='league', lazy='dynamic')

    def __init__(self, name: str = None):
        """The constructor.

        Raises:
            InvalidField
        """
        if not string_validator(name):
            raise InvalidField(payload={'details': "League - name"})
        self.name = name

    def __repr__(self) -> str:
        """Returns the string representation of the League."""
        return self.name

    def json(self) -> dict:
        """Returns a jsonserializable object."""
        return {'league_id': self.id,
                'league_name': self.name}

    def update(self, league: str) -> dict:
        """Update an existing league.

        Raises:
            InvalidField
        """
        if not string_validator(league):
            raise InvalidField(payload={'details': "League - name"})
        self.name = league

    @classmethod
    def does_league_exist(cls, league_id: str) -> bool:
        return League.query.get(league_id) is not None


class Bat(DB.Model):
    """
    A class that stores information about a Bat.
    Columns:
        id: the bat id
        game_id: the game that bat took place in
        team_id: the team the bat was for
        player_id: the player who took the bat
        rbi: the number of runs batted in
        inning: the inning the bat took place
        classification: how the bat would be classified (see BATS)
    """
    id = DB.Column(DB.Integer, primary_key=True)
    game_id = DB.Column(DB.Integer, DB.ForeignKey('game.id'))
    team_id = DB.Column(DB.Integer, DB.ForeignKey('team.id'))
    player_id = DB.Column(DB.Integer, DB.ForeignKey('player.id'))
    rbi = DB.Column(DB.Integer)
    inning = DB.Column(DB.Integer)
    classification = DB.Column(DB.String(2))

    def __init__(self,
                 player_id: int,
                 team_id: int,
                 game_id: int,
                 classification: str,
                 inning: int = 1,
                 rbi: int = 0):
        """The constructor.

        Raises:
            PlayerDoesNotExist
            InvalidField
            TeamDoesNotExist
            GameDoesNotExist
        """
        # check for exceptions
        classification = classification.lower().strip()
        player = Player.query.get(player_id)
        if player is None:
            raise PlayerDoesNotExist(payload={'details': player_id})
        if not hit_validator(classification, player.gender):
            raise InvalidField(payload={'details': "Bat - hit"})
        if not rbi_validator(rbi):
            raise InvalidField(payload={'details': "Bat - rbi"})
        if not inning_validator(inning):
            raise InvalidField(payload={'details': "Bat - inning"})
        if Team.query.get(team_id) is None:
            raise TeamDoesNotExist(payload={'details': team_id})
        if Game.query.get(game_id) is None:
            raise GameDoesNotExist(payload={'details': game_id})
        # otherwise good and a valid object
        self.classification = classification
        self.rbi = rbi
        self.player_id = player_id
        self.team_id = team_id
        self.game_id = game_id
        self.inning = inning

    def __repr__(self) -> str:
        """Returns the string representation of the Bat."""
        player = Player.query.get(self.player_id)
        return (player.name + "-" + self.classification + " in " +
                str(self.inning))

    def __add__(self, other: 'Bat') -> 'Bat':
        """Adds two Bat or an int together"""
        if (isinstance(other, Bat)):
            return self.rbi + other.rbi
        else:
            return self.rbi + other

    __radd__ = __add__

    def json(self) -> dict:
        """Returns a jsonserializable object."""
        return {
            'bat_id': self.id,
            'game_id': self.game_id,
            'team_id': self.team_id,
            'team': str(Player.query.get(self.team_id)),
            'rbi': self.rbi,
            'hit': self.classification,
            'inning': self.inning,
            'player_id': self.player_id,
            'player': str(Player.query.get(self.player_id))
        }

    def update(self,
               player_id: int = None,
               team_id: int = None,
               game_id: int = None,
               rbi: int = None,
               hit: int = None,
               inning: int = None) -> None:
        """Update an existing bat.

        Raises:
            TeamDoesNotExist
            GameDoesNotExist
            PlayerDoesNotExist
            InvalidField
        """
        if team_id is not None and Team.query.get(team_id) is not None:
            self.team_id = team_id
        elif team_id is not None:
            raise TeamDoesNotExist(payload={'details': team_id})
        if game_id is not None and Game.query.get(game_id) is not None:
            self.game_id = game_id
        elif game_id is not None:
            raise GameDoesNotExist(payload={'details': game_id})
        if player_id is not None and Player.query.get(player_id) is not None:
            self.player_id = player_id
        elif player_id is not None:
            raise PlayerDoesNotExist(payload={'details': player_id})
        if rbi is not None and rbi_validator(rbi):
            self.rbi = rbi
        elif rbi is not None:
            raise InvalidField(payload={'details': "Bat - rbi"})
        if hit is not None and hit_validator(hit):
            self.classification = hit
        elif hit is not None:
            raise InvalidField(payload={'details': "Bat - hit"})
        if inning is not None and inning_validator(inning):
            self.inning = inning
        elif inning is not None:
            raise InvalidField(payload={'details': "Bat - inning"})


class Game(DB.Model):
    """
    A class that holds information about a Game.
    Columns:
        id: the game id
        home_team_id: the home team's id
        away_team_id: the away team's id
        league_id: the league id the game is part of
        date: the date of the game
        status: the status of the game
        field: the field the game is to be played on
    """
    id = DB.Column(DB.Integer, primary_key=True)
    home_team_id = DB.Column(DB.Integer,
                             DB.ForeignKey('team.id',
                                           use_alter=True,
                                           name='fk_home_team_game'))
    away_team_id = DB.Column(DB.Integer,
                             DB.ForeignKey('team.id',
                                           use_alter=True,
                                           name='fk_away_team_game'))
    league_id = DB.Column(DB.Integer, DB.ForeignKey('league.id'))
    division_id = DB.Column(DB.Integer, DB.ForeignKey('division.id'))
    bats = DB.relationship("Bat", backref="game", lazy='dynamic')
    date = DB.Column(DB.DateTime)
    status = DB.Column(DB.String(120))
    field = DB.Column(DB.String(120))
    away_team_score = column_property(select([func.sum(Bat.rbi)])
                                      .where(and_(
                                          (Bat.game_id == id),
                                          (Bat.team_id == away_team_id)))
                                      .correlate_except(Bat),
                                      deferred=True,
                                      group='summary')
    home_team_score = column_property(select([func.sum(Bat.rbi)])
                                      .where(and_(
                                          (Bat.game_id == id),
                                          (Bat.team_id == home_team_id)))
                                      .correlate_except(Bat),
                                      deferred=True,
                                      group='summary')
    hit_clause = or_((Bat.classification == 's'),
                     (Bat.classification == 'ss'),
                     (Bat.classification == 'd'),
                     (Bat.classification == 'hr'))
    home_team_hits = column_property(select([func.count(Bat.id)])
                                     .where(and_(
                                         (Bat.game_id == id),
                                         (Bat.team_id == home_team_id),
                                         hit_clause))
                                     .correlate_except(Bat),
                                     deferred=True,
                                     group='summary')
    away_team_hits = column_property(select([func.count(Bat.id)])
                                     .where(and_(
                                         (Bat.game_id == id),
                                         (Bat.team_id == away_team_id),
                                         hit_clause))
                                     .correlate_except(Bat),
                                     deferred=True,
                                     group='summary')

    def __init__(self,
                 date: str,
                 time: str,
                 home_team_id: int,
                 away_team_id: int,
                 league_id: int,
                 division_id: int,
                 status: str = "",
                 field: str = ""):
        """The Constructor.

        Raises:
            InvalidField
            TeamDoesNotExist
            LeagueDoesNotExist
            DivisionDoesNotExist
        """
        # check for all the invalid parameters
        if not date_validator(date):
            raise InvalidField(payload={'details': "Game - date"})
        if not time_validator(time):
            raise InvalidField(payload={'details': "Game - time"})

        if (home_team_id is None or Team.query.get(home_team_id) is None):
            raise TeamDoesNotExist(payload={'details': home_team_id})
        if (away_team_id is None or Team.query.get(away_team_id) is None):
            raise TeamDoesNotExist(payload={'details': away_team_id})
        if League.query.get(league_id) is None:
            raise LeagueDoesNotExist(payload={'details': league_id})
        if ((status != "" and not string_validator(status)) or
                (field != "" and not field_validator(field))):
            raise InvalidField(payload={'details': "Game - field/status"})
        if Division.query.get(division_id) is None:
            raise DivisionDoesNotExist(payload={'details': division_id})

        # must be good now
        self.date = convert_date(date, time)
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.league_id = league_id
        self.status = status
        self.field = field
        self.division_id = division_id

    def __repr__(self) -> str:
        """Returns the string representation of the Game."""
        home = str(Team.query.get(self.home_team_id))
        away = str(Team.query.get(self.away_team_id))
        result = (home + " vs " + away + " on " +
                  self.date.strftime("%Y-%m-%d %H:%M"))
        if self.field != "":
            result += " at " + self.field
        return result

    def json(self) -> dict:
        """Returns a jsonserializable object."""
        return {
            'game_id': self.id,
            'home_team_id': self.home_team_id,
            'home_team': str(Team.query.get(self.home_team_id)),
            'away_team_id': self.away_team_id,
            'away_team': str(Team.query.get(self.away_team_id)),
            'league_id': self.league_id,
            'division_id': self.division_id,
            'date': self.date.strftime("%Y-%m-%d"),
            'time': self.date.strftime("%H:%M"),
            'status': self.status,
            'field': self.field}

    def update(self,
               date: str = None,
               time: str = None,
               home_team_id: int = None,
               away_team_id: int = None,
               league_id: int = None,
               status: str = None,
               field: str = None,
               division_id: int = None) -> None:
        """Update an existing game.

        Raises:
            InvalidField
            TeamDoesNotExist
            LeagueDoesNotExist
        """
        d = self.date.strftime("%Y-%m-%d")
        t = self.date.strftime("%H:%M")
        if date is not None and date_validator(date):
            d = date
        elif date is not None:
            raise InvalidField(payload={'details': "Game - date"})
        if time is not None and time_validator(time):
            t = time
        elif time is not None:
            raise InvalidField(payload={'details': "Game - time"})
        if (home_team_id is not None and
                Team.query.get(home_team_id) is not None):
            self.home_team_id = home_team_id
        elif home_team_id is not None:
            raise TeamDoesNotExist(payload={'details': home_team_id})
        if (away_team_id is not None and
                Team.query.get(away_team_id) is not None):
            self.away_team_id = away_team_id
        elif away_team_id is not None:
            raise TeamDoesNotExist(payload={'details': away_team_id})
        if league_id is not None and League.query.get(league_id) is not None:
            self.league_id = league_id
        elif league_id is not None:
            raise LeagueDoesNotExist(payload={'details': league_id})
        if status is not None and string_validator(status):
            self.status = status
        elif status is not None:
            raise InvalidField(payload={'details': "Game - status"})
        if field is not None and field_validator(field):
            self.field = field
        elif field is not None:
            raise InvalidField(payload={'details': "Game - field"})
        if (division_id is not None and
                Division.query.get(division_id) is not None):
            self.division_id = division_id
        elif division_id is not None:
            raise DivisionDoesNotExist(payload={'details': "division_id"})
        # worse case just overwrites it with same date or time
        self.date = datetime.strptime(d + "-" + t, '%Y-%m-%d-%H:%M')

    def summary(self) -> dict:
        """Returns a game summary."""
        return {
            'away_score': self.away_team_score
            if self.away_team_score is not None else 0,
            'away_bats': self.away_team_hits
            if self.away_team_hits is not None else 0,
            'home_score': self.home_team_score
            if self.home_team_score is not None else 0,
            'home_bats': self.home_team_hits
            if self.home_team_hits is not None else 0
        }

    @classmethod
    def does_game_exist(cls, game_id: str) -> bool:
        return Game.query.get(game_id) is not None


class JoinLeagueRequest(DB.Model):
    """
        A class used to store requests to join a league.
        Columns:
            team_id: the team they want to join
            name: the name they want to use
            email: the email from the Oauth provider
            pending: whether waiting for the outcome of the request
    """
    id = DB.Column(DB.Integer, primary_key=True)
    team_id = DB.Column(DB.Integer, DB.ForeignKey(Team.id), nullable=False)
    team = DB.relationship(Team)
    email = DB.Column(DB.String(120), nullable=False)
    name = DB.Column(DB.String(120), nullable=False)
    pending = DB.Column(DB.Boolean)
    gender = DB.Column(DB.String(1))

    def __init__(self, email: str, name: str, team: 'Team', gender: str):
        if team is None or not isinstance(team, Team) or team.id is None:
            raise TeamDoesNotExist("Given team does not exist")
        if not gender_validator(gender):
            raise InvalidField(payload={
                'details': "Player League Request - gender"})
        if not string_validator(email):
            raise InvalidField(payload="Player League Request - email")
        if not string_validator(name):
            raise InvalidField(payload="Player League Request - name")
        self.email = email.lower()
        self.name = name
        self.team_id = team.id
        self.pending = True
        self.gender = gender.lower()

    def accept_request(self) -> 'Player':
        """Accept the request and add the player to the team"""
        # create a player if they do not exit already
        if not self.pending:
            raise HaveLeagueRequestException("Request already submitted")
        player = Player.query.filter(
            func.lower(Player.email) == self.email.lower()).first()
        if player is None:
            player = Player(self.name, self.email, gender=self.gender)
            DB.session.add(player)
            DB.session.commit()
        self.pending = False
        team = Team.query.get(self.team_id)
        team.insert_player(player.id)
        DB.session.commit()
        return player

    def decline_request(self) -> None:
        """Decline the request."""
        self.pending = False
        DB.session.commit()

    def json(self) -> dict:
        """Get a json version of the model"""
        team = (None if self.team_id is None
                else Team.query.get(self.team_id).json())
        return {
            "team": team,
            "email": self.email,
            "id": self.id,
            "pending": self.pending,
            "player_name": self.name,
            "gender": self.gender
        }
