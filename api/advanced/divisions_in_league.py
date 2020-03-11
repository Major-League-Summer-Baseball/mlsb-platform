'''
@author: Dallas Fraser
@date: 2016-04-12
@organization: MLSB API
@summary: The views for finding what divisions are in a given league
'''
from flask_restful import Resource, reqparse
from flask import Response
from json import dumps
from api import DB
from api.errors import LeagueDoesNotExist
from api.model import Game, League, Division
from datetime import datetime, date, time, timedelta
from api.cached_items import get_league_map
parser = reqparse.RequestParser()
parser.add_argument('league_id', type=int, required=True)
parser.add_argument('game_id', type=int)
parser.add_argument('division_id', type=int)


class DivisionsLeagueAPI(Resource):
    def get(self, year, league_id):
        """
            GET request to get the various divisions for the given leagu
            Route: Route['vdivisions']/<league_ud: int>
            Parameters:
                league_id: the league id (int)
            Returns:
                status: 200
                mimetype: application/json
                data: list of divisions
        """
        if get_league_map().get(league_id, None) is None:
            raise LeagueDoesNotExist(payload={'details': league_id})
        start = datetime.combine(date(year, 1, 1), time(0, 0))
        end = datetime.combine(date(year, 12, 30), time(23, 0))
        division_ids = (DB.session.query(Division.id.distinct().label('id'))
                        .join(Game)
                        .filter(Game.league_id == league_id)
                        .filter(Game.date.between(start, end))).all()
        divisions_result = [Division.query.get(division[0]).json()
                            for division in division_ids]
        return Response(dumps(divisions_result), status=200,
                        mimetype="application/json")
