'''
@author: Dallas Fraser
@author: 2015-08-25
@organization: MLSB API
@summary: The basic player API
'''
from flask.ext.restful import Resource, reqparse
from flask import Response
from json import dumps
from api.model import Player
from api import DB
from api.validators import string_validator, gender_validator
parser = reqparse.RequestParser()
parser.add_argument('player_name', type=str)
parser.add_argument('gender', type=str)
parser.add_argument('email', type=str)
parser.add_argument('password', type=str)

#global parameters
HEADERS = [{'header':'player_name', 'required':True,
            'validator':""},
           {'header':'gender', 'required':True, 'validator':"gender_validator"}]

class PlayerAPI(Resource):
    
    def get(self, player_id):
        """
            GET request for Player List
            Route: /players/<player_id: int>
            Returns:
                status: 200 
                mimetype: application/json
                data: 
                    success: tells if request was successful (boolean)
                    message: the status message (string)
                    data:  {player_id:int, player-name:string, gender: string}
        """
        # expose a single user
        result = {'success': False,
                  'message': '',
                  'failures':[]}
        entry  = Player.query.get(player_id)
        if entry is None:
            result['message'] = 'Not a valid player ID'
            return Response(dumps(result), status=404, 
                            mimetype="application/json")
        result['success'] = True
        result['data'] = entry.json()
        return Response(dumps(result), status=200, mimetype="application/json")

    def delete(self, player_id):
        """
            DELETE request for Player
            Route: /players/<player_id:int>
            Returns:
                status: 200 
                mimetype: application/json
                data: 
                    success: tells if request was successful (boolean)
                    message: the status message (string)
        """
        result = {'success': False,
                  'message': '',}
        player = Player.query.get(player_id)
        if player is None:
            result['message'] = 'Not a valid player ID'
            return Response(dumps(result), status=404,
                            mimetype="application/json")
        # delete a single user
        DB.session.delete(player)
        DB.session.commit()
        result['success'] = True
        result['message'] = 'Player was deleted'
        return Response(dumps(result), status=200, mimetype="application/json")

    def put(self, player_id):
        """
            PUT request for Player
            Route: /players/<player_id:int>
            Parameters :
                player_name: The player's name (string)
                gender: a one letter character representing gender (string)
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
                  'failures': []}
        player = Player.query.get(player_id)
        args = parser.parse_args()
        if player is None:
            result['message'] = 'Not a valid player ID'
            return result
        if args['player_name'] and string_validator(args['player_name']):
            player.player_name = args['player_name']
        elif args['player_name'] and not string_validator(args['player_name']):
            result['failures'].append("Invalid player name")
        if args['gender'] and gender_validator(args['gender']):
            player.gender = args['gender']
        elif args['gender'] and not gender_validator(args['gender']):
            result['failures'].append("Invalid gender")
        if len(result['failures']) > 0:
            result['message'] = "Failed to properly supply the required fields"
            return Response(dumps(result), status=400, mimetype="application/json")
        DB.session.commit()
        result['success'] = True
        return Response(dumps(result), status=200, mimetype="application/json")

    def options (self):
        return {'Allow' : 'PUT' }, 200, \
                { 'Access-Control-Allow-Origin': '*', \
                 'Access-Control-Allow-Methods' : 'PUT,GET' }

class PlayerListAPI(Resource):
    def get(self):
        """
            GET request for Player List
            Route: /players
            Parameters :
                player_name: The player's name (string)
                gender: a one letter character representing gender (string)
            Returns:
                status: 200 
                mimetype: application/json
                data: 
                    players: [{player_id:int,
                              player-name:string,
                              gender: string},{}
                            ]
        """
        # return a list of users
        players = Player.query.all()
        for i in range(0, len(players)):
            players[i] = players[i].json()
        resp = Response(dumps(players), status=200, mimetype="application/json")
        return resp

    def post(self):
        """
            POST request for Player List
            Route: /players
            Parameters :
                player_name: The player's name (string)
                gender: a one letter character representing gender (string)
                email: the email of the player (string)
                password: the password of the player(string)
            Returns:
                status: 200 
                mimetype: application/json
                data: 
                    success: tells if request was successful (boolean)
                    message: the status message (string)
                    failures: a list of parameters that failed (list of string)
                    player_id: the created user player id (int)
        """
        # create a new user
        result = {'success': False,
                  'message': '',
                  'failures': [],
                  'player_id': None}
        args = parser.parse_args()
        gender = None
        player_name = None
        email = None
        password = None
        if args['player_name'] and string_validator(args['player_name']):
            player_name = args['player_name']
        else:
            result['failures'].append("Invalid player name")
        if args['gender'] and gender_validator(args['gender']):
            gender = args['gender']
        elif args['gender'] and not gender_validator(args['gender']):
            result['failures'].append("Invalid gender")
        if args['email'] and string_validator(args['email']):
            email = args['email']
        elif args['email'] and not string_validator(args['email']):
            result['failures'].append("Invalid email")
        if args['password'] and string_validator(args['password']):
            password = args['password']
        elif args['password'] and not string_validator(args['password']):
            result['failures'].append("Invalid password")
        if player_name is not None and len(result['failures']) <= 0:
            player = Player(player_name, email, gender, password)
            DB.session.add(player)
            DB.session.commit()
            result['player_id'] = player.id
            result['data'] = player.json()
            result['success'] = True
            return Response(dumps(result), status=200,
                        mimetype="application/json")
        else:
            result['message'] = "Failed to properly supply the required fields"
            return Response(dumps(result), status=400,
                        mimetype="application/json")

    def options (self):
        return {'Allow' : 'PUT' }, 200, \
                { 'Access-Control-Allow-Origin': '*', \
                 'Access-Control-Allow-Methods' : 'PUT,GET' }
