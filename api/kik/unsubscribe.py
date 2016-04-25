'''
@author: Dallas Fraser
@author: 2016-04-12
@organization: MLSB API
@summary: The Kik API for unsubscribing to a team
'''
from flask.ext.restful import Resource, reqparse
from flask import Response
from json import dumps
from api.model import unsubscribe
from api.authentication import requires_kik
parser = reqparse.RequestParser()
parser.add_argument('team', type=int, required=True)
parser.add_argument('kik', type=str, required=True)

class UnSubscribeToTeamAPI(Resource):
    @requires_kik
    def post(self):
        """
            POST request for a player unsubscribing to a team
            Route: Route['kikunsubscribe']
            Parameters:
                kik: the kik user name(str)
                team: the id of the team the player is subscribing to (int)
            Returns:
                status: 200 
                mimetype: application/json
                data: True
        """
        args = parser.parse_args()
        kik = args['kik']
        team_id = args['team']
        result = unsubscribe(kik, team_id)
        return Response(dumps(result), status=200, mimetype="application/json")
