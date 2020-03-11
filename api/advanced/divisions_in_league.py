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
from api.cached_items import get_divisions_for_league_and_year
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
        result = get_divisions_for_league_and_year(year, league_id)
        return Response(dumps(result), status=200,
                        mimetype="application/json")
