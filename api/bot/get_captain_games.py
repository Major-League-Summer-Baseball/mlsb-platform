from flask_restful import Resource, reqparse
from flask import Response
from json import dumps
from api.model import Team, Game
from api.errors import TeamDoesNotExist, NotTeamCaptain, InvalidField
from api.authentication import requires_admin

parser = reqparse.RequestParser()
parser.add_argument('team', type=int, required=True)
parser.add_argument('player_id', type=int, required=True)


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
        result = [game.json() for game in Game.games_needing_scores(
            [team], team.year)
        ]
        return Response(dumps(result), status=200, mimetype="application/json")
