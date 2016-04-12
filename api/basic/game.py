'''
@author: Dallas Fraser
@date: 2016-04-12
@organization: MLSB API
@summary: The basic game API
'''
from flask.ext.restful import Resource, reqparse
from flask import Response
from json import dumps
from api import DB
from api.model import Game
from api.authentication import requires_admin
parser = reqparse.RequestParser()
parser.add_argument('home_team_id', type=int)
parser.add_argument('away_team_id', type=int)
parser.add_argument('date', type=str)
parser.add_argument('time', type=str)
parser.add_argument('league_id', type=int)
parser.add_argument('status', type=str)
parser.add_argument('field', type=str)

post_parser = reqparse.RequestParser(bundle_errors=True)
post_parser.add_argument('home_team_id', type=int, required=True)
post_parser.add_argument('away_team_id', type=int, required=True)
post_parser.add_argument('date', type=str, required=True)
post_parser.add_argument('time', type=str, required=True)
post_parser.add_argument('league_id', type=int, required=True)
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
        response = Response(dumps(None), status=404,
                            mimetype="application/json")
        entry = Game.query.get(game_id)
        if entry is not None:
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
        response = Response(dumps(None), status=404,
                            mimetype="application/json")
        game = Game.query.get(game_id)
        if game is not None:
            DB.session.delete(game)
            DB.session.commit()
            response = Response(dumps(None), status=200,
                                mimetype="application/json")
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
        response = Response(dumps(None), status=404,
                            mimetype="application/json")
        game = Game.query.get(game_id)
        args = parser.parse_args()
        home_team_id = None
        away_team_id = None
        league_id = None
        date = None
        time = None
        field = None
        status = None
        if game is not None:
            if args['home_team_id']:
                home_team_id = args['home_team_id']
            if args['away_team_id']:
                away_team_id = args['away_team_id']
            if args['date']:
                date = args['date']
            if args['time']:
                time = args['time']
    
            if args['field']:
                field = args['field']
            if args['status']:
                status = args['status']
            if args['league_id']:
                league_id = args['league_id']
            game.update(date=date,
                        time=time,
                        home_team_id=home_team_id,
                        away_team_id=away_team_id,
                        league_id=league_id,
                        status=status,
                        field=field)
            DB.session.commit()
            response = Response(dumps(None), status=200,
                                mimetype="application/json")
        return response

    def option(self):
        return {'Allow' : 'PUT' }, 200, \
                { 'Access-Control-Allow-Origin': '*', \
                 'Access-Control-Allow-Methods' : 'PUT,GET' }

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
        # return a list of games
        games = Game.query.all()
        result = []
        for i in range(0, len(games)):
            result.append(games[i].json())
        resp = Response(dumps(result), status=200, mimetype="application/json")
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
        home_team_id = None
        away_team_id = None
        date = None
        time = None
        league_id = None
        status = ""
        field = ""
        if args['home_team_id']:
            home_team_id = args['home_team_id']
        if args['away_team_id']:
            away_team_id = args['away_team_id']
        if args['date'] and args['time']:
            date = args['date']
            time = args['time']
        if args['league_id']:
            league_id = args['league_id']
        if args['status']:
            status = args['status']
        if args['field']:
            field = args['field']
        game = Game(date,
                    time,
                    home_team_id,
                    away_team_id,
                    league_id,
                    status=status,
                    field=field)
        DB.session.add(game)
        DB.session.commit()
        result = game.id
        return Response(dumps(result), status=200, mimetype="application/json")

    def option(self):
        return {'Allow' : 'PUT' }, 200, \
                { 'Access-Control-Allow-Origin': '*', \
                 'Access-Control-Allow-Methods' : 'PUT,GET' }
