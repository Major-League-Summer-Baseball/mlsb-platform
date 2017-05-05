'''
@author: Dallas Fraser
@author: 2017-05-03
@organization: MLSB API
@summary: The bot API for authenticating a captain
'''
from flask.ext.restful import Resource, reqparse
from flask import Response
from json import dumps
from api import DB
from api.model import Player, Game
from api.errors import PlayerDoesNotExist
from api.authentication import requires_admin
from datetime import timedelta, date
from sqlalchemy import or_
parser = reqparse.RequestParser()
parser.add_argument('player_id', type=int, required=True)


class UpcomingGamesAPI(Resource):
    @requires_admin
    def post(self):
        """
            POST request for the upcoming games for the given player
            Route: Route['botupcominggames']
            Parameters:
                player_id: the id of the player (int)
            Returns:
                status: 200
                mimetype: application/json
                result: list of games
        """
        args = parser.parse_args()
        player_id = args['player_id']
        player = Player.query.get(player_id)
        if player is None:
            raise PlayerDoesNotExist(payload={'details': player_id})
        teams = []
        today = date.today() + timedelta(days=-1)
        next_two_weeks = today + timedelta(days=14)
        for team in player.teams:
            teams.append(team.id)
        games = DB.session.query(Game).filter(or_(Game.away_team_id.in_(teams),
                                              (Game.home_team_id.in_(teams))))
        games = games.filter(Game.date.between(today, next_two_weeks))
        result = []
        for game in games:
            result.append(game.json())
        return Response(dumps(result), status=200, mimetype="application/json")
