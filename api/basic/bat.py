'''
Name: Dallas Fraser
Date: 2014-08-23
Project: MLSB API
Purpose: A Bat API
'''
from flask.ext.restful import Resource, reqparse
from flask import Response
from api import DB
from api.model import Team, Game, Bat, Player
from json import dumps
from api.validators import rbi_validator, hit_validator, inning_validator
parser = reqparse.RequestParser()
parser.add_argument('player_id', type=int)
parser.add_argument('rbi', type=int)
parser.add_argument('game_id', type=int)
parser.add_argument('hit', type=str)
parser.add_argument('inning', type=int)
parser.add_argument('team_id', type=str)


class BatAPI(Resource):
    def get(self, bat_id):
        """
            GET request for Bat Object matching given bat_id
            Route: /bats/<bat_id: int>
            Returns:
                status: 200
                mimetype: application/json
                data:
                    success: tells if request was successful (boolean)
                    message: the status message (string)
                    data:  {
                            game_id: int, player_id: int,
                            rbi: int, bat_id: int,
                            team_id: int, inning:int
                            hit: string,
                            }
        """
        # expose a single bat
        result = {'success': False,
                  'message': '',
                  'failures': []}
        entry = Bat.query.get(bat_id)
        if entry is None:
            result['message'] = 'Not a valid bat ID'
            return Response(dumps(result), status=404,
                            mimetype="application/json")
        result['success'] = True
        result['data'] = entry.json()
        return Response(dumps(result), status=200,
                        mimetype="application/json")

    def delete(self, bat_id):
        """
            DELETE request for Bat
            Route: /bats/<bat_id:int>
            Returns:
                status: 200
                mimetype: application/json
                data:
                    success: tells if request was successful (boolean)
                    message: the status message (string)
        """
        result = {'success': False,
                  'message': ''}
        bat = Bat.query.get(bat_id)
        if bat is None:
            result['message'] = 'Not a valid bat ID'
            return Response(dumps(result), status=404, mimetype="application/json")
        # delete a single bat
        DB.session.delete(bat)
        DB.session.commit()
        result['success'] = True
        result['message'] = 'Bat was deleted'
        return Response(dumps(result), status=200, mimetype="application/json")

    def put(self, bat_id):
        """
            PUT request for Bat
            Route: /bats/<bat_id:int>
            Parameters :
                game_id: the id of the game (int)
                player_id: the id of the batter (int)
                rbi: the number of runs batted in (int)
                hit: the type of hit (string)
                inning: the inning the hit occurred (int)
                team_id: the id of the team (int)
            Returns:
                status: 200
                mimetype: application/json
                data:
                    success: tells if request was successful (boolean)
                    message: the status message (string)
                    failures: a list of parameters that failed to update
                              (list of string)
        """
        # update a single bat
        result = {'success': False,
                  'message': '',
                  'failures': []}
        args = parser.parse_args()
        bat = Bat.query.get(bat_id)
        if bat is None:
            result['message'] = "Not a valid bat ID"
            return Response(dumps(result), status=404,
                            mimetype="application/json")
        if args['team_id']:
            tid = args['team_id']
            if Team.query.get(tid) is None:
                result['failures'].append('Invalid team ID')
            else:
                bat.team_id = tid
        if args['game_id']:
            gid = args['game_id']
            if Game.query.get(gid) is None:
                result['failures'].append('Invalid game ID')
            else:
                bat.game_id = gid
        if args['player_id']:
            pid = args['player_id']
            if Player.query.get(gid) is None:
                result['failures'].append('Invalid player ID')
            else:
                bat.player_id = gid
        if args['rbi']:
            if rbi_validator(args['rbi']):
                bat.rbi = args['rbi']
            else:
                result['failures'].append('Invalid rbi')
        if args['hit']:
            if hit_validator(args['hit']):
                bat.classificaiton = args['hit']
            else:
                result['failures'].append('Invalid hit')
        if args['inning']:
            if inning_validator(args['inning']):
                bat.inning = args['inning']
            else:
                result['failures'].append('Invalid inning')
        if len(result['failures']) > 0:
            result['message'] = "Failed to properly supply the required fields"
            return Response(dumps(result), status=400, mimetype="application/json")
        DB.session.commit()
        result['success'] = True
        return Response(dumps(result), status=200, mimetype="application/json")

    def option(self):
        return {'Allow': 'PUT'}, 200, \
            { 'Access-Control-Allow-Origin': '*', \
            'Access-Control-Allow-Methods': 'PUT,GET'}

class BatListAPI(Resource):
    def get(self):
        """
            GET request for Bats List
            Route: /bats
            Parameters :
            Returns:
                status: 200 
                mimetype: application/json
                data: 
                    games: [  {
                                    game_id: int, player_id: int,
                                    rbi: int, bat_id: int,
                                    hit: string, inning:int,
                                    team_id: int
                              }
                                ,{...}
                           ]
        """
        #  return a list of bats
        bats = Bat.query.all()
        for i in range(0, len(bats)):
            bats[i] = bats[i].json()
        resp = Response(dumps(bats), status=200, mimetype="application/json")
        return resp

    def post(self):
        """
            POST request for Bats List
            Route: /bats
            Parameters :
                game_id: the id of the game (int)
                player_id: the id of the batter (int)
                rbi: the number of runs batted in (int)
                hit: the type of hit (string)
            Returns:
                status: 200 
                mimetype: application/json
                data: 
                    success: tells if request was successful (boolean)
                    message: the status message (string)
                    failures: a list of parameters that failed (list of string)
                    bat_id: the created bat id (int)
        """
        # create a new batr
        result = {'success': False,
                  'message': '',
                  'failures': [],
                  'bat_id': None}
        args = parser.parse_args()
        game_id = None
        player_id = None
        team_id = None
        rbi = 0
        hit = None
        inning = 1 # just assume some first inning
        if args['game_id']:
            game_id = args['game_id']
            if Game.query.get(game_id) is None:
                result['failures'].append("Invalid game ID")
        else:
            result['failures'].append('Invalid game ID')
        if args['player_id']:
            player_id = args['player_id']
            if Player.query.get(player_id) is None:
                result['failures'].append("Invalid player ID")
        else:
            result['failures'].append("Invalid player ID")
        if args['team_id']:
            team_id = args['team_id']
            team = Team.query.get(team_id)
            if team is None:
                result['failures'].append('Invalid team ID')
        else:
            result['failures'].append("Invalid team ID")
        if args['hit']:
            if hit_validator(args['hit']):
                hit = args['hit']
            else:
                result['failures'].append('Invalid hit')
        else:
            result['failures'].append("Invalid hit")
        if args['rbi']:
            if rbi_validator(args['rbi']):
                rbi = args['rbi']
            else:
                result['failures'].append("Invalid rbi")
        if args['inning']:
            if inning_validator(args['inning']):
                inning = args['inning']
            else:
                result['failures'].append('Invalid inning')
        if len(result['failures']) > 0:
            result['message'] = "Failed to properly supply the required fields"
            return Response(dumps(result), status=400, mimetype="application/json")
        bat = Bat(player_id,
                  team_id,
                  game_id,
                  hit, inning, rbi)
        DB.session.add(bat)
        DB.session.commit()
        result['bat_id'] = bat.id
        result['success'] = True
        resp = Response(dumps(result), status=200, mimetype="application/json")
        return resp

    def option(self):
        return {'Allow' : 'PUT' }, 200, \
                { 'Access-Control-Allow-Origin': '*', \
                 'Access-Control-Allow-Methods' : 'PUT,GET' }
