'''
Name: Dallas Fraser
Date: 2014-08-25
Project: MLSB API
Purpose: To create an application to act as an api for the database
'''
from flask.ext.restful import Resource, reqparse
from flask import Response
from json import dumps
from api.validators import date_validator
from api import DB
from api.model import Team, Player, roster
parser = reqparse.RequestParser()
parser.add_argument('player_id', type=int)
parser.add_argument('team_id', type=int)
parser.add_argument('captain', type=int)


class TeamRosterAPI(Resource):
    def get(self):
        """
            GET request for Team Roster List
            Route: /team_roster
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
        teams = Team.query.all()
        result = []
        for i in range(0, len(teams)):
            team = {i : teams[i].json()}
            team['players'] = []
            for player in teams[i].players :
                team['players'].append(player.json())
            team['captain'] = None
            if teams[i].player_id is not None:
                captain = Player.query.get(teams[i].player_id)
                if captain is not None:
                    team['captain'] = captain.json()
            result.append(team)
        return Response(dumps(result), status=200,
                        mimetype="application/json")

    def delete(self):
        """
            DELETE request for Team Roster List
            Routes: Routes['team_roster']
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
        result = {'success': False,
                  'message': '',}
        if args['team_id'] and args['player_id']:
            player = Player.query.get(args['player_id'])
            team = Team.query.get(args['team_id'])
            if player is not None and team is not None:
                if player in team.players:
                    team.players.remove(player)
                    DB.session.commit()
                    result['success'] = True
                else:
                    result['message'] = "Player is not on the team"
            else:
                result['message'] = "Invalid parameters"
        else:
            result['message'] = "Invalid parameters"
        return Response(dumps(result), status=200, mimetype="application/json")

    def post(self):
        """
            POST request for Team Roster List
            Route: /team_roster
            Parameters :
                player_id: a player's identifier (int)
                team_id: a team identifier (int)
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
        result = {'success': False,
                  'message': '',
                  'failures': []}
        if args['player_id'] and args['team_id']:
            player = Player.query.get(args['player_id'])
            team = Team.query.get(args['team_id'])
            if player is None:
                result['failures'].append("Invalid player")
            if team is None:
                result['failures'].append("Invalid team")
            if len(result['failures']) > 0:
                result['message'] = "Invalid parameters"
            else:
                if args['captain'] and args['captain'] == 1:
                    team.player_id = args['player_id']
                else:
                    team.players.append(player)
                result['success'] = True
                DB.session.commit()
        else:
            result['message'] = "Failed to properly supply the required fields"
        return Response(dumps(result), status=200, mimetype="application/json")

    def option(self):
        return {'Allow': 'PUT'}, 200, \
            { 'Access-Control-Allow-Origin': '*', \
            'Access-Control-Allow-Methods': 'PUT,GET'}

