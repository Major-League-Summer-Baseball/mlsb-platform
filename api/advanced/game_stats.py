'''
@author: Dallas Fraser
@author: 2015-09-29
@organization: MLSB API
@summary: The views for game stats
'''
import unittest

from flask.ext.restful import Resource, reqparse
from flask import Response
from json import dumps
from api.validators import date_validator
from api import DB
from api.model import Team, Player, roster, Game, League, Bat
from datetime import datetime, date, time
parser = reqparse.RequestParser()
parser.add_argument('year', type=int)
parser.add_argument('league_id', type=int)
parser.add_argument('game_id', type=int)
class GameStatsAPI(Resource):
    def post(self):
        """
            POST request for Game Stats
            Route: Route['vgame']
            Parameters:
                year: the year  (int)
                league_id: the team id (int)
                game_id: the game id (int)
            Returns:
                status: 200 
                mimetype: application/json
                data: list of Players
        """
        args = parser.parse_args()
        if args['game_id']:
            games = DB.session.query(Game).filter_by(id = args['game_id'])
        else:
            if args['year']:
                year = args['year']
            else:
                year = None
            if args['league_id']:
                id = args['league_id']
            else:
                id = None
            t1 = time(0, 0)
            t2 = time(0 , 0)
            if year is not None:
                d1 = date(year, 1, 1)
                t1 = time(0, 0)
                d2 = date(year, 12, 30)
                t2 = time(0 , 0)
            else:
                d1 = date(2014, 1, 1)
                d2 = date(date.today().year, 12, 30)
            start = datetime.combine(d1, t1)
            end = datetime.combine(d2, t2)
            games = DB.session.query(Game).filter(Game.date.between(start, end))
            if id is not None:
                games = games.filter_by(league_id=id)
        result = []
        for game in games:
            aid = game.away_team_id
            hid = game.home_team_id
            g = {
                 'status': game.status,
                 'game_id': game.id,
                 'home_score':0,
                 'away_score': 0,
                 'home_bats': [],
                 'away_bats': [],
                 'home_team': None,
                 'away_team': None,
                 'date': game.date.strftime("%Y-%m-%d %H:%M"),
                 'league': League.query.get(game.league_id).json()}
            g['home_team'] = Team.query.get(hid).json()
            g['away_team'] = Team.query.get(aid).json()
            away_bats = Bat.query.filter_by(team_id=aid).all()
            home_bats = Bat.query.filter_by(team_id=hid).all()
            for bat in away_bats:
                p = Player.query.get(bat.player_id)
                g['away_bats'].append({'name': p.name,
                                       'hit': bat.classification,
                                       'inning': bat.inning,
                                       'rbi':bat.rbi})
                g['away_score'] += bat.rbi
            for bat in range(0, len(home_bats)):
                p = Player.query.get(home_bats[bat].player_id)
                g['home_bats'].append({'name': p.name,
                                       'hit': home_bats[bat].classification,
                                       'inning': home_bats[bat].inning,
                                       'rbi':home_bats[bat].rbi})
                g['home_score'] += home_bats[bat].rbi
            result.append(g)
        return Response(dumps(result), status=200, mimetype="application/json")
