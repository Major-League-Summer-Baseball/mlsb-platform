'''
@author: Dallas Fraser
@date: 2016-04-12
@organization: MLSB API
@summary: The views for game stats
'''
from flask_restful import Resource, reqparse
from flask import Response
from json import dumps
from api import DB
from api.model import Team, Player, Game, League, Bat, Division
from datetime import datetime, date, time, timedelta
parser = reqparse.RequestParser()
parser.add_argument('year', type=int)
parser.add_argument('league_id', type=int)
parser.add_argument('game_id', type=int)
parser.add_argument('division_id', type=int)


def post(
        game_id=None,
        league_id=None,
        division_id=None,
        year=None,
        today=False,
        increment=None):
    result = []
    if game_id is not None:
        games = DB.session.query(Game).filter_by(id=game_id)
    else:
        t1 = time(0, 0)
        t2 = time(23, 59)
        if year is not None:
            d1 = date(year, 1, 1)
            d2 = date(year, 12, 30)
        else:
            d1 = date(2014, 1, 1)
            d2 = date(date.today().year, 12, 30)
        if today:
            d1 = date.today() + timedelta(-2)
            d2 = date.today() + timedelta(2)
        if increment is not None:
            d1 = date.today() + timedelta(-increment)
            d2 = date.today() + timedelta(increment)
        start = datetime.combine(d1, t1)
        end = datetime.combine(d2, t2)
        games = (DB.session.query(Game)
                 .filter(Game.date.between(start, end))
                 .order_by(Game.date))
    if division_id is not None:
        games = games.filter_by(division_id=division_id)
    if league_id is not None:
        games = games.filter_by(league_id=league_id)
    for game in games:
        aid = game.away_team_id
        hid = game.home_team_id
        g = {
            'status': game.status,
            'game_id': game.id,
            'home_score': 0,
            'away_score': 0,
            'home_bats': [],
            'away_bats': [],
            'home_team': None,
            'away_team': None,
            'date': game.date.strftime("%Y-%m-%d %H:%M"),
            'league': League.query.get(game.league_id).json(),
            'division': Division.query.get(game.division_id).json()
        }
        g['home_team'] = Team.query.get(hid).json()
        g['away_team'] = Team.query.get(aid).json()
        away_bats = (DB.session.query(Bat,
                                      Player)
                     .join(Player)
                     .filter(Bat.team_id == aid)
                     .filter(Bat.game_id == game.id)
                     ).all()
        home_bats = (DB.session.query(Bat,
                                      Player)
                     .join(Player)
                     .filter(Bat.team_id == hid)
                     .filter(Bat.game_id == game.id)
                     ).all()
        for bat in away_bats:
            g['away_bats'].append({'name': bat[1].name,
                                   'hit': bat[0].classification,
                                   'inning': bat[0].inning,
                                   'rbi': bat[0].rbi,
                                   'bat_id': bat[0].id})
            g['away_score'] += bat[0].rbi
        for bat in home_bats:
            g['home_bats'].append({'name': bat[1].name,
                                   'hit': bat[0].classification,
                                   'inning': bat[0].inning,
                                   'rbi': bat[0].rbi,
                                   'bat_id': bat[0].id})
            g['home_score'] += bat[0].rbi
        if g['away_bats'] == 0:
            g['away_score'] = "--"
        if g['home_bats'] == 0:
            g['home_score'] = "--"
        result.append(g)
    return result


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
        game_id = None
        league_id = None
        division_id = None
        year = None
        if args['game_id']:
            game_id = args['game_id']
        if args['league_id']:
            league_id = args['league_id']
        if args['year']:
            year = args['year']
        if args['division_id']:
            division_id = args['division_id']
        result = post(game_id=game_id, league_id=league_id,
                      year=year, division_id=division_id)
        return Response(dumps(result), status=200, mimetype="application/json")
