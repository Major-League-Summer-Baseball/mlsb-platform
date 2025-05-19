from sqlalchemy import func, desc
from sqlalchemy.sql.functions import coalesce
from api.models.espys import Espys
from api.models.team import Team
from api.models.game import Bat, Game
from api.extensions import DB
from api.variables import HALL_OF_FAME_SIZE, UNASSIGNED_TEAM


def get_team_records(
    team_id: int = None,
    league_id: int = None,
    division_id: int = None,
    year: int = None,
    limit: int = None
) -> dict:
    """Get team records where paramters are filter if given."""
    [home_record, away_record] = Game.get_record_queries(
        year=year, division_id=division_id, league_id=league_id
    )
    query = (
        DB.session.query(
            Team,
            coalesce(home_record.c.wins, 0) + coalesce(away_record.c.wins, 0),
            (
                coalesce(home_record.c.losses, 0) +
                coalesce(away_record.c.losses, 0)
            ),
            coalesce(home_record.c.ties, 0) + coalesce(away_record.c.ties, 0),
            (
                coalesce(home_record.c.wins, 0) +
                coalesce(away_record.c.wins, 0) +
                coalesce(home_record.c.losses, 0) +
                coalesce(away_record.c.losses, 0) +
                coalesce(home_record.c.ties, 0) +
                coalesce(away_record.c.ties, 0)
            ),
            (
                coalesce(home_record.c.runs_for, 0) +
                coalesce(away_record.c.runs_for, 0)
            ),
            (
                coalesce(home_record.c.runs_against, 0) +
                coalesce(away_record.c.runs_against, 0)
            )
        )
        .join(home_record, Team.id == home_record.c.id, isouter=True)
        .join(away_record, Team.id == away_record.c.id, isouter=True)
        .order_by(
            desc(
                coalesce(home_record.c.wins, 0) +
                coalesce(away_record.c.wins, 0)
            )
        )
    )

    # additional filters
    if team_id is not None:
        query = query.filter(Team.id == team_id)
    if league_id is not None:
        query = query.filter(Team.league_id == league_id)
    if year is not None:
        query = query.filter(Team.year == year)

    # order by wins
    query = query.filter(
        func.lower(Team.color) != UNASSIGNED_TEAM
    ).order_by(desc(home_record.c.wins + away_record.c.wins))

    # limit results
    if limit is not None:
        query = query.limit(limit)

    data = query.all()
    teams = []
    for record in data:
        team = record[0].json()
        team['name'] = team['team_name']
        team['espys'] = record[0].espys_total
        team['wins'] = record[1]
        team['losses'] = record[2]
        team['ties'] = record[3]
        team['games'] = record[4]
        team['runs_for'] = int(record[5])
        team['runs_against'] = int(record[6])
        teams.append(team)
    return teams


def rank_teams_by_stats(
    stat: str, limit: int = HALL_OF_FAME_SIZE
) -> list['Team']:
    """Rank every team to ever play by the given stat."""
    teams = (
        DB.session.query(
            Team,
            func.count(Bat.team_id).label('total')
        )
        .join(Team, Team.id == Bat.team_id)
        .filter(Bat.classification == stat)
        .filter(func.lower(Team.color) != UNASSIGNED_TEAM)
        .group_by(Team)
        .order_by(func.count(Bat.team_id).desc())
        .limit(limit)
    ).all()
    result = []
    for team in teams:
        data = team[0].json()
        data['total'] = team[1]
        result.append(data)
    return result


def rank_teams_by_runs_for(
    limit: int = HALL_OF_FAME_SIZE
) -> list['Team']:
    """Rank every team to ever play by total number of runs."""
    teams = (
        DB.session.query(
            Team,
            func.sum(Bat.rbi).label('total')
        )
        .join(Team, Team.id == Bat.team_id)
        .filter(func.lower(Team.color) != UNASSIGNED_TEAM)
        .group_by(Team)
        .order_by(func.sum(Bat.rbi).desc())
        .limit(limit)
    ).all()
    result = []
    for team in teams:
        data = team[0].json()
        data['total'] = team[1]
        result.append(data)
    return result


def rank_teams_by_espys(limit: int = HALL_OF_FAME_SIZE):
    """Rank every team to ever play by their espys total."""
    teams = (
        DB.session.query(
            Team,
            func.sum(Espys.points).label('total')
        )
        .join(Team, Team.id == Espys.team_id)
        .group_by(Team)
        .order_by(func.sum(Espys.points).desc())
        .limit(limit)
    ).all()
    result = []
    for team in teams:
        data = team[0].json()
        data['total'] = round(team[1])
        result.append(data)
    return result


def rank_teams_by_record(limit: int = HALL_OF_FAME_SIZE):
    """Rank every team to ever play by their record."""
    return get_team_records(limit=HALL_OF_FAME_SIZE)
