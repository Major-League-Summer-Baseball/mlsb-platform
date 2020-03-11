'''
@author: Dallas Fraser
@author: 2016-04-12
@organization: MLSB API
@summary: The views for player stats
'''
from flask_restful import Resource, reqparse
from flask import Response
from json import dumps
from api.cached_items import team_stats
parser = reqparse.RequestParser()
parser.add_argument('year', type=int)
parser.add_argument('league_id', type=int)
parser.add_argument('team_id', type=int)
parser.add_argument('division_id', type=int)


class TeamStatsAPI(Resource):

    def post(self):
        """
            GET request for Team Stats List
            Route: Route['player_stats']
            Parameters:
                year: the year  (int)
                team_id: the team id (int)
                league_id: the league id (int)
            Returns:
                status: 200
                mimetype: application/json
                data: list of Teams
        """
        args = parser.parse_args()
        team_id = args.get('team_id', None)
        year = args.get('year', None)
        league_id = args.get('league_id', None)
        division_id = args.get('division_id', None)
        team = team_stats(team_id, year, league_id, division_id=division_id)
        return Response(dumps(team),
                        status=200,
                        mimetype="application/json")
