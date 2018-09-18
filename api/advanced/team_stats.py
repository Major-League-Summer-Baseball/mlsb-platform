'''
@author: Dallas Fraser
@author: 2016-04-12
@organization: MLSB API
@summary: The views for player stats
'''
from flask.ext.restful import Resource, reqparse
from flask import Response
from json import dumps
from api import DB
from api.model import Team, Game
from datetime import datetime, date, time
from sqlalchemy import or_
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
    team_query = Team.query.get(team_id)
    if team_query is None:
        return {}
    games = (DB.session.query(Game)
             .filter(or_(Game.away_team_id == team_id,
                         Game.home_team_id == team_id)
                     ).all())
    team = {team_id: {'wins': 0,
                      'losses': 0,
                      'games': 0,
                      'ties': 0,
                      'runs_for': 0,
                      "runs_against": 0,
                      'hits_for': 0,
                      'hits_allowed': 0,
                      'name': str(team_query)}
            }
    for game in games:
        # loop through each game
        scores = game.summary()
        if game.away_team_id == team_id:
            score = scores['away_score']
            hits = scores['away_bats']
            opp = scores['home_score']
            opp_hits = scores['home_bats']
        else:
            score = scores['home_score']
            hits = scores['home_bats']
            opp = scores['away_score']
            opp_hits = scores['away_bats']
        if score > opp:
            team[team_id]['wins'] += 1
        elif score < opp:
            team[team_id]['losses'] += 1
        elif scores['home_bats'] + scores['away_bats'] > 0:
            team[team_id]['ties'] += 1
        team[team_id]['runs_for'] += score
        team[team_id]['runs_against'] += opp
        team[team_id]['hits_for'] += hits
        team[team_id]['hits_allowed'] += opp_hits
        team[team_id]['games'] += 1
    return team


def team_stats(year, league_id):
    t = time(0, 0)
    games = DB.session.query(Game)
    teams = DB.session.query(Team)
    if year is not None:
        d1 = date(year, 1, 1)
        d2 = date(year, 12, 30)
        start = datetime.combine(d1, t)
        end = datetime.combine(d2, t)
        games = games.filter(Game.date.between(start, end))
        teams = teams.filter(Team.year == year)
    if league_id is not None:
        games = games.filter(Game.league_id == league_id)
        teams = teams.filter(Team.league_id == league_id)
    result = {}
    for team in teams:
        # initialize each team
        result[team.id] = {'wins': 0,
                           'losses': 0,
                           'games': 0,
                           'ties': 0,
                           'runs_for': 0,
                           "runs_against": 0,
                           'hits_for': 0,
                           'hits_allowed': 0,
                           'name': str(team)}
    for game in games:
        # loop through each game (max ~400 for a season)
        score = game.summary()
        result[game.away_team_id]['runs_for'] += score['away_score']
        result[game.away_team_id]['runs_against'] += score['home_score']
        result[game.away_team_id]['hits_for'] += score['away_bats']
        result[game.away_team_id]['hits_allowed'] += score['home_bats']
        result[game.home_team_id]['runs_for'] += score['home_score']
        result[game.home_team_id]['runs_against'] += score['away_score']
        result[game.home_team_id]['hits_for'] += score['home_bats']
        result[game.home_team_id]['hits_allowed'] += score['away_bats']
        if score['away_bats'] + score['home_bats'] > 0:
            result[game.away_team_id]['games'] += 1
            result[game.home_team_id]['games'] += 1
        if score['away_score'] > score['home_score']:
            result[game.away_team_id]['wins'] += 1
            result[game.home_team_id]['losses'] += 1
        elif score['away_score'] < score['home_score']:
            result[game.home_team_id]['wins'] += 1
            result[game.away_team_id]['losses'] += 1
        elif score['away_bats'] + score['home_bats'] > 0:
            result[game.home_team_id]['ties'] += 1
            result[game.away_team_id]['ties'] += 1
    return result


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
        return Response(dumps(team),
                        status=200,
                        mimetype="application/json")
