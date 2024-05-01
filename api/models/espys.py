from datetime import datetime
from api.extensions import DB
from api.errors import InvalidField, SponsorDoesNotExist, TeamDoesNotExist
from api.validators import date_validator, float_validator, string_validator, \
    time_validator
from api.models.shared import convert_date, notNone, split_datetime, validate
from api.models.sponsor import Sponsor
from api.models.team import Team


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
