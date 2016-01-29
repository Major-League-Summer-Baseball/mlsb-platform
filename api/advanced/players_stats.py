'''
@author: Dallas Fraser
@author: 2015-09-29
@organization: MLSB API
@summary: The views for player stats
'''
from sqlalchemy.sql.expression import or_
from flask.ext.restful import Resource, reqparse
from flask import Response
from json import dumps
from api import DB
from api.model import Player, Bat, Game
from datetime import datetime, date, time
parser = reqparse.RequestParser()
parser.add_argument('year', type=int)
parser.add_argument('league_id', type=int)
parser.add_argument('player_id', type=int)
parser.add_argument('team_id', type=int)

def post(year=None, team_id=None, league_id=None, player_id=None):
    if player_id is not None:
        bats = DB.session.query(Bat).filter_by(player_id = player_id)
        players = {}
        for bat in bats:
            if bat.player_id in players:
                players[bat.player_id][bat.classification] += 1
                players[bat.player_id]['bats'] += 1
            else:
                players[bat.player_id] = {'bats': 0,
                                          's': 0,
                                          'd': 0,
                                          'k': 0,
                                          'hr': 0,
                                          'go': 0,
                                          'pf': 0}
                players[bat.player_id][bat.classification] += 1
                players[bat.player_id]['bats'] += 1
    else:
        t1 = time(0, 0)
        t2 = time(0 , 0)
        if year is not None:
            d1 = date(year, 1, 1)
            d2 = date(year, 12, 30)
        else:
            d1 = date(2014, 1, 1)
            d2 = date(date.today().year, 12, 30)
        start = datetime.combine(d1, t1)
        end = datetime.combine(d2, t2)
        games = DB.session.query(Game).filter(Game.date.between(start, end))
        if league_id is not None:
            games = games.filter_by(league_id=league_id)
        if team_id is not None:
            games = games.filter(or_(Game.away_team_id == team_id, Game.home_team_id == team_id))
        players = {}
        for game in games:
            for bat in game.bats:
                player = Player.query.get(bat.player_id)
                if player.name in players:
                    players[player.name][bat.classification] += 1
                    players[player.name]['bats'] += 1
                else:
                    players[player.name] = {'bats': 0,
                                              's': 0,
                                              'd': 0,
                                              'k': 0,
                                              'hr': 0,
                                              'go': 0,
                                              'pf': 0}
                    players[player.name][bat.classification] += 1
                    players[player.name]['bats'] += 1
    for key, __ in players.items():
        players[key]['avg'] = (players[key]['s'] +\
                               players[key]['d'] +\
                               players[key]['hr']) / players[key]['bats']
    return players

class PlayerStatsAPI(Resource):
    def post(self):
        """
            POST request for Players Stats List
            Route: Route['player_stats']
            Parameters:
                year: the year  (int)
                team_id: the team id (int)
                league_id: the league id (int)
                player_id: the player id (int)
            Returns:
                status: 200 
                mimetype: application/json
                data: list of Players
        """
        year = None
        league_id = None
        player_id = None
        team_id = None
        args = parser.parse_args()
        if args['year']:
            year = args['year']
        if args['league_id']:
            league_id = args['league_id']
        if args['player_id']:
            player_id = args['player_id']
        if args['team_id']:
            team_id = args['team_id']
        players = post(year=year,
                      team_id=team_id,
                      league_id=league_id,
                      player_id=player_id)
        return Response(dumps(players), status=200, mimetype="application/json")
