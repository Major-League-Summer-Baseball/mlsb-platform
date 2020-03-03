'''
@author: Dallas Fraser
@since: 2020-02-29
@organization: MLSB API
@summary: Holds various cached items that allow API and website to speed up
'''
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.sql.expression import and_
from datetime import date, datetime, time
from api import cache, DB
from api.advanced.game_stats import post as game_summary
from api.model import Team, Sponsor, League, Espys, Fun, Sponsor, Game
from api.errors import LeagueDoesNotExist
from api.variables import LONG_TERM_CACHE
from api.advanced.team_stats import team_stats
from api.advanced.league_leaders import get_leaders,\
    get_leaders_not_grouped_by_team
from api.tables import Tables
from api.advanced.league_leaders import get_leaders,\
    get_leaders_not_grouped_by_team
from api.routes import Routes
from api.variables import PAGE_SIZE
from api.helper import pagination_response_items
import json


def handle_table_change(table_changed: 'Tables', item=None):
    """Update the appropriate caches given the following table has changed"""

    # base website data should change for most things
    if table_changed in [Tables.BAT, Tables.GAME, Tables.LEAGUE,
                         Tables.SPONSOR]:
        cache.delete_memoized(get_website_base_data)

    # league standings and schedule should only change if score is changed
    # or some of the game information changed
    if table_changed == Tables.BAT or table_changed == Tables.GAME:
        cache.delete_memoized(get_league_standings)
        cache.delete_memoized(get_league_schedule)
        cache.delete_memoized(get_upcoming_games)
        cache.delete_memoized(get_league_leaders)

    # team mape needs to change if either team or sponsor changes
    # since sponsor affects the team name
    if table_changed == Tables.SPONSOR or table_changed == Tables.TEAM:
        cache.delete_memoized(get_team_map)

    #  update league standings if esyps change
    # also update the esyps break down
    if table_changed == Tables.ESPYS:
        cache.delete_memoized(get_league_standings)
        cache.delete_memoized(get_espys_breakdown)

    if table_changed == Tables.SPONSOR:
        cache.delete_memoized(get_sponsor_map)

    # update the league mape if league changed
    if table_changed == Tables.LEAGUE:
        cache.delete_memoized(get_league_map)

    if table_changed == Tables.FUN:
        cache.delete_memoized(get_fun_counts)


@cache.memoize(timeout=LONG_TERM_CACHE)
def get_upcoming_games(year):
    """Returns the upcoming games and any scores from day before"""
    return game_summary(year=year, today=True, increment=1)


@cache.memoize(timeout=LONG_TERM_CACHE)
def get_fun_counts():
    return [fun.json() for fun in Fun.query.all()]


@cache.memoize(timeout=LONG_TERM_CACHE)
def get_sponsor_map():
    sponsor_map = {}
    for sponsor in Sponsor.query.all():
        sponsor_map[sponsor.id] = sponsor.json()
    return sponsor_map


@cache.memoize(timeout=LONG_TERM_CACHE)
def get_league_map():
    league_map = {}
    leagues = League.query.all()
    for league in leagues:
        league_map[league.id] = league.json()
    return league_map


@cache.memoize(timeout=LONG_TERM_CACHE)
def get_team_map():
    """Get a team map that maps team id to info about name and sponsor."""
    team_map = {}
    teams = Team.query.all()
    for team in teams:
        team_map[team.id] = {}
        team_map[team.id]['team_name'] = str(team)
        team_map[team.id]['sponsor_id'] = team.sponsor_id
        team_map[team.id]['sponsor_name'] = team.sponsor_name
    return team_map


@cache.memoize(timeout=LONG_TERM_CACHE)
def get_league_leaders(stat, year=None, group_by_team=False):
    """Get the league leaders for the given stat"""
    if group_by_team:
        return get_leaders_not_grouped_by_team(stat, year=year)
    else:
        return get_leaders(stat, year=year)


@cache.memoize(timeout=LONG_TERM_CACHE)
def get_league_schedule(year, league_id, page):
    """Get a page of the league schedule for the given league and year"""
    url_route = Routes['schedulecache'] + f"/{year}/{league_id}"
    return pull_schedule(year, league_id, page=page, url_route=url_route)


@cache.memoize(timeout=LONG_TERM_CACHE)
def get_league_standings(year, league_id):
    """Gets the league standings for the given league for some year."""
    league = get_league_map().get(league_id, None)
    if league is None:
        return None
    league['teams'] = []
    teams = team_stats(year, league['league_id'])
    for team in teams:
        valid_form = {'name': teams[team]['name'],
                      'id': team,
                      'espys': teams[team]['espys'],
                      'games': teams[team]['games'],
                      'wins': teams[team]['wins'],
                      'losses': teams[team]['losses'],
                      'ties': teams[team]['ties'],
                      'runs_for': teams[team]['runs_for'],
                      'runs_against': teams[team]['runs_against'],
                      'plus_minus': (teams[team]['runs_for'] -
                                     teams[team]['runs_against'])}
        league['teams'].append(valid_form)
    return league


@cache.memoize(timeout=LONG_TERM_CACHE)
def get_website_base_data(year):
    base = {}
    base['current_year'] = datetime.now().year
    base['games'] = get_upcoming_games(year)
    base['sponsors'] = [sponsor.json() for sponsor in DB.session.query(Sponsor)
                        .filter(Sponsor.active == True)
                        .order_by(Sponsor.name).all()]
    base['leagues'] = [league.json() for league in League.query.all()]
    fun_count = Fun.query.filter_by(year=year).first()
    if fun_count is None:
        fun_count = {'year': year, 'count': 0}
    else:
        fun_count = fun_count
    base['fun'] = fun_count
    base['today'] = datetime.now().strftime("%Y-%m-%d")
    return base


@cache.memoize(timeout=LONG_TERM_CACHE)
def get_espys_breakdown(year):
    teams = DB.session.query(Team).filter(Team.year == year).all()
    result = []
    total = func.sum(Espys.points).label('espys')
    t = time(0, 0)
    d1 = date(year, 1, 1)
    d2 = date(year, 12, 30)
    start = datetime.combine(d1, t)
    end = datetime.combine(d2, t)
    tree = {'name': "ESPYS Breakdown"}
    for team in teams:
        element = {}
        element['name'] = str(team)
        children_list = []
        espys = (DB.session.query(total, Sponsor.name, )
                 .outerjoin(Sponsor)
                 .filter(Espys.date.between(start, end))
                 .filter(Espys.team_id == team.id)
                 .group_by(Sponsor.name)).all()
        for espy in espys:
            point = {'name': 'Awarded ESPYS'}
            if espy[1] is not None:
                point['name'] = espy[1]
            point['size'] = espy[0]
            children_list.append(point)
        if len(children_list) == 0:
            element['size'] = 0
        else:
            element['children'] = children_list
        result.append(element)
    tree['children'] = result
    return json.dumps(tree)


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
