from datetime import datetime, date, time
from sqlalchemy.sql import func
from api.extensions import DB
from api.model import Player, Bat, Game, Team
from api.variables import HALL_OF_FAME_SIZE


def get_single_game_leader(hit: str, year=None):
    """Returns the top X leaders for the given stats in a given game
        Parameters:
          hit: the type of hit classification to get the leaders for
          year: if given then get leaders for just that year otherwise
                all years are considered
        Returns: a list of
                { 'name': str,
                  'id': int,
                  'hits': str,
                  'team_id': int,
                  'team': str,
                  'year': int
                }
    """
    leaders = []
    t = time(0, 0)
    if year is not None:
        d1 = date(year, 1, 1)
        d2 = date(year, 12, 30)
    else:
        # get all players
        d1 = date(2014, 1, 1)
        d2 = date(date.today().year, 12, 30)
    start = datetime.combine(d1, t)
    end = datetime.combine(d2, t)

    unassigned = Player.get_unassigned_player()
    unassigned_id = 0 if unassigned is None else unassigned.id
    players = (
        DB.session.query(
            Bat.game_id,
            Bat.classification,
            Player.id,
            Player.name,
            Team,
            func.count(Bat.player_id).label("total"),
        )
        .join(Player, Player.id == Bat.player_id)
        .join(Team, Team.id == Bat.team_id)
        .join(Game, Game.id == Bat.game_id)
        .filter(Bat.classification == hit)
        .filter(Game.date.between(start, end))
        .filter(Game.division_id != 3)  # remove any WNL stats
        .filter(Bat.player_id != unassigned_id)
        .group_by(Player)
        .group_by(Bat.classification)
        .group_by(Bat.game_id)
        .group_by(Team)
        .order_by(func.count(Bat.player_id).desc())
        .order_by(Team.year)
        .limit(HALL_OF_FAME_SIZE)
    ).all()
    for player in players:
        team = player[4]
        leaders.append(
            {
                'id': player[2],
                'name': player[3],
                'year': team.year,
                'team': str(team),
                'team_id': team.id,
                'game_id': player[0],
                'hits': player[5],
                'hit': player[1]
            }
        )
    return leaders


def get_leaders(hit, year=None):
    """Returns the top X leaders for the given stats grouped by teams
        Parameters:
          hit: the type of hit classification to get the leaders for
          year: if given then get leaders for just that year otherwise
                all years are considered
        Returns: a list of
                { 'name': str,
                  'id': int,
                  'hits': str,
                  'team_id': int,
                  'team': str,
                  'year': int
                }
    """
    leaders = []
    hits = func.count(Bat.player_id).label("total")
    t = time(0, 0)
    if year is not None:
        d1 = date(year, 1, 1)
        d2 = date(year, 12, 30)
    else:
        # get all players
        d1 = date(2014, 1, 1)
        d2 = date(date.today().year, 12, 30)
    start = datetime.combine(d1, t)
    end = datetime.combine(d2, t)

    unassigned = Player.get_unassigned_player()
    unassigned_id = 0 if unassigned is None else unassigned.id

    records = (
        DB.session.query(
            hits,
            Player,
            Team,
        )
        .join(Player, Player.id == Bat.player_id)
        .join(Team, Team.id == Bat.team_id)
        .join(Game, Game.id == Bat.game_id)
        .filter(Game.date.between(start, end))
        .filter(Bat.player_id != unassigned_id)
        .filter(Bat.classification == hit)
        .group_by(Player)
        .group_by(Team)
        .order_by(func.count(Bat.player_id).desc())
        .order_by(Team.year)
        .limit(HALL_OF_FAME_SIZE)
    ).all()
    for record in records:
        team = record[2]
        player = record[1]
        result = {
            'name': player.name,
            'id': player.id,
            'hits': record[0],
            'team_id': team.id,
            'team': str(team),
            'year': team.year
        }
        leaders.append(result)
    return leaders


def get_leaders_not_grouped_by_team(hit, year=None):
    """Returns the top X leaders for the given stats not grouped by teams
        Parameters:
          hit: the type of hit classification to get the leaders for
          year: if given then get leaders for just that year otherwise
                all years are considered
        Returns: a list of
                { 'name': str,
                  'id': int,
                  'hits': str,
                  'team_id': None,
                  'team': None,
                  'year': None
                }
    """
    leaders = []
    hits = func.count(Bat.player_id).label("total")
    t = time(0, 0)
    if year is not None:
        d1 = date(year, 1, 1)
        d2 = date(year, 12, 30)
    else:
        # get all players
        d1 = date(2014, 1, 1)
        d2 = date(date.today().year, 12, 30)
    start = datetime.combine(d1, t)
    end = datetime.combine(d2, t)

    unassigned = Player.get_unassigned_player()
    unassigned_id = 0 if unassigned is None else unassigned.id

    players = (
        DB.session.query(
            hits,
            Player.id,
            Player.name,
        )
        .join(Player, Player.id == Bat.player_id)
        .join(Game, Game.id == Bat.game_id)
        .filter(Bat.classification == hit)
        .filter(Game.date.between(start, end))
        .filter(Bat.player_id != unassigned_id)
        .group_by(Player)
        .group_by(Bat.classification)
        .order_by(func.count(Bat.player_id).desc())
        .limit(HALL_OF_FAME_SIZE)
    ).all()
    for player in players:
        result = {'name': player[2],
                  'id': player[1],
                  'hits': player[0],
                  'team_id': None,
                  'team': None,
                  'year': year
                  }
        leaders.append(result)
    return leaders