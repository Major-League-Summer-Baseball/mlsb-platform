'''
@author: Dallas Fraser
@since: 2020-02-29
@organization: MLSB API
@summary: Holds various cached items that allow API and website to speed up
'''
from api.advanced.game_stats import post as game_summary
from api import cache, DB
from api.model import Team, Sponsor, League, Espys, Fun
from api.variables import LONG_TERM_CACHE
from api.advanced.league_leaders import get_leaders,\
    get_leaders_not_grouped_by_team
from api.tables import Tables
from datetime import datetime


def handle_table_change(table_changed: 'Tables', item=None):
    """Update the appropriate caches given the following table has changed"""
    if table_changed in [Tables.BAT, Tables.GAME, Tables.LEAGUE,
                         Tables.SPONSOR]:
        cache.delete_memoized(get_website_base_data)
    if table_changed == Tables.BAT or table_changed == Tables.GAME:
        cache.delete_memoized(get_league_standings)
        cache.delete_memoized(get_league_schedule)
    if table_changed == Tables.SPONSOR or table_changed == Tables.TEAM:
        cache.delete_memoized(get_team_map)
    if table_changed == Tables.ESPYS:
        cache.delete_memoized(get_league_standings)
        cache.delete_memoized(get_espys_breakdown)
    if table_changed == Tables.LEAGUE:
        cache.delete_memoized(get_league_map)


@cache.memoize(timeout=LONG_TERM_CACHE)
def get_fun_counts():
    return [fun.json() for fun in Fun.query.all()]


@cache.memoize(timeout=LONG_TERM_CACHE)
def get_league_map():
    print("Getting league map")
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
def get_league_schedule(year, league_id, page):
    """Get a page of the league schedule for the given league and year"""
    url_route = Routes['schedulecache'] + f"/{year}/{league_id}"
    return pull_schedule(year, league_id, page=page, url_route=url_route)


@cache.memoize(timeout=LONG_TERM_CACHE)
def get_league_standings(year, legaue_id):
    """Gets the league standings for the given league for some year."""
    team_map = {}
    teams = Team.query.all()
    for team in teams:
        team_map[team.id] = {}
        team_map[team.id]['team_name'] = str(team)
        team_map[team.id]['sponsor_id'] = team.sponsor_id
        team_map[team.id]['sponsor_name'] = team.sponsor_name
    return team_map


@cache.memoize(timeout=LONG_TERM_CACHE)
def get_website_base_data():
    base = {}
    base['current_year'] = datetime.now().year
    base['games'] = game_summary(year=year, today=True, increment=1)
    base['sponsors'] = [sponsor.json for sponsor in DB.session.query(Sponsor)
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
