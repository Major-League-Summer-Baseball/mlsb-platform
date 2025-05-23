from datetime import date
from api.extensions import DB
from api.errors import ImageDoesNotExist, InvalidField, LeagueDoesNotExist, PlayerDoesNotExist, \
    PlayerNotOnTeam, SponsorDoesNotExist
from api.models.image import Image
from api.validators import string_validator, year_validator
from api.models.shared import notNone, validate
from sqlalchemy.ext.hybrid import hybrid_property
from api.models.player import Player
from api.models.league import League
from api.models.sponsor import Sponsor

roster = DB.Table(
    'roster',
    DB.Column('player_id', DB.Integer, DB.ForeignKey('player.id')),
    DB.Column('team_id', DB.Integer, DB.ForeignKey('team.id'))
)


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
    league_id = DB.Column(DB.Integer, DB.ForeignKey('league.id'))
    year = DB.Column(DB.Integer)
    player_id = DB.Column(DB.Integer, DB.ForeignKey('player.id'))
    image_id = DB.Column(DB.Integer, DB.ForeignKey('image.id'), nullable=True)
    home_games = DB.relationship(
        'Game',
        lazy='dynamic',
        back_populates='home_team',
        foreign_keys='[Game.home_team_id]'
    )
    away_games = DB.relationship(
        'Game',
        lazy='dynamic',
        back_populates='away_team',
        foreign_keys='[Game.away_team_id]'
    )
    bats = DB.relationship('Bat', lazy='dynamic')
    captain = DB.relationship('Player', uselist=False)
    espys = DB.relationship('Espys', lazy='dynamic')
    players = DB.relationship(
        'Player', secondary=roster, back_populates='teams'
    )
    sponsor = DB.relationship('Sponsor', back_populates='teams')
    image = DB.relationship('Image', lazy=True)

    def __init__(
        self,
        color: str = None,
        sponsor_id: int = None,
        league_id: int = None,
        year: int = date.today().year,
        image_id: int = None,
    ):
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
        validate(
            image_id,
            lambda id: Image.does_image_exist(id),
            ImageDoesNotExist(payload={'details': image_id}),
            required=False
        )
        self.__update(
            color=color,
            sponsor_id=sponsor_id,
            league_id=league_id,
            year=year,
            image_id=image_id
        )

    def __update(
        self,
        color: str,
        sponsor_id: int,
        league_id: int,
        year: int,
        image_id: int
    ):
        self.color = notNone(color, self.color)
        self.sponsor_id = notNone(sponsor_id, self.sponsor_id)
        self.league_id = notNone(league_id, self.league_id)
        self.year = notNone(year, self.year)
        self.image_id = notNone(image_id, self.image_id)
        self.kik = None

    def __repr__(self) -> str:
        """Returns the string representation."""
        name_parts = []
        fallback = f"Team: {self.id}"
        if self.sponsor is not None:
            name_parts.append(str(self.sponsor))
        if self.color is not None:
            name_parts.append(self.color)
        return " ".join(name_parts) if len(name_parts) > 0 else fallback

    @hybrid_property
    def espys_total(self) -> float:
        return sum(espy.points for espy in self.espys)

    def json(self, admin: bool = False) -> dict:
        """Returns a jsonserializable object."""
        captain = None
        if self.captain is not None:
            captain = (
                self.captain.admin_json() if admin else self.captain.json()
            )
        return {
            'team_id': self.id,
            'team_name': str(self),
            'color': self.color,
            'sponsor_id': self.sponsor_id,
            'sponsor': None if self.sponsor_id is None else self.sponsor.json(),
            'league_id': self.league_id,
            'year': self.year,
            'espys': self.espys_total if self.espys_total is not None else 0,
            'captain': captain,
            'image_id': self.image_id,
            'image': None if self.image_id is None else self.image.json(),
        }

    def update(
        self,
        color: str = None,
        sponsor_id: int = None,
        league_id: int = None,
        year: int = None,
        image_id: int = None,
    ) -> None:
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
        validate(
            image_id,
            lambda id: Image.does_image_exist(id),
            ImageDoesNotExist(payload={'details': image_id}),
            required=False
        )
        self.__update(
            color=color,
            sponsor_id=sponsor_id,
            league_id=league_id,
            year=year,
            image_id=image_id,
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
        if self.player_id == player_id:
            self.player_id = None
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
        player = None if self.player_id is None else Player.query.get(
            self.player_id
        )
        return (
            player is not None and
            player.name == player_name and
            player.check_password(password)
        )

    def team_stats(self) -> None:
        pass

    @classmethod
    def get_teams_captained(cls, player_id: str) -> list['Team']:
        return Team.query.filter(Team.player_id == player_id).all()

    @classmethod
    def get_teams(cls, player_id: str) -> list['Team']:
        return (
            DB.session.query(Team)
            .join(roster)
            .filter(roster.c.player_id == player_id)
        ).all()

    @classmethod
    def does_team_exist(cls, team_id: str) -> bool:
        return Team.query.get(team_id) is not None
