'''
@author: Dallas Fraser
@author: 2016-04-12
@organization: MLSB API
@summary: The views for the teams a player is on
'''
from flask_restful import Resource, reqparse
from flask import Response
from json import dumps
from api.model import Player
parser = reqparse.RequestParser()
parser.add_argument('email', type=str)
parser.add_argument('player_name', type=str)
parser.add_argument("player_id", type=int)


class PlayerTeamLookupAPI(Resource):

    def post(self):
        """
            POST request to lookup a Player's teams
            Route: Route['player_lookup']
            Parameters:
                email: the league id (str)
                player_name: the player id (str)
                player_id: the player id (int)
            Returns:
                status: 200
                mimetype: application/json
                data: list of possible Teams
        """
        data_lookup = {}
        data = []
        args = parser.parse_args()
        players = None
        if args['player_id']:
            # guaranteed to get a player
            players = [Player.query.get(args['player_id'])]
        elif args['email']:
            # guaranteed to find player
            email = args['email'].strip().lower()
            players = Player.query.filter(Player.email == email).all()
        elif args['player_name']:
            # maybe overlap
            pn = args['player_name']
            players = Player.query.filter(Player.name.contains(pn)).all()
        if players is not None:
            for player in players:
                for team in player.teams:
                    if(team.id not in data_lookup):
                        data_lookup[team.id] = True
                        data.append(team.json())
        return Response(dumps(data), status=200, mimetype="application/json")
