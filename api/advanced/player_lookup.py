'''
@author: Dallas Fraser
@author: 2016-04-12
@organization: MLSB API
@summary: The views for looking up a player
'''
from flask_restful import Resource, reqparse
from flask import Response
from json import dumps
from api.model import Player
parser = reqparse.RequestParser()
parser.add_argument('email', type=str)
parser.add_argument('player_name', type=str)
parser.add_argument("active", type=int)

class PlayerLookupAPI(Resource):
    def post(self):
        """
            POST request to lookup Player
            Route: Route['player_lookup']
            Parameters:
                email: the league id (str)
                player_name: the player id (str)
            Returns:
                status: 200
                mimetype: application/json
                data: list of possible Players
        """
        data = []
        args = parser.parse_args()
        players = None
        active = False
        if args['active'] and args['active'] == 1:
            active = True
        if args['email']:
            # guaranteed to find player
            if not active:
                players = (Player.query
                           .filter(Player.email == args['email']).all())
            else:
                players = (Player.query
                           .filter(Player.email == args['email'])
                           .filter(Player.active == active).all())
        elif args['player_name']:
            # maybe overlap
            pn = args['player_name']
            if not active:
                players = (Player.query
                           .filter(Player.name.contains(pn)).all())
            else:
                players = (Player.query
                           .filter(Player.name.contains(pn))
                           .filter(Player.active == active).all())
        if players is not None:
            for player in players:
                data.append(player.json())
        return Response(dumps(data), status=200, mimetype="application/json")
