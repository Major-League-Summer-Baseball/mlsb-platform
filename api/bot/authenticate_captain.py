from flask_restful import Resource, reqparse
from flask import Response
from json import dumps
from api.model import Player, Team
from api.errors import TeamDoesNotExist, NotTeamCaptain
from api.authentication import requires_admin
parser = reqparse.RequestParser()
parser.add_argument('team', type=int, required=True)
parser.add_argument('player_id', type=int, required=True)


class AuthenticateCaptainAPI(Resource):

    @requires_admin
    def post(self):
        """
            POST request for authenticating a player is a captain of a team
            Route: Route['botcaptain']
            Parameters:
                team: the team's id (str)
                player_id: the player_id of the captain (int)
            Returns:
                status: 200
                mimetype: application/json
                team.id: the team's id of the captain
        """
        args = parser.parse_args()
        player_id = args['player_id']
        team_id = args['team']
        team = Team.query.get(team_id)
        if team is None:
            raise TeamDoesNotExist(payload={'details': team_id})
        team_captain = Player.query.get(team.player_id)
        if team_captain.id != player_id:
            # the names do not match
            raise NotTeamCaptain(payload={'details': team_captain.name})
        # captain is authenticated
        return Response(dumps(team.id),
                        status=200,
                        mimetype="application/json")
