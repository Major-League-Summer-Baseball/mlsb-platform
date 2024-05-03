from datetime import datetime, date, time
from api.extensions import DB
from api.errors import DivisionDoesNotExist, GameDoesNotExist, InvalidField, \
    LeagueDoesNotExist, PlayerDoesNotExist, TeamDoesNotExist
from api.helper import normalize_string
from api.models.team import Team
from api.validators import date_validator, field_validator, hit_validator, \
    inning_validator, rbi_validator, string_validator, time_validator
from api.models.shared import convert_date, notNone, split_datetime, validate
from sqlalchemy import and_, select, func, or_, desc, asc, not_, case
from sqlalchemy.orm import column_property, PropComparator
from sqlalchemy.sql.expression import Alias
from sqlalchemy.sql.functions import coalesce
from api.models.player import Player
from api.models.league import Division, League


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
    home_team_id = DB.Column(
        DB.Integer,
        DB.ForeignKey('team.id', use_alter=True, name='fk_home_team_game')
    )
    away_team_id = DB.Column(
        DB.Integer,
        DB.ForeignKey('team.id', use_alter=True, name='fk_away_team_game')
    )
    league_id = DB.Column(DB.Integer, DB.ForeignKey('league.id'))
    division_id = DB.Column(DB.Integer, DB.ForeignKey('division.id'))
    bats = DB.relationship("Bat", backref="game", lazy='dynamic')
    date = DB.Column(DB.DateTime)
    status = DB.Column(DB.String(120))
    field = DB.Column(DB.String(120))

    # use this column property sparingly
    away_team_score = column_property(
        select([func.sum(Bat.rbi)])
        .where(
            and_(
                (Bat.game_id == id),
                (Bat.team_id == away_team_id)
            )
        )
        .correlate_except(Bat),
        deferred=True,
        group='summary'
    )
    # use this column property sparingly
    home_team_score = column_property(
        select([func.sum(Bat.rbi)])
        .where(
            and_(
                (Bat.game_id == id),
                (Bat.team_id == home_team_id)
            )
        )
        .correlate_except(Bat),
        deferred=True,
        group='summary')
    hit_clause = or_(
        (Bat.classification == 's'),
        (Bat.classification == 'ss'),
        (Bat.classification == 'd'),
        (Bat.classification == 'hr')
    )
    home_team_hits = column_property(
        select([func.count(Bat.id)])
        .where(
            and_(
                (Bat.game_id == id),
                (Bat.team_id == home_team_id),
                hit_clause
            )
        )
        .correlate_except(Bat),
        deferred=True,
        group='summary'
    )
    away_team_hits = column_property(
        select([func.count(Bat.id)])
        .where(
            and_(
                (Bat.game_id == id),
                (Bat.team_id == away_team_id),
                hit_clause
            )
        )
        .correlate_except(Bat),
        deferred=True,
        group='summary'
    )

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
    def get_game_results_query(
        cls, league_id: int = None, division_id: int = None, year: int = None
    ) -> list[Alias]:
        """Returns a subquery for getting home"""
        home_score = (
            DB.session.query(
                Game.id, coalesce(func.sum(Bat.rbi), 0).label('runs')
            )
            .select_from(Game).join(
                Bat,
                and_(
                    Bat.team_id == Game.home_team_id,
                    Bat.game_id == Game.id
                ),
                isouter=True
            ).group_by(Game.id).subquery()
        )
        away_score = (
            DB.session.query(
                Game.id, coalesce(func.sum(Bat.rbi), 0).label('runs')
            )
            .select_from(Game).join(
                Bat,
                and_(
                    Bat.team_id == Game.away_team_id,
                    Bat.game_id == Game.id
                ),
                isouter=True
            ).group_by(Game.id).subquery()
        )
        query = (
            DB.session.query(
                Game.id,
                Game.away_team_id,
                Game.home_team_id,
                away_score.c.runs.label('away_score'),
                home_score.c.runs.label('home_score')
            )
            .select_from(Game)
            .join(home_score, Game.id == home_score.c.id)
            .join(away_score, Game.id == away_score.c.id)
        )
        if year is not None:
            if year == datetime.now().year:
                start = datetime.combine(date(year, 1, 1), time(0, 0))
                end = datetime.now()
            else:
                start = datetime.combine(date(year, 1, 1), time(0, 0))
                end = datetime.combine(date(year, 12, 30), time(0, 0))
            query = query.filter(Game.date.between(start, end))
        else:
            start = datetime.combine(date(2014, 1, 1), time(0, 0))
            end = datetime.combine(date.today(), time(23,59))
            query = query.filter(Game.date.between(start, end))
        if league_id is not None:
            query = query.filter(Game.league_id == league_id)
        if division_id is not None:
            query = query.filter(Game.division_id == division_id)
        return query.subquery()

    @classmethod
    def get_record_queries(
        cls, league_id: int = None, division_id: int = None, year: int = None
    ) -> list[Alias, Alias]:
        """Returns subqueries for home/away record that can be used"""
        home_results = cls.get_game_results_query(
            league_id=league_id, division_id=division_id, year=year
        )
        away_results = cls.get_game_results_query(
            league_id=league_id, division_id=division_id, year=year
        )
        home_losses = generate_sum_of_case(and_(
            Team.id == home_results.c.home_team_id,
            home_results.c.home_score < home_results.c.away_score
        ), 1)
        home_ties = generate_sum_of_case(and_(
            Team.id == home_results.c.home_team_id,
            home_results.c.home_score == home_results.c.away_score
        ), 1)
        home_wins = generate_sum_of_case(and_(
            Team.id == home_results.c.home_team_id,
            home_results.c.home_score > home_results.c.away_score
        ), 1)
        home_runs_for = generate_sum_of_case(
            Team.id == home_results.c.home_team_id, home_results.c.home_score
        )
        home_runs_against = generate_sum_of_case(
            Team.id == home_results.c.home_team_id, home_results.c.away_score
        )
        home_record = (
            DB.session.query(
                Team.id,
                home_losses.label('losses'),
                home_ties.label('ties'),
                home_wins.label('wins'),
                home_runs_for.label('runs_for'),
                home_runs_against.label('runs_against')

            )
            .select_from(Team)
            .join(home_results, home_results.c.home_team_id == Team.id)
            .group_by(Team.id)
        ).subquery()

        away_losses = generate_sum_of_case(and_(
            Team.id == away_results.c.away_team_id,
            away_results.c.away_score < away_results.c.home_score
        ), 1)
        away_ties = generate_sum_of_case(and_(
            Team.id == away_results.c.away_team_id,
            away_results.c.away_score == away_results.c.home_score
        ), 1)
        away_wins = generate_sum_of_case(and_(
            Team.id == away_results.c.away_team_id,
            away_results.c.away_score > away_results.c.home_score
        ), 1)
        away_runs_for = generate_sum_of_case(
            Team.id == away_results.c.away_team_id, away_results.c.away_score
        )
        away_runs_against = generate_sum_of_case(
            Team.id == away_results.c.away_team_id, away_results.c.home_score
        )
        away_record = (
            DB.session.query(
                Team.id,
                away_losses.label('losses'),
                away_ties.label('ties'),
                away_wins.label('wins'),
                away_runs_for.label('runs_for'),
                away_runs_against.label('runs_against')
            )
            .select_from(Team)
            .join(away_results, away_results.c.away_team_id == Team.id)
            .group_by(Team.id)
        ).subquery()
        return [away_record, home_record]

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


def generate_sum_of_case(condition: PropComparator, count) -> Alias:
    """Generate a func to sum the given condition"""
    return func.sum(case([(condition, count)], else_=0))
