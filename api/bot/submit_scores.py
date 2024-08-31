from typing import List
from flask_restful import Resource, reqparse
from flask import Response
from json import dumps
from api.extensions import DB
from api.model import Player, Bat, Game, Team
from api.authentication import requires_admin
from api.errors import InvalidField, NotTeamCaptain, GameDoesNotExist, \
    PlayerNotSubscribed, TeamDoesNotExist
from api.variables import UNASSIGNED
from api.cached_items import handle_table_change
from api.tables import Tables
parser = reqparse.RequestParser()
parser.add_argument('game_id', type=int, required=True)
parser.add_argument('player_id', type=int, required=True)
parser.add_argument('score', type=int, required=True)
parser.add_argument('hr', type=int, action="append")
parser.add_argument('ss', type=int, action="append")





class SubmitScoresAPI(Resource):

    @requires_admin
    def post(self):
        """
            POST request for submitting Score Summaries
            Route: Route['botsubmitscore']
            Parameters:
                game_id: the game_id (int)
                player_id: the player_id of the captain (str)
                score: the score of the captains team (int)
                hr: a list of player's name who hit homeruns(List of str)
                ss: a list of player's name who hit sentry singles (List - str)
            Returns:
                status: 200
                mimetype: application/json
                data: True
        """
        args = parser.parse_args()
        submit_score(
            args.get('game_id', UNASSIGNED),
            args.get('player_id', UNASSIGNED),
            args.get('score', 0),
            args.get('hr', []),
            args.get('ss', []))
        return Response(dumps(True), status=200, mimetype="application/json")
