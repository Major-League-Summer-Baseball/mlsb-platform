'''
Name: Dallas Fraser
Date: 2014-08-25
Project: MLSB API
Purpose: To create an application to act as an api for the database
'''
from flask.ext.restful import Resource, reqparse
from flask import Response
from json import dumps
from api.authentication import requires_admin
from api import DB
from api.model import Team
from api.errors import TeamDoesNotExist
parser = reqparse.RequestParser()
parser.add_argument('player_id', type=int, required=True)
parser.add_argument('captain', type=int)


class TeamRosterAPI(Resource):
    def get(self, team_id):
        """
            GET request for Team Roster List
            Route: Routes['team_roster']/<int:team_id>
            Returns:
                status: 200
                mimetype: application/json
                data: [
                    'team_id': { 'color': '',
                                 'league_id': int,
                                 'sponsor_id': int,
                                 'team_id': int,
                                 'year': int},
                                 'captain': {  'email': '',
                                               'gender': '',
                                               'player_id': int,
                                               'player_name': ''},
                                 'players': [{'email': '',
                                    'gender': '',
                                    'player_id': int,
                                    'player_name': ''}]
                            },
                    'team_id':{...},
                ]
        """
        team = Team.query.get(team_id)
        if team is None:
            raise TeamDoesNotExist(payload={'details': team_id})
        result = team.json()
        result['players'] = []
        for player in team.players:
            result['players'].append(player.json())
        response = Response(dumps(result),
                            status=200, mimetype="application/json")
        return response

    @requires_admin
    def delete(self, team_id):
        """
            DELETE request for Team Roster List
            Routes: Routes['team_roster']/<int:team_id>
            Parameters :
                player_id: The player id (int)
               team_id: The team id (int)
            Returns:
                status: 200
                mimetype: application/json
                data:
                    success: tells if request was successful (boolean)
                    message: the status message (string)
        """
        args = parser.parse_args()
        team = Team.query.get(team_id)
        if team is None:
            raise TeamDoesNotExist(payload={'details': team_id})
        team.remove_player(args['player_id'])
        DB.session.commit()
        if team.player_id == args['player_id']:
            team.player_id = None
            DB.session.commit()
        response = Response(dumps(None), status=200,
                            mimetype="application/json")
        return response

    @requires_admin
    def post(self, team_id):
        """
            POST request for Team Roster List
            Route: Routes['team_roster']/<int:team_id>
            Parameters :
                player_id: a player's identifier (int)
                captain: a 1 if a captain (int)
            Returns:
                status: 200
                mimetype: application/json
                data:
                    success: tells if request was successful (boolean)
                    message: the status message (string)
                    failures: a list of parameters that failed (list of string)
        """
        args = parser.parse_args()
        team = Team.query.get(team_id)
        if team is None:
            raise TeamDoesNotExist(payload={'details': team_id})
        captain = False
        if args['captain'] and args['captain'] == 1:
            captain = True
        team.insert_player(args['player_id'], captain=captain)
        DB.session.commit()
        response = Response(dumps(None), status=201,
                            mimetype="application/json")
        return response

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}
