'''
Name: Dallas Fraser
Date: 2014-08-23
Project: MLSB API
Purpose: To create an application to act as an api for the database
'''
from flask.ext.restful import Resource, reqparse
from flask import Response
from json import dumps
from api import DB
from api.model import Game, Team, League
from api.validators import date_validator, time_validator
from sqlalchemy.ext.baked import Result
from datetime import datetime
parser = reqparse.RequestParser()
parser.add_argument('home_team_id', type=int)
parser.add_argument('away_team_id', type=int)
parser.add_argument('date', type=str)
parser.add_argument('time', type=str)
parser.add_argument('league_id', type=int)

class GameAPI(Resource):
    def get(self, game_id):
        """
            GET request for Game Object matching given Game_id
            Route: /games/<game_id: int>
            Returns:
                status: 200 
                mimetype: application/json
                data: 
                    success: tells if request was successful (boolean)
                    message: the status message (string)
                    data:  {
                            home_team_id: int, away_team_id: int,
                            date: string, time: string,
                            league_id: int, game_id: int
                           }
        """
        # expose a single game
        result = {'success': False,
                  'message': '',
                  'failures':[]}
        entry = Game.query.get(game_id)
        if entry is None:
            result['message'] = 'Not a valid game ID'
            return Response(dumps(result), status=404,
                            mimetype="application/json")
        result['success'] = True
        result['data'] = entry.json()
        return Response(dumps(result), status=200,
                        mimetype="application/json")

    def delete(self, game_id):
        """
            DELETE request for Game
            Route: /games/<game_id:int>
            Returns:
                status: 200 
                mimetype: application/json
                data: 
                    success: tells if request was successful (boolean)
                    message: the status message (string)
        """
        result = {'success': False,
                  'message': '',}
        game = Game.query.get(game_id)
        if game is None:
            result['message'] = 'Not a valid game ID'
            return Response(dumps(result), status=404,
                            mimetype="application/json")
        print(game)
        DB.session.delete(game)
        DB.session.commit()
        result['success'] = True
        result['message'] = "Game was deleted"
        return Response(dumps(result), status=200, mimetype="application/json")

    def put(self, game_id):
        """
            PUT request for game
            Route: /games/<game_id:int>
            Parameters :
                home_team_id: The home team id (int)
                away_team_id: The away team id (int)
                date: The date of the game with the format YYYY-MM-DD (string)
                time: The time of the game in the format HH:MM (string)
                league_id: The league this game belongs to (int)
            Returns:
                status: 200 
                mimetype: application/json
                data: 
                    success: tells if request was successful (boolean)
                    message: the status message (string)
                    failures: a list of parameters that failed to update 
                              (list of string)
        """
        result = {'success': False,
                  'message': '',
                  'failures': []}
        game = Game.query.get(game_id)
        args = parser.parse_args()
        if game is None:
            result['message'] = 'Invalid game ID'
            return result
        if args['home_team_id']:
            htid = args['home_team_id']
            if Team.query.get(htid) is None:
                result['failures'].append("Invalid home team ID")
            else:
                game.home_team_id = htid
        if args['away_team_id']:
            atid = args['away_team_id']
            if Team.query.get(atid) is None:
                result['failures'].append("Invalid away team ID")
            else:
                game.away_team_id = atid
        if args['date'] and args['time']:
            if date_validator(args['date']) and time_validator(args['time']):
                game.date = datetime.strptime(args['date'] + "-" +args['time'],
                                              '%Y-%m-%d-%H:%M')
            else:
                result['failures'].append("Invalid time & date")
        else:
            result['failures'].append('Invalid time & date')
        if args['league_id']:
            lid = args['league_id']
            if League.query.get(lid) is None:
                result['failures'].append("Invalid league ID")
            else:
                game.league_id = lid
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

class GameListAPI(Resource):
    def get(self):
        """
            GET request for Games List
            Route: /games
            Parameters :
            Returns:
                status: 200 
                mimetype: application/json
                data: 
                    games: [  {
                                    home_team_id: int, away_team_id: int,
                                    date: string, time: string,
                                    league_id: int, game_id: int
                              }
                                ,{...}
                           ]
        """
        # return a list of games
        games = Game.query.all()
        for i in range(0, len(games)):
            games[i] = games[i].json()
        resp = Response(dumps(games), status=200, mimetype="application/json")
        return resp


    def post(self):
        """
            POST request for Games List
            Route: /teams
            Parameters :
                home_team_id: The home team id (int)
                away_team_id: The away team id (int)
                date: The date of the game with the format YYYY-MM-DD (string)
                time: The time of the game in the format HH:MM (string)
                league_id: The tournament this game belongs to (int)
            Returns:
                status: 200 
                mimetype: application/json
                data: 
                    success: tells if request was successful (boolean)
                    message: the status message (string)
                    failures: a list of parameters that failed (list of string)
                    game_id: the created game id (int)
        """
        # create a new game
        result = {'success': False,
                  'message': '',
                  'failures': [],
                  'game_id': None}
        args = parser.parse_args()
        home_team_id = None
        away_team_id = None
        date = None
        time = None
        league_id = None
        if args['home_team_id']:
            htid = args['home_team_id']
            if Team.query.get(htid) is None:
                result['failures'].append("Invalid home team ID")
            else:
                home_team_id = htid
        else:
            result['failures'].append("Invalid home team ID")
        if args['away_team_id']:
            atid = args['away_team_id']
            if Team.query.get(atid) is None:
                result['failures'].append("Invalid away team ID")
            else:
                away_team_id = atid
        else:
            result['failures'].append("Invalid away team ID")
        if args['date'] and args['time']:
            if date_validator(args['date']) and time_validator(args['time']):
                date = datetime.strptime(args['date'] + "-" +args['time'],
                                              '%Y-%m-%d-%H:%M')
            else:
                result['failures'].append("Invalid time & date")
        else:
            result['failures'].append('Invalid time & date')
        if args['league_id']:
            lid = args['league_id']
            if League.query.get(lid) is None:
                result['failures'].append("Invalid league ID")
            else:
                league_id = lid
        else:
            result['failures'].append("Invalid league ID")
        if len(result['failures']) > 0:
            result['message'] = "Failed to properly supply the required fields"
            return Response(dumps(result), status=400, mimetype="application/json")
        game = Game(date, home_team_id, away_team_id, league_id)
        DB.session.add(game)
        DB.session.commit()
        result['success'] = True
        result['game_id'] = game.id
        return Response(dumps(result), status=200, mimetype="application/json")


    def option(self):
        return {'Allow' : 'PUT' }, 200, \
                { 'Access-Control-Allow-Origin': '*', \
                 'Access-Control-Allow-Methods' : 'PUT,GET' }
