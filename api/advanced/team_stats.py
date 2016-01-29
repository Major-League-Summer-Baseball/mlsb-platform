'''
@author: Dallas Fraser
@author: 2015-09-29
@organization: MLSB API
@summary: The views for player stats
'''
from flask.ext.restful import Resource, reqparse
from flask import Response
from json import dumps
from api import DB
from api.model import Team, Game
from api.variables import HITS
from datetime import datetime, date, time
parser = reqparse.RequestParser()
parser.add_argument('year', type=int)
parser.add_argument('league_id', type=int)
parser.add_argument('team_id', type=int)


def post(team_id, year, league_id):
    if team_id is not None:
        team = single_team(team_id)
    else:
        team = team_stats(year, league_id)
    return team

def single_team(team_id):
    away_games = DB.session.query(Game).filter_by(away_team_id = team_id)
    home_games = DB.session.query(Game).filter_by(home_team_id = team_id)
    team = {team_id: {'wins': 0,
                'losses': 0,
                'games': 0,
                'ties': 0,
                "away_wins": 0,
                "away_losses": 0,
                'home_wins': 0,
                'home_losses': 0,
                'runs_for': 0,
                "runs_against": 0,
                'hits_for': 0,
                'hits_allowed': 0}
            }
    for game in away_games:
        team_score = 0
        opponent_score = 0
        for bat in game.bats:
            if bat.team_id == team_id:
                team_score += bat.rbi
                if bat.classification in HITS:
                    team[team_id]['hits_for'] += 1
            else:
                opponent_score += bat.rbi
                if bat.classification in HITS:
                    team[team_id]['hits_allowed'] += 1
        if team_score > opponent_score:
            team[team_id]['wins'] += 1
            team[team_id]['away_wins'] += 1
        elif team_score < opponent_score:
            team[team_id]['losses'] += 1
            team[team_id]['away_losses'] += 1
        else:
            team[team_id]['ties'] += 1
        team[team_id]['runs_for'] += team_score
        team[team_id]['runs_against'] += opponent_score
    for game in home_games:
        team_score = 0
        opponent_score = 0
        for bat in game.bats:
            if bat.team_id == team_id:
                team_score += bat.rbi
                if bat.classification in HITS:
                    team[team_id]['hits_for'] += 1
            else:
                opponent_score += bat.rbi
                if bat.classification in HITS:
                    team[team_id]['hits_allowed'] += 1
        if team_score > opponent_score:
            team[team_id]['wins'] += 1
            team[team_id]['home_wins'] += 1
        elif team_score < opponent_score:
            team[team_id]['losses'] += 1
            team[team_id]['home_losses'] += 1
        else:
            team[team_id]['ties'] += 1
        team[team_id]['runs_for'] += team_score
        team[team_id]['runs_against'] += opponent_score
    return team

def team_stats(year, league_id):
    t1 = time(0, 0)
    t2 = time(0 , 0)
    if year is not None:
        d1 = date(year, 1, 1)
        t1 = time(0, 0)
        d2 = date(year, 12, 30)
        t2 = time(0 , 0)
        teams = DB.session.query(Team).filter(year=year)
    else:
        d1 = date(2014, 1, 1)
        d2 = date(date.today().year, 12, 30)
        teams = DB.session.query(Team)
    start = datetime.combine(d1, t1)
    end = datetime.combine(d2, t2)
    games = DB.session.query(Game).filter(Game.date.between(start, end))
    if id is not None and year is not None:
        games = games.filter_by(league_id=id, )
        teams = teams.filter_by(league_id=id)
    team = {}
    for t in teams:
        team[t.id] ={'wins': 0,
                    'losses': 0,
                    'games': 0,
                    'ties': 0,
                    "away_wins": 0,
                    "away_losses": 0,
                    'home_wins': 0,
                    'home_losses': 0,
                    'runs_for': 0,
                    "runs_against": 0,
                    'hits_for': 0,
                    'hits_allowed': 0}
    for game in games:
        home_score = 0
        away_score = 0
        for bat in game.bats:
            if bat.team_id == game.away_team_id:
                away_score += bat.rbi
                if bat.classification in HITS:
                    team[game.away_team_id]['hits_for'] += 1
                    team[game.home_team_id]['hits_allowed']
            else:
                home_score += bat.rbi
                if bat.classification in HITS:
                    team[game.home_team_id]['hits_for'] += 1
                    team[game.away_team_id]['hits_allowed'] += 1
                    team[bat.team_id]['hits_allowed'] += 1
        if away_score > home_score:
            team[game.away_team_id]['wins'] += 1
            team[game.away_team_id]['away_wins'] += 1
            team[game.home_team_id]['losses'] += 1
            team[game.home_team_id]['home_losses'] += 1
            
        elif away_score < home_score:
            team[game.home_team_id]['wins'] += 1
            team[game.home_team_id]['home_wins'] += 1
            team[game.away_team_id]['losses'] += 1
            team[game.away_team_id]['away_losses'] += 1
        else:
            team[game.home_team_id]['ties'] += 1
            team[game.away_team_id]['ties'] += 1
        team[game.home_team_id]['runs_for'] += away_score
        team[game.home_team_id]['runs_against'] += home_score
        team[game.away_team_id]['runs_for'] += home_score
        team[game.away_team_id]['runs_against'] += away_score
    return team

class TeamStatsAPI(Resource):
    def post(self):
        """
            GET request for Team Stats List
            Route: Route['player_stats']
            Parameters:
                year: the year  (int)
                team_id: the team id (int)
                league_id: the league id (int)
            Returns:
                status: 200 
                mimetype: application/json
                data: list of Teams
        """
        year = None
        id = None
        args = parser.parse_args()
        if args['team_id']:
            tid = args['team_id']
            team = post(tid, None, None)
        else:
            
            if args['year']:
                year = args['year']
            else:
                year = None
            if args['league_id']:
                league_id = args['league_id']
            else:
                league_id = None
            team = post(None, year, league_id)
        return Response(dumps(team), status=200, mimetype="application/json")