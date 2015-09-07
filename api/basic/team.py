'''
Name: Dallas Fraser
Date: 2014-08-22
Project: MLSB API
Purpose: To create an application to act as an api for the database
'''
from flask.ext.restful import Resource, reqparse
from flask import Response
from json import dumps
from api.validators import string_validator
from api.model import Team, Sponsor, League
from api import DB
parser = reqparse.RequestParser()
parser.add_argument('sponsor_id', type=int)
parser.add_argument('color', type=str)
parser.add_argument('league_id', type=int)


class TeamAPI(Resource):
    def get(self, team_id):
        """
            GET request for Team Object matching given team_id
            Route: /teams/<team_id: int>
            Returns:
                status: 200 
                mimetype: application/json
                data: 
                    success: tells if request was successful (boolean)
                    message: the status message (string)
                    data:  {
                            team_name: string, team_id: int,
                            captain_id: int, sponsor_id: int,
                            photo: int, color:string
                            }
        """
        # expose a single team
        result = {'success': False,
                  'message': '',
                  'failures':[]}
        entry  = Team.query.get(team_id)
        if entry is None:
            result['message'] = 'Not a valid team ID'
            return Response(dumps(result), status=404, mimetype="application/json")
        result['success'] = True
        result['data'] = entry.json()
        return Response(dumps(result), status=200, mimetype="application/json")

    def delete(self, team_id):
        """
            DELETE request for Team
            Route: /teams/<team_id:int>
            Returns:
                status: 200 
                mimetype: application/json
                data: 
                    success: tells if request was successful (boolean)
                    message: the status message (string)
        """
        result = {'success': False,
                  'message': '',}
        team = Team.query.get(team_id)
        # delete a single user
        if team is None:
            result['message'] = 'Not a valid team ID'
            return Response(dumps(result), status=404, mimetype="application/json")
        # delete a single team
        DB.session.delete(team)
        DB.session.commit()
        result['success'] = True
        result['message'] = 'Team was deleted'
        return Response(dumps(result), status=200, mimetype="application/json")

    def put(self, team_id):
        """
            PUT request for team
            Route: /teams/<team_id:int>
            Parameters :
                team_name: The team's name (string)
                captain_id: The captain player id (int)
                sponsor_id: The sponsor id (int)
                team_picture_id: The picture id (int)
                color: the color of the team (string)
            Returns:
                status: 200 
                mimetype: application/json
                data: 
                    success: tells if request was successful (boolean)
                    message: the status message (string)
                    failures: a list of parameters that failed to update 
                              (list of string)
        """
        # update a single user
        result = {'success': False,
                  'message': '',
                  'failures':[]}
        team = Team.query.get(team_id)
        args = parser.parse_args()
        if team is None:
            result['message'] = "Not a valid team ID"
            return Response(dumps(result), status=404,
                            mimetype="application/json")
        if args['color'] and string_validator(args['color']):
            team.color = args['color']
        elif args['color'] and not string_validator(args['color']):
            result['failures'].append('Invalid color')
        if args['sponsor_id']:
            sid = args['sponsor_id']
            sponsor = Sponsor.query.get(sid)
            if sponsor is None:
                result['failures'].append('Invalid sponsor ID')
            else:
                team.sponsor_id = sid
        if args['league_id']:
            lid = args['league_id']
            league = League.query.get(lid)
            if league is None:
                result['failures'].append('Invalid league ID')
            else:
                team.league_id = lid
        if len(result['failures']) > 0:
            result['message'] = "Failed to properly supply the required fields"
            return Response(dumps(result), status=400, mimetype="application/json")
        DB.session.commit()
        result['success'] = True
        return Response(dumps(result), status=200, mimetype="application/json")

    def option(self):
        return {'Allow' : 'PUT' }, 200, \
                { 'Access-Control-Allow-Origin': '*', \
                 'Access-Control-Allow-Methods' : 'PUT,GET' }

class TeamListAPI(Resource):
    def get(self):
        """
            GET request for Teams List
            Route: /teams
            Parameters :

            Returns:
                status: 200 
                mimetype: application/json
                data: 
                    teams: [  {
                                    team_name: string, team_id: int,
                                    captain_id: int, sponsor_id: int,
                                    photo: int, color:string
                                    }
                                ,{...}
                                ]
        """
        # return a list of teams
        teams = Team.query.all()
        for i in range(0, len(teams)):
            teams[i] = teams[i].json()
        resp = Response(dumps(teams), status=200, mimetype="application/json")
        return resp

    def post(self):
        """
            POST request for Teams List
            Route: /teams
            Parameters :
                team_name: The team's name (string)
                captain_id: The captain player id (int)
                sponsor_id: The sponsor id (int)
                team_picture_id: The picture id (int)
                color: the color of the team (string)
            Returns:
                status: 200 
                mimetype: application/json
                data: 
                    success: tells if request was successful (boolean)
                    message: the status message (string)
                    failures: a list of parameters that failed (list of string)
                    team_id: the created user team id (int)
        """
        # create a new user
        result = {'team_id': None,
                  'success': False,
                  'message': '',
                  'failures':[]}
        args = parser.parse_args()
        color = None
        sponsor_id = None
        league_id = None
        
        if args['color'] and string_validator(args['color']):
            color = args['color']
        elif args['color'] and not string_validator(args['color']):
            result['failures'].append('Invalid color')
        else:
            result['failures'].append("Missing color")
        if args['sponsor_id']:
            sid = args['sponsor_id']
            sponsor = Sponsor.query.get(sid)
            if sponsor is None:
                result['failures'].append('Invalid sponsor ID')
            else:
                sponsor_id = sid
        if args['league_id']:
            lid = args['league_id']
            league = League.query.get(lid)
            if league is None:
                result['failures'].append('Invalid league ID')
            else:
                league_id = lid
        if len(result['failures']) > 0:
            result['message'] = "Failed to properly supply the required fields"
            return Response(dumps(result), status=400, mimetype="application/json")
        t = Team(color=color, sponsor_id=sponsor_id, league_id=league_id)
        DB.session.add(t)
        DB.session.commit()
        result['success'] = True
        result['team_id'] = t.id
        return Response(dumps(result), status=200, mimetype="application/json")

    def options (self):
        return {'Allow' : 'PUT' }, 200, \
                { 'Access-Control-Allow-Origin': '*', \
                 'Access-Control-Allow-Methods' : 'PUT,GET' }
