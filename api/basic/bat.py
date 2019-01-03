'''
@author: Dallas Fraser
@date: 2016-04-12
@organization: MLSB API
@summary: The basic bat API
'''
from flask_restful import Resource, reqparse
from flask import Response
from api import DB
from api.model import Bat
from json import dumps
from api.authentication import requires_admin
from api.errors import BatDoesNotExist
from api.variables import PAGE_SIZE
from api.routes import Routes
from api.helper import pagination_response
from flask import request
parser = reqparse.RequestParser()
parser.add_argument('player_id', type=int)
parser.add_argument('rbi', type=int)
parser.add_argument('game_id', type=int)
parser.add_argument('hit', type=str)
parser.add_argument('inning', type=int)
parser.add_argument('team_id', type=str)
post_parser = reqparse.RequestParser(bundle_errors=True)
post_parser.add_argument('player_id', type=int, required=True)
post_parser.add_argument('rbi', type=int)
post_parser.add_argument('game_id', type=int, required=True)
post_parser.add_argument('hit', type=str, required=True)
post_parser.add_argument('inning', type=int)
post_parser.add_argument('team_id', type=str, required=True)


class BatAPI(Resource):
    def get(self, bat_id):
        """
            GET request for Bat Object matching given bat_id
            Route: Routes['bat']/<bat_id: int>
            Returns:
                if found
                    status: 200
                    mimetype: application/json
                    data:
                        {
                           'bat_id': int,
                           'game_id': int,
                           'team_id': int,
                           'team': string,
                           'rbi': int,
                           'hit': string,
                           'inning': int,
                           'player_id': int,
                           'player': string
                       }
                otherwise
                    status: 404
                    mimetype: application/json
                    data: None
        """
        entry = Bat.query.get(bat_id)
        if entry is None:
            raise BatDoesNotExist(payload={'details': bat_id})
        response = Response(dumps(entry.json()), status=200,
                            mimetype="application/json")
        return response

    @requires_admin
    def delete(self, bat_id):
        """
            DELETE request for Bat
            Route: Routes['bat']/<bat_id: int>
            Returns:
                status: 200
                mimetype: application/json
                data:
                    success: tells if request was successful (boolean)
                    message: the status message (string)
        """
        bat = Bat.query.get(bat_id)
        if bat is None:
            raise BatDoesNotExist(payload={'details': bat_id})
        # delete a single bat
        DB.session.delete(bat)
        DB.session.commit()
        response = Response(dumps(None),
                            status=200,
                            mimetype="application/json")
        return response

    @requires_admin
    def put(self, bat_id):
        """
            PUT request for Bat
            Route: Routes['bat']/<bat_id: int>
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
        args = parser.parse_args()
        bat = Bat.query.get(bat_id)
        player_id = None
        team_id = None
        game_id = None
        rbi = None
        hit = None
        inning = None
        if bat is None:
            raise BatDoesNotExist(payload={'details': bat_id})
        if args['team_id']:
            team_id = args['team_id']
        if args['game_id']:
            game_id = args['game_id']
        if args['player_id']:
            player_id = args['player_id']
        if args['rbi']:
            rbi = args['rbi']
        if args['hit']:
            hit = args['hit']
        if args['inning']:
            inning = args['inning']
        bat.update(player_id=player_id,
                   team_id=team_id,
                   game_id=game_id,
                   rbi=rbi,
                   hit=hit,
                   inning=inning)
        DB.session.commit()
        response = Response(dumps(None), status=200,
                            mimetype="application/json")
        return response

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}


class BatListAPI(Resource):
    def get(self):
        """
            GET request for Bats List
            Route: Routes['bat']
            Parameters :
            Returns:
                status: 200
                mimetype: application/json
                data:
                    games: [  {
                                'bat_id': int,
                               'game_id': int,
                               'team_id': int,
                               'team': string,
                               'rbi': int,
                               'hit': string,
                               'inning': int,
                               'player_id': int,
                               'player': string
                              }
                                ,{...}
                           ]
        """
        #  return a pagination of bats
        page = request.args.get('page', 1, type=int)
        pagination = Bat.query.paginate(page, PAGE_SIZE, False)
        result = pagination_response(pagination, Routes['bat'])
        resp = Response(dumps(result), status=200,
                        mimetype="application/json")
        return resp

    @requires_admin
    def post(self):
        """
            POST request for Bats List
            Route: Routes['bat']
            Parameters :
                game_id: the id of the game (int)
                player_id: the id of the batter (int)
                rbi: the number of runs batted in (int)
                hit: the type of hit (string)
                inning: the inning the hit occurred (int)
                team_id: the id of the team (int)
            Returns:
                if successful
                    status: 200
                    mimetype: application/json
                    data: the created bat id (int)
                otherwise possible errors
                    status: 400, GDNESC, PDNESC, TDNESC
                    mimetype: application/json
                    data: None
        """
        # create a new bat
        args = post_parser.parse_args()
        game_id = None
        player_id = None
        team_id = None
        rbi = 0
        hit = None
        inning = 1  # just assume some first inning
        if args['game_id']:
            game_id = args['game_id']
        if args['player_id']:
            player_id = args['player_id']
        if args['team_id']:
            team_id = args['team_id']
        if args['hit']:
            hit = args['hit']
        if args['rbi']:
            rbi = args['rbi']
        if args['inning']:
            inning = args['inning']
        bat = Bat(player_id,
                  team_id,
                  game_id,
                  hit,
                  inning=inning,
                  rbi=rbi)
        DB.session.add(bat)
        DB.session.commit()
        bat_id = bat.id
        resp = Response(dumps(bat_id), status=201, mimetype="application/json")
        return resp

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}
