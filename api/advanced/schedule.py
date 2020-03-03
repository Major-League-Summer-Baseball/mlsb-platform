'''
@author: Dallas Fraser
@date: 2019-03-11
@organization: MLSB API
@summary: The views for game schedule
'''
from sqlalchemy.sql.expression import and_
from datetime import datetime, date, time
from flask_restful import Resource, request
from api.model import Game
from api.errors import LeagueDoesNotExist
from api.routes import Routes
from api.cached_items import get_team_map, get_league_map
from api.helper import pagination_response_items
from api.variables import PAGE_SIZE


def pull_schedule(year, league_id, page=1, page_size=PAGE_SIZE,
                  url_route=None):
    """Pull the schedule for the given league and year"""
    team_mapper = get_team_map()
    if league_id not in get_league_map().keys():
        raise LeagueDoesNotExist(payload={'details': league_id})
    start = datetime.combine(date(year, 1, 1), time(0, 0))
    end = datetime.combine(date(year, 12, 30), time(23, 0))
    games = (Game.query.filter(and_(Game.league_id == league_id,
                                    Game.date.between(start, end)))
             ).order_by("date").paginate(page, PAGE_SIZE, False)
    data = []
    for game in games.items:
        result = game_to_json(game, team_mapper)
        if game.date.date() <= datetime.today().date():
            scores = game.summary()
            result['score'] = (str(scores['home_score']) + '-' +
                               str(scores['away_score']))
        else:
            result['score'] = ""
        data.append(result)
    if url_route is None:
        url_route = (Routes['vschedule'] + "/" + str(year) + "/" +
                     str(league_id))
    return pagination_response_items(games, url_route, data)


def game_to_json(game, team_mapper):
    return {
        'game_id': game.id,
        'home_team_id': game.home_team_id,
        'home_team': team_mapper[game.home_team_id]['team_name'],
        'away_team_id': game.away_team_id,
        'away_team': team_mapper[game.away_team_id]['team_name'],
        'league_id': game.league_id,
        'division_id': game.division_id,
        'date': game.date.strftime("%Y-%m-%d"),
        'time': game.date.strftime("%H:%M"),
        'status': game.status,
        'field': game.field}


class ScheduleAPI(Resource):

    def get(self, year, league_id):
        """
            Get request for schedule data
            Route: Route['vschedule']/<int:year>/<int:team_id>
            Parameters:
                year: the year to get the schedule for
                league_id: the id of the league
            Returns:
                status: 200
                mimetype: application/json
                data: [
                        {
                            "away_team_id": int,
                            "away_team": str,
                            "date": str,
                            "field": str,
                            "home_team_id": int,
                            "home_team": str,
                            "league_id": int,
                            "score": str(home team - away team),
                            "status": str,
                            "time": str
                        }
                    ]
        """
        page = request.args.get('page', 1, type=int)
        return pull_schedule(year, league_id, page=page)
