from flask_restful import Resource, reqparse
from flask import Response
from json import dumps
from datetime import datetime, date, time
from sqlalchemy.sql import func
from api.extensions import DB
from api.model import Player, Bat, Game, Team
from api.validators import hit_validator
from api.errors import InvalidField
parser = reqparse.RequestParser()
parser.add_argument('year', type=int)
parser.add_argument('group_by_team', type=int)
parser.add_argument('stat', type=str, required=True)


def get_leaders(hit, year=None):
    """Returns the top ten leaders for the given stats grouped by teams
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

    bats = (DB.session.query(Bat.player_id,
                             hits,
                             Bat.team_id,
                             Bat.classification,
                             Bat.team_id)
            .join(Game)
            .filter(Game.date.between(start, end))
            .filter(Bat.player_id != unassigned_id)
            .group_by(Bat.player_id)
            .group_by(Bat.classification)
            .group_by(Bat.team_id)).subquery("bats")
    players = (DB.session.query(Player.name,
                                Player.id,
                                bats.c.total,
                                bats.c.team_id,
                                bats.c.classification)
               .join(bats)
               .filter(bats.c.classification == hit)
               .order_by(bats.c.total.desc()).limit(10))
    players = players.all()
    for player in players:
        _team = Team.query.get(player[3])
        result = {'name': player[0],
                  'id': player[1],
                  'hits': player[2],
                  'team_id': player[3],
                  'team': str(_team),
                  'year': _team.year
                  }
        leaders.append(result)
    return leaders


def get_leaders_not_grouped_by_team(hit, year=None):
    """Returns the top ten leaders for the given stats not grouped by teams
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

    bats = (DB.session.query(Bat.player_id,
                             hits,
                             Bat.classification)
            .join(Game)
            .filter(Game.date.between(start, end))
            .filter(Bat.player_id != unassigned_id)
            .group_by(Bat.player_id)
            .group_by(Bat.classification)).subquery("bats")
    players = (DB.session.query(Player.name,
                                Player.id,
                                bats.c.total,
                                bats.c.classification)
               .join(bats)
               .filter(bats.c.classification == hit)
               .order_by(bats.c.total.desc()).limit(10))
    players = players.all()
    for player in players:
        result = {'name': player[0],
                  'id': player[1],
                  'hits': player[2],
                  'team_id': None,
                  'team': None,
                  'year': year
                  }
        leaders.append(result)
    return leaders


class LeagueLeadersAPI(Resource):

    def post(self):
        """
            POST request for League Leaders
            Route: Route['vleagueleaders']
            Parameters:
                year: the year  (int)
                stat: the stat to order by (str)
                group_by_team: whether to group by team or not (int)
                               default=True
            Returns:
                status: 200
                mimetype: application/json
                data: list of Players
        """
        year = None
        stat = None
        group_by_team = True
        args = parser.parse_args()
        if args['year']:
            year = args['year']
        if args['stat'] and hit_validator(args['stat'], gender="f"):
            stat = args['stat'].lower()
        else:
            raise InvalidField(payload={'details': 'Invalid stat'})
        if args['group_by_team'] == 0:
            group_by_team = False
        if group_by_team:
            players = get_leaders(stat, year=year)
        else:
            players = get_leaders_not_grouped_by_team(stat, year=year)
        return Response(dumps(players),
                        status=200,
                        mimetype="application/json")
