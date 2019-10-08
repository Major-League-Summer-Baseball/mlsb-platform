'''
@author: Dallas Fraser
@author: 2016-04-12
@organization: MLSB API
@summary: The Kik api for authenticating a captain
'''
from flask_restful import Resource, reqparse
from flask import Response
from json import dumps
from api import DB
from api.model import Player, Team
from api.errors import TeamDoesNotExist, TeamAlreadyHasCaptain,\
    NotTeamCaptain
from api.authentication import requires_kik
parser = reqparse.RequestParser()
parser.add_argument('team', type=int, required=True)
parser.add_argument('captain', type=str, required=True)
parser.add_argument('kik', type=str, required=True)


class AuthenticateCaptainAPI(Resource):

    @requires_kik
    def post(self):
        """
            POST request for authenticating a player is a captain of a team
            Route: Route['kikcaptain']
            Parameters:
                team: the team's id (str)
                captain: the name of the captain (str)
                kik: the captain's kik user name (str)
            Returns:
                status: 200
                mimetype: application/json
                data: id: the captain's team id
        """
        args = parser.parse_args()
        captain = args['captain']
        team_id = args['team']
        kik = args['kik']
        team = Team.query.get(team_id)
        if team is None:
            raise TeamDoesNotExist(payload={'details': team_id})
        team_captain = Player.query.get(team.player_id)
        if team_captain.name != captain:
            # the names do not match
            raise NotTeamCaptain(payload={'details': team_captain.name})
        if team_captain.kik is None:
            # update their kik name
            team_captain.kik = kik
            DB.session.commit()
        elif team_captain.kik != kik:
            # something fishy is going on
            raise TeamAlreadyHasCaptain(payload={'details': team_captain.kik})
        # captain is authenticated
        return Response(dumps(team.id),
                        status=200,
                        mimetype="application/json")
