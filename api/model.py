from datetime import date, datetime
from sqlalchemy.orm import column_property
from sqlalchemy import and_, select, func, or_, desc, asc, not_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from api.extensions import DB
from api.errors import TeamDoesNotExist, PlayerDoesNotExist, GameDoesNotExist, \
    InvalidField, LeagueDoesNotExist, SponsorDoesNotExist, \
    NonUniqueEmail, PlayerNotOnTeam, DivisionDoesNotExist, \
    HaveLeagueRequestException, LeagueEventDoesNotExist
from api.helper import normalize_string
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


def validate(field, validator, exception, required=True):
    """Helper function for validating a given field."""
    if (required or field is not None) and not validator(field):
        raise exception


def notNone(value, default):
    """Returns the value if it is not None otherwise the default."""
    return value if value is not None else default


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
        validate(
            name,
            string_validator,
            InvalidField(payload={"details": "League event - name"})
        )
        validate(
            active,
            boolean_validator,
            InvalidField(payload={"details": "League event - active"})
        )
        validate(
            description,
            string_validator,
            InvalidField(payload={"details": "League event - description"})
        )
        self.__update(name=name, description=description, active=active)

    def __update(self, name: str, description: str, active: bool):
        self.name = notNone(name, self.name)
        self.description = notNone(description, self.description)
        self.active = notNone(active, self.active)

    def update(self, name=None, description=None, active=None) -> None:
        """Update a league event.

            Parameters:
                name: the league event new name (optional str)
                description: the league event new description (optional str)
                active: is the event active or not (optional str)
        """
        validate(
            name,
            string_validator,
            InvalidField(payload={"details": "League event - name"}),
            required=False
        )
        validate(
            active,
            boolean_validator,
            InvalidField(payload={"details": "League event - name"}),
            required=False

        )
        validate(
            description,
            string_validator,
            InvalidField(payload={"details": "League event - active"}),
            required=False
        )
        self.__update(name=name, description=description, active=active)

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
        validate(
            date,
            date_validator,
            InvalidField(payload={'details': "League Event Date - date"})
        )
        validate(
            time,
            time_validator,
            InvalidField(payload={'details': "League Event Date - time"})
        )
        validate(
            league_event_id,
            lambda id: LeagueEvent.is_league_event(id),
            LeagueEventDoesNotExist(payload={'details': league_event_id})
        )
        self.__update(date, time, league_event_id)

    def __update(self, date: str, time: str, league_event_id: int):
        self.date = convert_date(date, time)
        self.league_event_id = notNone(league_event_id, self.league_event_id)

    def update(
        self,
        date: str = None,
        time: str = None,
        league_event_id: int = None
    ) -> None:
        """ League event date constructor. """
        validate(
            date,
            date_validator,
            InvalidField(payload={'details': "League Event Date - date"}),
            required=False
        )
        validate(
            time,
            time_validator,
            InvalidField(payload={'details': "League Event Date - time"}),
            required=False
        )
        validate(
            league_event_id,
            lambda id: LeagueEvent.is_league_event(id),
            LeagueEventDoesNotExist(payload={'details': league_event_id}),
            required=False
        )

        (current_date, current_time) = split_datetime(self.date)
        self.__update(
            notNone(date, current_date),
            notNone(time, current_time),
            league_event_id
        )

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
        player = Player.query.get(player_id)
        if player is None:
            raise PlayerDoesNotExist(payload={'details': player_id})

        if not self.is_player_signed_up(player.id):
            self.players.append(player)
            return True
        return False

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

    def __init__(
        self,
        team_id: int,
        sponsor_id: int = None,
        description: str = None,
        points: float = 0.0,
        receipt: str = None,
        time: str = None,
        date: str = None
    ):
        """The constructor.

            Raises:
                SponsorDoesNotExist
                TeamDoesNotExist
        """
        validate(
            points,
            float_validator,
            InvalidField(payload={"details": "Espys - points"})
        )
        validate(
            team_id,
            lambda id: Team.does_team_exist(id),
            TeamDoesNotExist(payload={"details": team_id})
        )
        validate(
            description,
            string_validator,
            InvalidField(payload={"details": "Espys - description"}),
            required=False
        )
        validate(
            receipt,
            string_validator,
            InvalidField(payload={"details": "Espys - receipt"}),
            required=False
        )
        validate(
            sponsor_id,
            lambda id: Sponsor.does_sponsor_exist(id),
            SponsorDoesNotExist(payload={"details": sponsor_id}),
            required=False
        )
        validate(
            date,
            date_validator,
            InvalidField(payload={'details': "Game - date"}),
            required=False
        )
        validate(
            time,
            time_validator,
            InvalidField(payload={'details': "Game - time"}),
            required=False
        )

        (current_date, current_time) = split_datetime(datetime.today())
        self.__update(
            team_id=team_id,
            sponsor_id=sponsor_id,
            description=description,
            points=float(points),
            receipt=receipt,
            time=notNone(time, current_time),
            date=notNone(date, current_date)
        )

    def __update(
        self,
        team_id: int,
        sponsor_id: int,
        description: str,
        points: float,
        receipt: str,
        time: str,
        date: str
    ):
        self.points = notNone(points, self.points)
        self.receipt = notNone(receipt, self.receipt)
        self.description = notNone(description, self.description)
        self.team_id = notNone(team_id, self.team_id)
        self.sponsor_id = notNone(sponsor_id, self.sponsor_id)
        self.date = convert_date(date, time)

    def __add__(self, other) -> 'Espys':
        """Adds two Espys or an int together"""
        if (isinstance(other, Espys)):
            return self.points + other.points
        else:
            return self.points + other

    __radd__ = __add__

    def update(
        self,
        team_id: int = None,
        sponsor_id: int = None,
        description: str = None,
        points: float = None,
        receipt: str = None,
        date: str = None,
        time: str = None
    ) -> None:
        """Used to update an existing espy transaction.

            Raises:
                TeamDoesNotExist
                SponsorDoesNotExist
        """
        validate(
            points,
            float_validator,
            InvalidField(payload={"details": "Espys - points"}),
            required=False
        )
        validate(
            team_id,
            lambda id: Team.does_team_exist(id),
            TeamDoesNotExist(payload={"details": team_id}),
            required=False
        )
        validate(
            description,
            string_validator,
            InvalidField(payload={"details": "Espys - description"}),
            required=False
        )
        validate(
            receipt,
            string_validator,
            InvalidField(payload={"details": "Espys - receipt"}),
            required=False
        )
        validate(
            sponsor_id,
            lambda id: Sponsor.does_sponsor_exist(id),
            SponsorDoesNotExist(payload={"details": sponsor_id}),
            required=False
        )
        validate(
            date,
            date_validator,
            InvalidField(payload={'details': "Game - date"}),
            required=False
        )
        validate(
            time,
            time_validator,
            InvalidField(payload={'details': "Game - time"}),
            required=False
        )

        (current_date, current_time) = split_datetime(self.date)
        self.__update(
            team_id=team_id,
            sponsor_id=sponsor_id,
            description=description,
            points=float(notNone(points, self.points)),
            receipt=receipt,
            time=notNone(time, current_time),
            date=notNone(date, current_date)
        )

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
                 gender: str = "m",
                 password: str = "default",
                 active: bool = True):
        """The constructor.

            Raises:
                InvalidField
                NonUniqueEmail
        """
        validate(
            email,
            string_validator,
            InvalidField(payload={'details': "Player - email"})
        )
        validate(
            Player.normalize_email(email),
            lambda email: Player.is_email_unique(email),
            NonUniqueEmail(payload={'details': email})
        )
        validate(
            name,
            string_validator,
            InvalidField(payload={"details": "Player - name"})
        )
        validate(
            gender,
            gender_validator,
            InvalidField(payload={'details': "Player - gender"})
        )

        self.__update(
            name=name,
            email=email,
            gender=gender,
            password=password,
            active=active
        )

    def __update(
        self,
        name: str,
        email: str,
        gender: str,
        password: str,
        active: bool
    ):
        self.name = notNone(name, self.name)
        self.email = Player.normalize_email(notNone(email, self.email))
        self.gender = Player.normalize_gender(notNone(gender, self.gender))
        self.set_password(notNone(password, self.password))
        self.active = notNone(active, self.active)

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
        validate(
            email,
            string_validator,
            InvalidField(payload={'details': "Player - email"}),
            required=False
        )
        validate(
            None if email is None else Player.normalize_email(email),
            lambda email: Player.is_email_unique(email),
            NonUniqueEmail(payload={'details': email}),
            required=False
        )
        validate(
            name,
            string_validator,
            InvalidField(payload={"details": "Player - name"}),
            required=False
        )
        validate(
            gender,
            gender_validator,
            InvalidField(payload={'details': "Player - gender"}),
            required=False
        )

        self.__update(
            name=name,
            email=email,
            gender=gender,
            password=password,
            active=active
        )

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
        return self.name

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

    def activate(self) -> None:
        """Activate the player."""
        self.active = True

    def deactivate(self) -> None:
        """Deactivate the player (retire them)."""
        self.active = False

    @classmethod
    def get_teams_captained(cls, player_id: str) -> list['Team']:
        return Team.query.filter(Team.player_id == player_id).all()

    @classmethod
    def does_player_exist(cls, player_id: str) -> bool:
        return Player.query.get(player_id) is not None

    @classmethod
    def normalize_email(cls, email: str) -> str:
        """Return a normalized email."""
        return normalize_string(email)

    @classmethod
    def normalize_gender(cls, gender: str) -> str:
        """Return a normalized email."""
        return normalize_string(gender)

    @classmethod
    def find_by_email(cls, email: str) -> "Player":
        """Returns the player with the given email."""
        if email is None:
            return None
        return Player.query.filter(
            func.lower(Player.email) == Player.normalize_email(email)
        ).first()
    
    @classmethod
    def search_player(cls, search_phrase: str) -> list["Player"]:
        """Returns all players who meet the search phrase"""
        return Player.query.filter(
            or_(
                func.lower(Player.email).contains(search_phrase.lower()),
                func.lower(Player.name).contains(search_phrase.lower())
            )
        ).all()

    @classmethod
    def is_email_unique(cls, email: str) -> bool:
        """Returns whether the email is unique and available."""
        return Player.find_by_email(email) is None


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

    def __init__(
        self,
        name: str,
        link: str = None,
        description: str = None,
        active: bool = True,
        nickname: str = None
    ):
        """The constructor.

           Raises:
               InvalidField
        """
        validate(
            name,
            string_validator,
            InvalidField(payload={'details': "Sponsor - name"})
        )
        validate(
            nickname,
            string_validator,
            InvalidField(payload={'details': "Sponsor - nickname"}),
            required=False
        )
        validate(
            link,
            string_validator,
            InvalidField(payload={'details': "Sponsor - link"})
        )
        validate(
            description,
            string_validator,
            InvalidField(payload={'details': "Sponsor - description"})
        )
        validate(
            active,
            boolean_validator,
            InvalidField(payload={'details': "Sponsor - active"})
        )
        self.__update(
            name=name,
            description=description,
            link=link,
            active=active,
            nickname=nickname if nickname is not None else name
        )

    def __update(
        self,
        name: str,
        link: str,
        description: str,
        active: bool,
        nickname: str
    ):
        self.name = notNone(name, self.name)
        self.description = notNone(description, self.description)
        self.link = notNone(link, self.link)
        self.active = notNone(active, self.active)
        self.nickname = notNone(nickname, self.nickname)

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
               active: bool = None,
               nickname: str = None) -> None:
        """Updates an existing sponsor.

           Raises:
               InvalidField
        """
        validate(
            name,
            string_validator,
            InvalidField(payload={'details': "Sponsor - name"}),
            required=False
        )
        validate(
            nickname,
            string_validator,
            InvalidField(payload={'details': "Sponsor - nickname"}),
            required=False
        )
        validate(
            link,
            string_validator,
            InvalidField(payload={'details': "Sponsor - link"}),
            required=False
        )
        validate(
            description,
            string_validator,
            InvalidField(payload={'details': "Sponsor - description"}),
            required=False
        )
        validate(
            active,
            boolean_validator,
            InvalidField(payload={'details': "Sponsor - active"}),
            required=False
        )
        has_nickname = self.name != self.nickname
        self.__update(
            name=name,
            description=description,
            link=link,
            active=active,
            nickname=nickname if nickname is not None else (
                name if not has_nickname else self.nickname
            )
        )

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
        validate(
            color,
            string_validator,
            InvalidField(payload={'details': "Team - color"}),
            required=False
        )
        validate(
            year,
            year_validator,
            InvalidField(payload={'details': "Team - year"}),
        )
        validate(
            sponsor_id,
            lambda id: Sponsor.does_sponsor_exist(id),
            SponsorDoesNotExist(payload={'details': sponsor_id}),
            required=False
        )
        validate(
            league_id,
            lambda id: League.does_league_exist(id),
            LeagueDoesNotExist(payload={'details': league_id}),
            required=False
        )
        self.__update(
            color=color,
            sponsor_id=sponsor_id,
            league_id=league_id,
            year=year
        )

    def __update(
        self,
        color: str,
        sponsor_id: int,
        league_id: int,
        year: int
    ):
        self.color = notNone(color, self.color)
        self.sponsor_id = notNone(sponsor_id, self.sponsor_id)
        self.league_id = notNone(league_id, self.league_id)
        self.year = notNone(year, self.year)
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
        validate(
            color,
            string_validator,
            InvalidField(payload={'details': "Team - color"}),
            required=False
        )
        validate(
            year,
            year_validator,
            InvalidField(payload={'details': "Team - year"}),
            required=False
        )
        validate(
            sponsor_id,
            lambda id: Sponsor.does_sponsor_exist(id),
            SponsorDoesNotExist(payload={'details': sponsor_id}),
            required=False
        )
        validate(
            league_id,
            lambda id: League.does_league_exist(id),
            LeagueDoesNotExist(payload={'details': league_id}),
            required=False
        )
        self.__update(
            color=color,
            sponsor_id=sponsor_id,
            league_id=league_id,
            year=year
        )

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

        on_team = self.is_player_on_team(player)
        if not on_team:
            self.players.append(player)
        if captain:
            self.player_id = player_id
        return captain or not on_team

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
        validate(
            name,
            string_validator,
            InvalidField(payload={'details': "Division - name"})
        )
        validate(
            shortname,
            string_validator,
            InvalidField(payload={'details': "Division - shortname"}),
            required=False
        )
        self.__update(name=name, shortname=shortname)

    def __update(self, name: str, shortname: str):
        self.name = notNone(name, self.name)
        self.shortname = notNone(shortname, self.shortname)

    def update(self, name: str = None, shortname: str = None) -> None:
        """Update an existing division.

        Raises:
            InvalidField
        """
        validate(
            name,
            string_validator,
            InvalidField(payload={'details': "Division - name"}),
            required=False
        )
        validate(
            shortname,
            string_validator,
            InvalidField(payload={'details': "Division - shortname"}),
            required=False
        )
        self.__update(name=name, shortname=shortname)

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
        return {
            'division_id': self.id,
            'division_name': self.name,
            'division_shortname': self.shortname
        }

    @classmethod
    def does_division_exist(cls, division_id: str) -> bool:
        return Division.query.get(division_id) is not None


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
        validate(
            name,
            string_validator,
            InvalidField(payload={'details': "League - name"})
        )
        self.__update(name)

    def __update(self, name: str):
        self.name = notNone(name, self.name)

    def update(self, league: str) -> dict:
        """Update an existing league.

        Raises:
            InvalidField
        """
        validate(
            league,
            string_validator,
            InvalidField(payload={'details': "League - name"})
        )
        self.__update(league)

    def __repr__(self) -> str:
        """Returns the string representation of the League."""
        return self.name

    def json(self) -> dict:
        """Returns a jsonserializable object."""
        return {
            'league_id': self.id,
            'league_name': self.name
        }

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

    def __init__(
        self,
        player_id: int,
        team_id: int,
        game_id: int,
        classification: str,
        inning: int = 1,
        rbi: int = 0
    ):
        """The constructor.

        Raises:
            PlayerDoesNotExist
            InvalidField
            TeamDoesNotExist
            GameDoesNotExist
        """
        validate(
            team_id,
            lambda id: Team.does_team_exist(id),
            TeamDoesNotExist(payload={'details': team_id}),
        )
        validate(
            game_id,
            lambda id: Game.does_game_exist(id),
            GameDoesNotExist(payload={'details': game_id}),
        )
        validate(
            player_id,
            lambda id: Player.does_player_exist(id),
            PlayerDoesNotExist(payload={'details': player_id}),
        )
        player = Player.query.get(player_id)
        validate(
            rbi,
            rbi_validator,
            InvalidField(payload={'details': "Bat - rbi"}),
        )
        validate(
            classification,
            lambda cls: hit_validator(cls, player.gender),
            InvalidField(payload={'details': "Bat - hit"}),
        )
        validate(
            inning,
            inning_validator,
            InvalidField(payload={'details': "Bat - inning"}),
        )
        self.__update(
            player_id=player_id,
            team_id=team_id,
            game_id=game_id,
            rbi=rbi,
            inning=inning,
            classification=classification
        )

    def __update(
        self,
        player_id: int,
        team_id: int,
        game_id: int,
        classification: str,
        inning: int,
        rbi: int
    ):
        self.rbi = notNone(rbi, self.rbi)
        self.player_id = notNone(player_id, self.player_id)
        self.team_id = notNone(team_id, self.team_id)
        self.game_id = notNone(game_id, self.game_id)
        self.inning = notNone(inning, self.inning)
        self.classification = Bat.normalize_classification(
            notNone(classification, self.classification)
        )

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
            'team': str(Team.query.get(self.team_id)),
            'rbi': self.rbi,
            'hit': self.classification,
            'inning': self.inning,
            'player_id': self.player_id,
            'player': str(Player.query.get(self.player_id))
        }

    @classmethod
    def does_bat_exist(cls, bat_id: str) -> bool:
        return Bat.query.get(bat_id) is not None

    @classmethod
    def normalize_classification(cls, classification: str) -> str:
        return normalize_string(classification)

    def update(
        self,
        player_id: int = None,
        team_id: int = None,
        game_id: int = None,
        rbi: int = None,
        hit: int = None,
        inning: int = None
    ) -> None:
        """Update an existing bat.

        Raises:
            TeamDoesNotExist
            GameDoesNotExist
            PlayerDoesNotExist
            InvalidField
        """
        validate(
            team_id,
            lambda id: Team.does_team_exist(id),
            TeamDoesNotExist(payload={'details': team_id}),
            required=False
        )
        validate(
            game_id,
            lambda id: Game.does_game_exist(id),
            GameDoesNotExist(payload={'details': game_id}),
            required=False
        )
        validate(
            player_id,
            lambda id: Player.does_player_exist(id),
            PlayerDoesNotExist(payload={'details': player_id}),
            required=False
        )
        validate(
            rbi,
            rbi_validator,
            InvalidField(payload={'details': "Bat - rbi"}),
            required=False
        )
        validate(
            inning,
            inning_validator,
            InvalidField(payload={'details': "Bat - inning"}),
            required=False
        )
        player = Player.query.get(
            player_id
            if player_id is not None else self.player_id
        )
        validate(
            hit,
            lambda cls: hit_validator(cls, player.gender),
            InvalidField(payload={'details': "Bat - hit"}),
            required=False
        )
        self.__update(
            player_id=player_id,
            team_id=team_id,
            game_id=game_id,
            rbi=rbi,
            inning=inning,
            classification=notNone(hit, self.classification)
        )


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

    def __init__(
        self,
        date: str,
        time: str,
        home_team_id: int,
        away_team_id: int,
        league_id: int,
        division_id: int,
        status: str = "",
        field: str = ""
    ):
        """The Constructor.

        Raises:
            InvalidField
            TeamDoesNotExist
            LeagueDoesNotExist
            DivisionDoesNotExist
        """
        validate(
            date,
            date_validator,
            InvalidField(payload={'details': "Game - date"})
        )
        validate(
            time,
            time_validator,
            InvalidField(payload={'details': "Game - time"})
        )
        validate(
            home_team_id,
            lambda id: Team.does_team_exist(id),
            TeamDoesNotExist(payload={'details': home_team_id}),
            required=False
        )
        validate(
            away_team_id,
            lambda id: Team.does_team_exist(id),
            TeamDoesNotExist(payload={'details': away_team_id}),
            required=False
        )
        validate(
            league_id,
            lambda id: League.does_league_exist(id),
            LeagueDoesNotExist(payload={'details': league_id}),
        )
        validate(
            division_id,
            lambda id: Division.does_division_exist(id),
            DivisionDoesNotExist(payload={'details': division_id}),
        )
        validate(
            status if status != '' else None,
            string_validator,
            InvalidField(payload={'details': "Game - status"}),
            required=False
        )
        validate(
            field if field != '' else None,
            field_validator,
            InvalidField(payload={'details': "Game - field"}),
            required=False
        )
        self.__update(
            date=date,
            time=time,
            home_team_id=home_team_id,
            away_team_id=away_team_id,
            league_id=league_id,
            division_id=division_id,
            status=status,
            field=field
        )

    def __update(
        self,
        date: str,
        time: str,
        home_team_id: int,
        away_team_id: int,
        league_id: int,
        division_id: int,
        status: str,
        field: str
    ):
        self.date = convert_date(date, time)
        self.home_team_id = notNone(home_team_id, self.home_team_id)
        self.away_team_id = notNone(away_team_id, self.away_team_id)
        self.league_id = notNone(league_id, self.league_id)
        self.status = notNone(status, self.status)
        self.field = notNone(field, self.field)
        self.division_id = notNone(division_id, self.division_id)

    def update(
        self,
        date: str = None,
        time: str = None,
        home_team_id: int = None,
        away_team_id: int = None,
        league_id: int = None,
        status: str = None,
        field: str = None,
        division_id: int = None
    ) -> None:
        """Update an existing game.

        Raises:
            InvalidField
            TeamDoesNotExist
            LeagueDoesNotExist
        """
        validate(
            date,
            date_validator,
            InvalidField(payload={'details': "Game - date"}),
            required=False
        )
        validate(
            time,
            time_validator,
            InvalidField(payload={'details': "Game - time"}),
            required=False
        )
        validate(
            home_team_id,
            lambda id: Team.does_team_exist(id),
            TeamDoesNotExist(payload={'details': home_team_id}),
            required=False
        )
        validate(
            away_team_id,
            lambda id: Team.does_team_exist(id),
            TeamDoesNotExist(payload={'details': away_team_id}),
            required=False
        )
        validate(
            league_id,
            lambda id: League.does_league_exist(id),
            LeagueDoesNotExist(payload={'details': league_id}),
            required=False
        )
        validate(
            division_id,
            lambda id: Division.does_division_exist(id),
            DivisionDoesNotExist(payload={'details': division_id}),
            required=False
        )
        validate(
            status,
            string_validator,
            InvalidField(payload={'details': "Game - status"}),
            required=False
        )
        validate(
            field,
            field_validator,
            InvalidField(payload={'details': "Game - field"}),
            required=False
        )
        (current_date, current_time) = split_datetime(self.date)
        self.__update(
            date=notNone(date, current_date),
            time=notNone(time, current_time),
            home_team_id=home_team_id,
            away_team_id=away_team_id,
            league_id=league_id,
            division_id=division_id,
            status=status,
            field=field
        )

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
            'field': self.field
        }

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

    def get_team_bats(self, team_id: int):
        """Remove score for the given team from the game."""
        print(self.bats)
        return [bat for bat in self.bats if bat.team_id == team_id]

    @classmethod
    def does_game_exist(cls, game_id: str) -> bool:
        return Game.query.get(game_id) is not None

    @classmethod
    def normalize_field(cls, field: str) -> str:
        """Normalized the field """
        return normalize_string(field)

    @classmethod
    def games_with_scores(
            cls,
            teams: list[Team],
            year: int = datetime.today().year
    ) -> list['Game']:
        """Return games that have a score for the given year & list of teams

        If given a empty list of teams will get all games for all
        teams in the given year
        """
        team_ids = [team.id for team in teams] if len(teams) > 0 else [
            team.id for team in Team.query.filter(Team.year == year).all()
        ]
        games = Game.query.filter(
            or_(
                Game.away_team_id.in_(team_ids),
                Game.home_team_id.in_(team_ids),
            )
        ).filter(
            Game.bats.any(Bat.team_id.in_(team_ids))
        ).order_by(desc(Game.date)).all()
        return games

    @classmethod
    def games_needing_scores(
            cls,
            teams: list[Team],
            year: int = datetime.today().year
    ) -> list['Game']:
        """Return games that are elible for a score submission without one

        If given a empty list of teams will get all games for all
        teams in the given year
        """
        today = datetime.today()
        end_of_today = datetime(
            today.year, today.month, today.day, hour=23, minute=59
        )
        team_ids = [team.id for team in teams] if len(teams) > 0 else [
            team.id for team in Team.query.filter(Team.year == year).all()
        ]
        games = Game.query.filter(
            or_(
                Game.away_team_id.in_(team_ids),
                Game.home_team_id.in_(team_ids),
            )
        ).filter(
            not_(Game.bats.any(Bat.team_id.in_(team_ids)))
        ).filter(
            Game.date <= end_of_today
        ).order_by(asc(Game.date)).all()
        return games


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
        validate(
            gender,
            gender_validator,
            InvalidField(payload={'details': "Player League Request - gender"})
        )
        validate(
            email,
            string_validator,
            InvalidField(payload={"details": "Player League Request - email"})
        )
        validate(
            name,
            string_validator,
            InvalidField(payload={"details": "Player League Request - name"})
        )
        validate(
            -1 if team is None or not isinstance(team, Team) else team.id,
            lambda id: Team.does_team_exist(id),
            TeamDoesNotExist(payload={"details": "Given team does not exist"})
        )

        self.email = Player.normalize_email(email)
        self.name = name
        self.team_id = team.id
        self.pending = True
        self.gender = gender.lower()

    def accept_request(self) -> 'Player':
        """Accept the request and add the player to the team"""
        # create a player if they do not exit already
        if not self.pending:
            raise HaveLeagueRequestException(
                payload={"details": "Request already submitted"}
            )

        player = Player.find_by_email(self.email)
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

    @classmethod
    def create_request(
        cls,
        player_name: str,
        player_email: str,
        gender: str,
        team_id: int,
        ) -> 'JoinLeagueRequest':
        """Create a join league request"""
        pending_request = JoinLeagueRequest.query.filter(
            func.lower(JoinLeagueRequest.email) == player_email.lower()
        ).first()
        if pending_request is not None:
            raise HaveLeagueRequestException(
                payload={'detail': "Already pending request"}
            )

        return JoinLeagueRequest(
            player_email, player_name, Team.query.get(team_id), gender
        )

    @classmethod
    def find_request(cls, player_email: str) -> 'JoinLeagueRequest':
        """Find a pending request for the given email"""
        return JoinLeagueRequest.query.filter(
            and_(
                JoinLeagueRequest.email == player_email,
                JoinLeagueRequest.pending == True
            )
        ).first()
