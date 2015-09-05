'''
Name: Dallas Fraser
Date: 2014-07-31
Project: MLSB API
Purpose: To create an application to act as an api for the database
'''
from flask.ext.restful import Resource, reqparse
from flask import Response
from api.model import League
from json import dumps
from api.validators import string_validator
from api import DB

parser = reqparse.RequestParser()
parser.add_argument('league_name', type=str)

HEADERS = [{'header':'league_name', 'required':True, 
            'validator':string_validator},]

class LeagueAPI(Resource):
    def get(self, league_id):
        """
            GET request for League Object matching given league_id
            Route: /leagues/<league_id: int>
            Returns:
                status: 200 
                mimetype: application/json
                data: 
                    success: tells if request was successful (boolean)
                    message: the status message (string)
                    data:  {league_id:int, league_name:string}
        """
        # expose a single League
        result = {'success': False,
                  'message': '',
                  'failures':[]}
        entry  = League.query.get(league_id)
        if entry is None:
            result['message'] = 'Not a valid league ID'
            return Response(dumps(result), status=404,
                             mimetype="application/json")
        result['success'] = True
        result['data'] = entry.json()
        return Response(dumps(result), status=200, mimetype="application/json")


    def delete(self, league_id):
        """
            DELETE request for League
            Route: /leagues/<league_id:int>
            Returns:
                status: 200 
                mimetype: application/json
                data: 
                    success: tells if request was successful (boolean)
                    message: the status message (string)
        """
        result = {'success': False,
                  'message': '',}
        # delete a single user
        league = League.query.get(league_id)
        if league is None:
            result['message'] = "Not a valid league ID"
            return Response(dumps(result), status=404,
                            mimetype="application/json")
        DB.session.delete(league)
        DB.session.commit()
        result['success'] = True
        result['message'] = 'League was deleted'
        return Response(dumps(result), status=200, mimetype="application/json")


    def put(self, league_id):
        """
            PUT request for league
            Route: /leagues/<league_id:int>
            Parameters :
                league_name: The league's name (string)
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
        args = parser.parse_args()
        league = League.query.get(league_id)
        if league is None:
            result['message'] = 'Not a valid league ID'
            return Response(dumps(result), status=404,
                            mimetype="application/json")
        if args['league_name'] and string_validator(args['league_name']):
            league.name = args['league_name']
            result['success'] = True
            result['message'] = ""
            DB.session.commit()
        elif args['league_name'] and not string_validator(args['league_name']):
            result['failures'].append("Invalid league name")
        if len(result['failures']) > 0:
            result['message'] = "Failed to properly supply the required fields"
            return Response(dumps(result), status=400,
                        mimetype="application/json")
        
        return Response(dumps(result), status=200, mimetype="application/json")


    def options (self):
        return {'Allow' : 'PUT' }, 200, \
                { 'Access-Control-Allow-Origin': '*', \
                 'Access-Control-Allow-Methods' : 'PUT,GET' }

class LeagueListAPI(Resource):
    def get(self):
        """
            GET request for League List
            Route: /leagues
            Parameters :
                league_name: The league's name (string)
            Returns:
                status: 200 
                mimetype: application/json
                data: 
                    tournaments: [{league_id:int,
                                   league_name:string,
                              },{...}
                            ]
        """
        # return a list of leagues
        leagues = League.query.all()
        for i in range(0, len(leagues)):
            leagues[i] = leagues[i].json()
        resp = Response(dumps(leagues), status=200, mimetype="application/json")
        return resp

    def post(self):
        """
            POST request for League List
            Route: /leagues
            Parameters :
                tournament_name: The league's name (string)
            Returns:
                status: 200 
                mimetype: application/json
                data: 
                    success: tells if request was successful (boolean)
                    message: the status message (string)
                    failures: a list of parameters that failed (list of string)
                    league_id: the created user league id (int)
        """
        # create a new user
        result = {'success': False,
                  'message': '',
                  'failures': [],
                  'league_id': None}
        args = parser.parse_args()
        league_name = None
        if args['league_name'] and string_validator(args['league_name']):
            league_name = args['league_name']
        else:
            result['failures'].append("Invalid league name")
        if len(result['failures']) > 0:
            result['message'] = "Failed to properly supply the required fields"
            return Response(dumps(result), status=400,
                        mimetype="application/json")
        league= League(league_name)
        DB.session.add(league)
        DB.session.commit()
        result['league_id'] = league.id
        result['data'] = league.json()
        result['success'] = True
        return Response(dumps(result), status=200,
                        mimetype="application/json")

    def options (self):
        return {'Allow' : 'PUT' }, 200, \
                { 'Access-Control-Allow-Origin': '*', \
                 'Access-Control-Allow-Methods' : 'PUT,GET' }
