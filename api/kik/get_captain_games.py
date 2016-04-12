'''
@author: Dallas Fraser
@author: 2016-04-12
@organization: MLSB API
@summary: The Kik API for authenticating a captain
'''
from flask.ext.restful import Resource, reqparse
from flask import Response
from json import dumps
from api import DB
from api.model import Player, Team, Game, Bat
from api.errors import TDNESC
from api.authentication import requires_kik
from datetime import datetime
from sqlalchemy import or_
parser = reqparse.RequestParser()
parser.add_argument('team', type=int, required=True)
parser.add_argument('kik', type=str, required=True)


class CaptainGamesAPI(Resource):
    @requires_kik
    def post(self):
        """
            POST request for retrieving a captain games that needs scores submitted
            Route: Route['kikcaptaingames']
            Parameters:
                team: the team's id (str)
                kik: the captain's kik user name (str)
            Returns:
                status: 200 
                mimetype: application/json
                result: list of games objects
        """
        args = parser.parse_args()
        team_id = args['team']
        kik = args['kik']
        team = Team.query.get(team_id)
        if team is None:
            return Response(dumps("Team does not exist"), status=TDNESC, mimetype="application/json")
        team_captain = Player.query.get(team.player_id)
        if team_captain.kik != kik:
            # something fishy is going on
            return Response(dumps("Not the right captain for the team"), status=401, mimetype="application/json")
        # captain is authenticated
        # get all the bats for that team and its game id
        bats = DB.session.query(Bat.game_id).filter(Bat.team_id == team_id).all()
        if (len(bats) > 0):
            games = DB.session.query(Game).filter(or_(Game.away_team_id == team_id, Game.home_team_id==team_id)).filter(Game.date <= datetime.today()).filter(~Game.id.in_(bats)).all()
        else:
            games = DB.session.query(Game).filter(or_(Game.away_team_id == team_id, Game.home_team_id==team_id)).filter(Game.date <= datetime.today()).all()
        # now get the teams games, that have past game date and have no bats
        result = []
        for game in games:
            result.append(game.json())
        return Response(dumps(result), status=200, mimetype="application/json")
