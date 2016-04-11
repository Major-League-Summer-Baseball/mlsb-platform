'''
@author: Dallas Fraser
@author: 2015-09-29
@organization: MLSB API
@summary: The route for subscribing to a team
'''
from flask.ext.restful import Resource, reqparse
from flask import Response
from json import dumps
from api.model import subscribe, Team
from api.authentication import requires_kik
from datetime import datetime
parser = reqparse.RequestParser()
parser.add_argument('team', type=int, required=True)
parser.add_argument('kik', type=str, required=True)
parser.add_argument('name', type=str, required=True)


class SubscribeToTeamAPI(Resource):
    @requires_kik
    def post(self):
        """
            POST request for authenticating a player is a captain of a team
            Route: Route['authenticate_captain']
            Parameters:
                kik: the kik user name(str)
                team: the id of the team the player is subscribing to (int)
                name: the name of the player (str)
            Returns:
                status: 200 
                mimetype: application/json
                data: True
        """
        args = parser.parse_args()
        kik = args['kik']
        team_id = args['team']
        name = args['name']
        result = subscribe(kik, name, team_id)
        return Response(dumps(result), status=200, mimetype="application/json")
