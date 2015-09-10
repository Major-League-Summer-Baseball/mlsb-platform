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
delete_parser = reqparse.RequestParser()
delete_parser.add_argument("player_id", type=int, location="args")
delete_parser.add_argument("team_id", type=int, location="args")
parser.add_argument('player_id', type=int, )
parser.add_argument('team_id', type=int)
parser.add_argument('tournament_id', type=int)
parser.add_argument('start_date', type=str)
parser.add_argument('end_date', type=str)


class TeamRosterAPI(Resource):
    def get(self):
        """
            GET request for Team Roster List
            Route: /team_roster
            Returns:
                status: 200 
                mimetype: application/json
                data: {
                         player_id: int,
                         team_id: int,
                         start_date: string
                         end_date: string
                         tournament_id: int
                     }
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
        pass

    def post(self):
        """
            POST request for Team Roster List
            Route: /team_roster
            Parameters :
                player_id: a player's identifier (int)
                team_id: a team identifier (int)
                tournament_id: the tournament identifier (int)
                start_date: when the player started playing (string)
            Returns:
                status: 200 
                mimetype: application/json
                data: 
                    success: tells if request was successful (boolean)
                    message: the status message (string)
                    failures: a list of parameters that failed (list of string)
        """
        pass

    def option(self):
        return {'Allow': 'PUT'}, 200, \
            { 'Access-Control-Allow-Origin': '*', \
            'Access-Control-Allow-Methods': 'PUT,GET'}

