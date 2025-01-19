from api.extensions import DB
from api.errors import ImageDoesNotExist, InvalidField, LeagueEventDoesNotExist, PlayerDoesNotExist, PlayerNotOnTeam
from api.models.image import Image
from api.models.player import Player
from api.models.shared import convert_date, notNone, split_datetime, validate
from api.validators import boolean_validator, date_validator, string_validator, time_validator


attendance = DB.Table(
    'attendance',
    DB.Column(
        'player_id',
        DB.Integer,
        DB.ForeignKey('player.id')
    ),
    DB.Column(
        'league_event_date_id',
        DB.Integer,
        DB.ForeignKey('league_event_date.id')
    )
)


class LeagueEvent(DB.Model):
    """
        A class used to store league events like Summerween.
        Columns:
            id: the unique id
            name: the name of the event
            description: the description of the
            image_id: the id of the image associated with the event
    """
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(80))
    description = DB.Column(DB.Text())
    active = DB.Column(DB.Boolean())
    image_id = DB.Column(DB.Integer, DB.ForeignKey('image.id'), nullable=True)
    image = DB.relationship('Image', lazy=True)

    def __init__(
        self,
        name: str,
        description: str,
        active: bool = True,
        image_id: int = None
    ):
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
        validate(
            image_id,
            lambda id: Image.does_image_exist(id),
            ImageDoesNotExist(payload={'details': image_id}),
            required=False
        )
        self.__update(
            name=name,
            description=description,
            active=active,
            image_id=image_id
        )

    def __update(
        self,
        name: str,
        description: str,
        active: bool,
        image_id: int | None
    ):
        self.name = notNone(name, self.name)
        self.description = notNone(description, self.description)
        self.active = notNone(active, self.active)
        self.image_id = notNone(image_id, self.image_id)

    def update(
        self,
        name=None,
        description=None,
        active=None,
        image_id=None
    ) -> None:
        """Update a league event.

            Parameters:
                name: the league event new name (optional str)
                description: the league event new description (optional str)
                active: is the event active or not (optional str)
                image_id: the id of the event image (optional id)
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
        validate(
            image_id,
            lambda id: Image.does_image_exist(id),
            ImageDoesNotExist(payload={'details': image_id}),
            required=False
        )
        self.__update(
            name=name,
            description=description,
            active=active,
            image_id=image_id
        )

    def json(self) -> dict:
        """Returns a jsonserializable object."""
        return {
            "league_event_id": self.id,
            "name": self.name,
            "description": self.description,
            "active": self.active,
            "image": None if self.image_id is None else self.image.json(),
            "image_id": self.image_id,
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
            image_id: the image id of the event for given year (optional id)
    """
    id = DB.Column(DB.Integer, primary_key=True)
    league_event_id = DB.Column(DB.Integer, DB.ForeignKey('league_event.id'))
    date = DB.Column(DB.DateTime)
    image_id = DB.Column(DB.Integer, DB.ForeignKey('image.id'), nullable=True)
    image = DB.relationship('Image', lazy=True)
    event = DB.relationship('LeagueEvent')
    players = DB.relationship('Player', secondary=attendance, lazy='dynamic')

    def __init__(
        self,
        date: str,
        time: str,
        league_event_id: int,
        image_id: int | None = None,
    ):
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
        validate(
            image_id,
            lambda id: Image.does_image_exist(id),
            ImageDoesNotExist(payload={'details': image_id}),
            required=False
        )
        self.__update(date, time, league_event_id, image_id)

    def __update(
        self,
        date: str,
        time: str,
        league_event_id: int,
        image_id: int | None,
    ):
        self.date = convert_date(date, time)
        self.league_event_id = notNone(league_event_id, self.league_event_id)
        self.image_id = notNone(image_id, self.image_id)

    def update(
        self,
        date: str = None,
        time: str = None,
        league_event_id: int = None,
        image_id: int = None
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
        validate(
            image_id,
            lambda id: Image.does_image_exist(id),
            ImageDoesNotExist(payload={'details': image_id}),
            required=False
        )

        (current_date, current_time) = split_datetime(self.date)
        self.__update(
            notNone(date, current_date),
            notNone(time, current_time),
            league_event_id,
            image_id
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
        event = self.event.json()
        image = (
            event['image']
            if self.image_id is None
            else self.image.json()
        )
        image_id = event['image_id'] if self.image_id is None else self.image_id
        return {
            'league_event_date_id': self.id,
            'league_event_id': self.event.id,
            'date': date,
            'time': time,
            'description': self.event.description,
            'name': self.event.name,
            'active': self.event.active,
            'attendance': self.players.count(),
            'image': image,
            'image_id': image_id,
            'has_image': image_id != event['image_id'] and image_id is not None
        }
