'''
@author: Dallas Fraser
@since: 2020-02-29
@organization: MLSB API
@summary: Holds various cached items that allow API and website to speed up
'''

from sqlalchemy import func
from sqlalchemy.orm import undefer
from sqlalchemy.sql.expression import and_, or_
from datetime import date, datetime, time
from api import cache, DB
from api.advanced.game_stats import post as game_summary
from api.model import Team, Sponsor, League, Espys, Fun, Game, Division
from api.errors import LeagueDoesNotExist
from api.variables import LONG_TERM_CACHE
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
        cache.delete_memoized(team_stats)
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
        cache.delete_memoized(team_stats)
        cache.delete_memoized(get_espys_breakdown)

    if table_changed == Tables.SPONSOR:
        cache.delete_memoized(get_sponsor_map)

    # update the league mape if league changed
    if table_changed == Tables.LEAGUE:
        cache.delete_memoized(get_league_map)
        cache.delete_memoized(get_divisions_for_league_and_year)

    if table_changed == Tables.FUN:
        cache.delete_memoized(get_fun_counts)

    if table_changed == Tables.GAME:
        cache.delete_memoized(get_divisions_for_league_and_year)


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
def get_divisions_for_league_and_year(year, league_id):
    """Get a list of divisions that associated with the league for that year"""
    if get_league_map().get(league_id, None) is None:
        raise LeagueDoesNotExist(payload={'details': league_id})
    start = datetime.combine(date(year, 1, 1), time(0, 0))
    end = datetime.combine(date(year, 12, 30), time(23, 0))
    division_ids = (DB.session.query(Division.id.distinct().label('id'))
                    .join(Game)
                    .filter(Game.league_id == league_id)
                    .filter(Game.date.between(start, end))).all()
    return [Division.query.get(division[0]).json()
            for division in division_ids]


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
    home_team = (
        "TBD"
        if game.home_team_id is None
        else team_mapper[game.home_team_id]['team_name']
    )
    away_team = (
        "TBD"
        if game.away_team_id is None
        else team_mapper[game.away_team_id]['team_name']
    )
    return {
        'game_id': game.id,
        'home_team_id': game.home_team_id,
        'home_team': home_team,
        'away_team_id': game.away_team_id,
        'away_team': away_team,
        'league_id': game.league_id,
        'division_id': game.division_id,
        'date': game.date.strftime("%Y-%m-%d"),
        'time': game.date.strftime("%H:%M"),
        'status': game.status,
        'field': game.field}


@cache.memoize(timeout=LONG_TERM_CACHE)
def team_stats(team_id, year, league_id, division_id=None):
    if team_id is not None:
        team = single_team(team_id)
    else:
        team = multiple_teams(year, league_id, division_id=division_id)
    return team


def single_team(team_id):
    team_query = Team.query.options(undefer('espys_total')).get(team_id)
    if team_query is None:
        return {}
    games = (DB.session.query(Game)
             .filter(or_(Game.away_team_id == team_id,
                         Game.home_team_id == team_id)
                     ).all())
    espy_total = (team_query.espys_total
                  if team_query.espys_total is not None else 0)
    team = {team_id: {'wins': 0,
                      'losses': 0,
                      'games': 0,
                      'ties': 0,
                      'runs_for': 0,
                      "runs_against": 0,
                      'hits_for': 0,
                      'hits_allowed': 0,
                      'name': str(team_query),
                      'espys': espy_total}
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


def filter_teams_by_map(result, team_map):
    """Returns copy of the result with only teams in the map"""
    new_result = {}
    for team_id in result.keys():
        if team_id in team_map.keys():
            new_result[team_id] = result[team_id]
    return new_result


def multiple_teams(year, league_id, division_id=None):
    t = time(0, 0)
    games = DB.session.query(Game)
    teams = DB.session.query(Team).options(undefer('espys_total'))
    team_map = {}
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
    if division_id is not None:
        games = games.filter(Game.division_id == division_id)
    result = {}
    for team in teams:
        # initialize each team
        espy_total = (team.espys_total
                      if team.espys_total is not None else 0)
        result[team.id] = {'wins': 0,
                           'losses': 0,
                           'games': 0,
                           'ties': 0,
                           'runs_for': 0,
                           "runs_against": 0,
                           'hits_for': 0,
                           'hits_allowed': 0,
                           'name': str(team),
                           'espys': espy_total}
    for game in games:
        # loop through each game (max ~400 for a season)
        if game.away_team_id is None or game.home_team_id is None:
            break
        team_map[game.home_team_id] = True
        team_map[game.away_team_id] = True
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
    if division_id is not None:
        result = filter_teams_by_map(result, team_map)
    return result
