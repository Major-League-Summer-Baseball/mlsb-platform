'''
@author: Dallas Fraser
@author: 2016-04-12
@organization: MLSB API
@summary: The views for player stats
'''
from flask.ext.restful import Resource, reqparse
from flask import Response
from json import dumps
from api import DB
from api.model import Player, Bat, Game, Team
from datetime import datetime, date, time
from sqlalchemy.sql import func
from api.variables import UNASSIGNED, UNASSIGNED_EMAIL
parser = reqparse.RequestParser()
parser.add_argument('year', type=int)
parser.add_argument('stat', type=str, required=True)

def get_leaders(hit, year=None):
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
    unassigned_id = 0
    unassigned = Player.query.filter_by(email=UNASSIGNED_EMAIL).first()
    if unassigned is not None:
        unassigned_id = unassigned.id
    bats = (DB.session.query(Bat.player_id,
                            hits,
                            Bat.team_id,
                            Bat.classification,
                            Bat.team_id
                            ).join(Game)
                            .filter(Game.date.between(start, end))
                            .filter(Bat.player_id != unassigned_id)
                            .group_by(Bat.player_id)
                            .group_by(Bat.classification)
                            .group_by(Bat.team_id)).subquery("bats")
    players = (DB.session.query(Player.name,
                              Player.id,
                              bats.c.total,
                              bats.c.team_id,
                              bats.c.classification
                              )
                              .join(bats)
                              .filter(bats.c.classification == hit)
                              .order_by(bats.c.total.desc()).limit(10)
                              )
    players = players.all()
    for player in players:
        result = {'name': player[0],
                  'id': player[1],
                  'hits': player[2],
                  'team_id': player[3],
                  'team': str(Team.query.get(player[3]))
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
            Returns:
                status: 200 
                mimetype: application/json
                data: list of Players
        """
        year = None
        stat = None
        args = parser.parse_args()
        if args['year']:
            year = args['year']
        if args['stat']:
            stat = args['stat']
        players = get_leaders(stat,
                              year=year)
        return Response(dumps(players), status=200, mimetype="application/json")
