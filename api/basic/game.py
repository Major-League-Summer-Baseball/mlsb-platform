'''
@author: Dallas Fraser
@date: 2016-04-12
@organization: MLSB API
@summary: The basic game API
'''
from flask_restful import Resource, reqparse
from flask import Response, request
from json import dumps
from api import DB
from api.model import Game
from api.authentication import requires_admin
from api.errors import GameDoesNotExist
from api.variables import PAGE_SIZE
from api.routes import Routes
from api.helper import pagination_response
from api.cached_items import handle_table_change
from api.tables import Tables
parser = reqparse.RequestParser()
parser.add_argument('home_team_id', type=int)
parser.add_argument('away_team_id', type=int)
parser.add_argument('date', type=str)
parser.add_argument('time', type=str)
parser.add_argument('league_id', type=int)
parser.add_argument('division_id', type=int)
parser.add_argument('status', type=str)
parser.add_argument('field', type=str)

post_parser = reqparse.RequestParser(bundle_errors=True)
post_parser.add_argument('home_team_id', type=int, required=True)
post_parser.add_argument('away_team_id', type=int, required=True)
post_parser.add_argument('date', type=str, required=True)
post_parser.add_argument('time', type=str, required=True)
post_parser.add_argument('league_id', type=int, required=True)
post_parser.add_argument('division_id', type=int, required=True)
post_parser.add_argument('status', type=str)
post_parser.add_argument('field', type=str)


class GameAPI(Resource):
    def get(self, game_id):
        """
            GET request for Game Object matching given Game_id
            Route: Routes['game']/<game_id: int>
            Returns:
                if found
                    status: 200
                    mimetype: application/json
                    data:   {
                            home_team: string
                            home_team_id: int,
                            away_team: string
                            away_team_id: int,
                            date: string,
                            time: string,
                            league_id: int,
                            game_id: int,
                            status: string,
                            field: string
                               }
                otherwise
                    status: 404
                    mimetype: application/json
                    data:   None
        """
        # expose a single game
        entry = Game.query.get(game_id)
        if entry is None:
            raise GameDoesNotExist(payload={'details': game_id})
        response = Response(dumps(entry.json()), status=200,
                            mimetype="application/json")
        return response

    @requires_admin
    def delete(self, game_id):
        """
            DELETE request for Game
            Route: Routes['game']/<game_id: int>
            Returns:
                if found
                    status: 200
                    mimetype: application/json
                    data: None
                otherwise
                    status: 404
                    mimetype: application/json
                    data: None
        """
        game = Game.query.get(game_id)
        if game is None:
            raise GameDoesNotExist(payload={'details': game_id})
        DB.session.delete(game)
        DB.session.commit()
        response = Response(dumps(None), status=200,
                            mimetype="application/json")
        handle_table_change(Tables.GAME, item=game.json())
        return response

    @requires_admin
    def put(self, game_id):
        """
            PUT request for game
            Route: Routes['game']/<game_id: int>
            Parameters :
                home_team_id: The home team id (int)
                away_team_id: The away team id (int)
                date: The date of the game with the format YYYY-MM-DD (string)
                time: The time of the game in the format HH:MM (string)
                league_id: The league this game belongs to (int),
                status: the game's status (string)
                field: the game's field (string)
            Returns:
                if found and successful
                    status: 200
                    mimetype: application/json
                    data: None
                otherwise possible errors
                    status: 404, IFSC, TDNESC, LDNESC
                    mimetype: application/json
                    data: None
        """
        game = Game.query.get(game_id)
        args = parser.parse_args()
        if game is None:
            raise GameDoesNotExist(payload={'details': game_id})
        game.update(date=args.get('date', None),
                    time=args.get('time', None),
                    home_team_id=args.get('home_team_id', None),
                    away_team_id=args.get('away_team_id', None),
                    league_id=args.get('league_id', None),
                    division_id=args.get('division_id', None),
                    status=args.get('status', None),
                    field=args.get('field', None))
        DB.session.commit()
        response = Response(dumps(None), status=200,
                            mimetype="application/json")
        handle_table_change(Tables.GAME, item=game.json())
        return response

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}


class GameListAPI(Resource):
    def get(self):
        """
            GET request for Games List
            Route: Routes['game']
            Parameters :
            Returns:
                status: 200
                mimetype: application/json
                data:
                    games: [  {
                                home_team: string
                                home_team_id: int,
                                away_team: string
                                away_team_id: int,
                                date: string,
                                time: string,
                                league_id: int,
                                game_id: int,
                                status: string,
                                field: string
                              }
                                ,{...}
                           ]
        """
        # return a pagination of games
        page = request.args.get('page', 1, type=int)
        pagination = Game.query.paginate(page, PAGE_SIZE, False)
        result = pagination_response(pagination, Routes['game'])
        resp = Response(dumps(result), status=200,
                        mimetype="application/json")
        return resp

    @requires_admin
    def post(self):
        """
            POST request for Games List
            Route: Routes['game']
            Parameters :
                home_team_id: The home team id (int)
                away_team_id: The away team id (int)
                date: The date of the game with the format YYYY-MM-DD (string)
                time: The time of the game in the format HH:MM (string)
                league_id: The league this game belongs to (int)
                status: the game status (string)
                field: the field the game is being played on (string)
            Returns:
                if successful
                    status: 200
                    mimetype: application/json
                    data: the created game id (int)
        """
        # create a new game
        args = post_parser.parse_args()
        date = None
        time = None
        if args['date'] and args['time']:
            date = args['date']
            time = args['time']
        status = args.get('status') if args.get('status') is not None else ''
        field = args.get('field') if args.get('field') is not None else ''
        game = Game(date,
                    time,
                    args.get('home_team_id'),
                    args.get('away_team_id'),
                    args.get('league_id'),
                    args.get('division_id'),
                    status=status,
                    field=field)
        DB.session.add(game)
        DB.session.commit()
        result = game.id
        handle_table_change(Tables.GAME, item=game.json())
        return Response(dumps(result), status=201, mimetype="application/json")

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}
