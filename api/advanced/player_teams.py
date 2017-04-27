'''
@author: Dallas Fraser
@author: 2016-04-12
@organization: MLSB API
@summary: The views for the teams a player is on
'''
from flask.ext.restful import Resource, reqparse
from flask import Response
from json import dumps
from api.model import Player
parser = reqparse.RequestParser()
parser.add_argument('email', type=str)
parser.add_argument('player_name', type=str)


class PlayerTeamLookupAPI(Resource):
    def post(self):
        """
            POST request to lookup a Player's teams
            Route: Route['player_lookup']
            Parameters:
                email: the league id (str)
                player_name: the player id (str)
            Returns:
                status: 200
                mimetype: application/json
                data: list of possible Teams
        """
        data = []
        args = parser.parse_args()
        players = None
        if args['email']:
            # guaranteed to find player
            players = Player.query.filter(Player.email == args['email']).all()
        elif args['player_name']:
            # maybe overlap
            pn = args['player_name']
            players = Player.query.filter(Player.name.contains(pn)).all()
        if players is not None:
            for player in players:
                for team in player.teams:
                    data.append(team.json())
        return Response(dumps(data), status=200, mimetype="application/json")
