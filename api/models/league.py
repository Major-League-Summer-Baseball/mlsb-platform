from api.extensions import DB
from api.errors import InvalidField
from api.validators import string_validator
from api.models.shared import notNone, validate


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
