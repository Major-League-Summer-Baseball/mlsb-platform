'''
@author: Dallas Fraser
@author: 2017-05-03
@organization: MLSB API
@summary: The bot API for authenticating a captain
'''
from flask_restful import Resource, reqparse
from flask import Response
from json import dumps
from api import DB
from api.model import Team, Game, Bat
from api.errors import TeamDoesNotExist, NotTeamCaptain, InvalidField
from api.authentication import requires_admin
from datetime import datetime
from sqlalchemy import or_
parser = reqparse.RequestParser()
parser.add_argument('team', type=int, required=True)
parser.add_argument('player_id', type=int, required=True)


def games_without_scores(team_id: int) -> list[Game]:
    """Returns a list of games without scores for the given team"""
    bats = (DB.session.query(Bat.game_id)
            .filter(Bat.team_id == team_id)).all()
    today = datetime.today()
    end_of_today = datetime(
        today.year, today.month, today.day, hour=23, minute=59)
    if (len(bats) > 0):
        games = (DB.session.query(Game)
                 .filter(or_(Game.away_team_id == team_id,
                             Game.home_team_id == team_id))
                 .filter(Game.date <= end_of_today))
        for bat in bats:
            games = games.filter(Game.id != bat.game_id)
        games = games.all()
    else:
        today = 
        games = (DB.session.query(Game)
                 .filter(or_(Game.away_team_id == team_id,
                             Game.home_team_id == team_id))
                 .filter(Game.date <= end_of_today)).all()
    return games


class CaptainGamesAPI(Resource):

    @requires_admin
    def post(self):
        """
            POST request for retrieving a captain
            games that needs scores submitted
            Route: Route['botcaptaingames']
            Parameters:
                team: the team's id (str)
                player_id: the captain's player_id (int)
            Returns:
                status: 200
                mimetype: application/json
                result: list of games objects
        """
        args = parser.parse_args()
        team_id = args['team']
        player_id = args['player_id']
        team = Team.query.get(team_id)
        if team is None:
            raise TeamDoesNotExist(payload={'details': team_id})
        if team.player_id is None:
            raise InvalidField(payload={"details":
                                        "Team's captain has not been set"})
        if player_id != team.player_id:
            # something fishy is going on
            raise NotTeamCaptain(payload={'details': player_id})
        # captain is authenticated
        # now get the teams games, that have past game date and have no bats
        result = [game.json() for game in games_without_scores(team_id)]
        return Response(dumps(result), status=200, mimetype="application/json")
