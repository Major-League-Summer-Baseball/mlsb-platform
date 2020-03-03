'''
@author: Dallas Fraser
@since: 2016-04-12
@organization: MLSB API
@summary: Holds the the views for the website
'''
from flask import render_template, url_for, send_from_directory, \
    redirect, request
from sqlalchemy.sql import func
from datetime import date, datetime
from api import app, PICTURES, POSTS, DB
from api.model import Team, Player, Sponsor, League, Espys
from api.variables import EVENTS, NOTFOUND
from api.routes import Routes
from api.advanced.team_stats import single_team
from api.advanced.players_stats import post as player_summary
from api.cached_items import get_league_map, get_team_map, get_sponsor_map,\
    get_league_standings, get_league_schedule, get_league_leaders,\
    get_espys_breakdown, get_upcoming_games
from api.cached_items import get_website_base_data as base_data
import os.path
import json

'''
# -----------------------------------------------------------------------------
#             POST PAGES ISSUES
# -----------------------------------------------------------------------------
'''


@app.route(Routes['posts'] + "/<int:year>")
def posts_json(year):
    return json.dumps(get_all_descriptions(year))


@app.route(Routes['posts'] + "/<int:year>/<date>/<file_name>/plain")
def checkout_post_raw_html(year, date, file_name):
    result = ""
    file_name = date + "_" + file_name
    if file_name.endswith(".html"):
        result = post_raw_html(file_name, year)
    return result


@app.route(Routes['posts'] + "/<int:year>/<date>/<file_name>/json")
def checkout_post_json(year, date, file_name):
    file_name = date + "_" + file_name
    result = {}
    if file_name.endswith(".html"):
        result = post_json(file_name, year)
    return json.dumps(result)


@app.route(Routes['posts'] + "/<int:year>/<date>/<file_name>")
def checkout_post(year, date, file_name):
    file_name = date + "_" + file_name
    template = "/".join(["website", "posts", str(year), file_name])
    if template.endswith(".html"):
        return render_template(template,
                               route=Routes,
                               base=base_data(year),
                               title="Posts",
                               year=year,
                               games=get_upcoming_games(year))
    else:
        return render_template("website/notFound.html",
                               route=Routes,
                               base=base_data(year),
                               title="Posts not Found",
                               year=year,
                               games=get_upcoming_games(year))


'''
# -----------------------------------------------------------------------------
#             POST PAGES ISSUES
# -----------------------------------------------------------------------------
'''


@app.route("/")
@app.route(Routes["homepage"])
@app.route("/website")
@app.route("/website/")
def reroute():
    year = date.today().year
    return redirect(url_for("index", year=year))


@app.route("/about/<int:year>")
def about(year):
    return render_template("website/about.html",
                           route=Routes,
                           base=base_data(year),
                           title="About",
                           year=year,
                           games=get_upcoming_games(year)
                           )


@app.route(Routes["homepage"] + "/<int:year>")
def index(year):
    games = get_upcoming_games(year)
    news = get_summaries(year)
    return render_template("website/index.html",
                           route=Routes,
                           base=base_data(year),
                           title="Recent news",
                           year=year,
                           games=games,
                           news=news)


@app.route(Routes['sponsorspicture'] + "/<int:name>")
@app.route(Routes['sponsorspicture'] + "/<name>")
def sponsor_picture(name):
    name = "notFound"
    if isinstance(name, int):
        sponsor_id = int(name)
        sponsor = get_sponsor_map().get(sponsor_id, None)
        if sponsor is not None:
            name = sponsor['sponsor_name']
    name = name.lower().replace(" ", "_") + ".png"
    f = os.path.join(PICTURES, "sponsors", name)
    fp = os.path.join(PICTURES, "sponsors")
    if os.path.isfile(f):
        return send_from_directory(fp, filename=name)
    else:
        return send_from_directory(fp, filename=NOTFOUND)


@app.route(Routes["logo"])
def mlsb_logo():
    fp = os.path.dirname(PICTURES)
    return send_from_directory(fp, filename="banner.png")


@app.route(Routes['teampicture'] + "/<int:team>")
@app.route(Routes['teampicture'] + "/<team>")
def team_picture(team):
    name = team if team is not None and team != "None" else "notFound"
    if isinstance(team, int):
        team_id = int(team)
        team = get_team_map().get(team_id, None)
        if team is not None and team['sponsor_name'] is not None:
            name = team['sponsor_name']
        else:
            name = "notFound"
    name = name.lower().replace(" ", "_") + ".png"
    f = os.path.join(PICTURES, "sponsors", name)
    fp = os.path.join(PICTURES, "sponsors")
    if os.path.isfile(f):
        return send_from_directory(fp, filename=name)
    else:
        return send_from_directory(fp, filename=NOTFOUND)


@app.route(Routes['postpicture'] + "/<name>")
def post_picture(name):
    f = os.path.join(PICTURES, "posts", name)
    fp = os.path.join(PICTURES, "posts")
    if os.path.isfile(f):
        return send_from_directory(fp, filename=name)
    else:
        return send_from_directory(fp, filename=NOTFOUND)


@app.route(Routes['sponsorspage'] + "/<int:year>")
def sponsors_page(year):
    return render_template("website/sponsors.html",
                           route=Routes,
                           base=base_data(year),
                           title="Sponsors",
                           year=year)


@app.route(Routes['sponsorspage'] + "/<int:year>" + "/<int:sponsor_id>")
def sponsor_page(year, sponsor_id):
    sponsor = get_sponsor_map().get(sponsor_id, None)
    if sponsor is None:
        page = render_template("website/notFound.html",
                               route=Routes,
                               base=base_data(year),
                               title="Not Found",
                               year=year)
    else:
        page = render_template("website/sponsor.html",
                               route=Routes,
                               base=base_data(year),
                               sponsor=sponsor,
                               title="Sponsor | " + sponsor.get('sponsor_name',
                                                                'No Name'),
                               year=year)
    return page


@app.route(Routes['leaguenotfoundpage'] + "<int:year>")
def league_not_found(year):
    return render_template("website/leagueNotFound.html",
                           route=Routes,
                           base=base_data(year),
                           title="League not found",
                           year=year)


@app.route(Routes["schedulepage"] + "/<int:league_id>/<int:year>")
def schedule(league_id, year):
    league = get_league_map().get(league_id, None)
    if league is None:
        return redirect(url_for("league_not_found", year=year))
    return render_template("website/schedule.html",
                           route=Routes,
                           base=base_data(year),
                           title="Schedule",
                           league=league,
                           year=year)


@app.route(Routes['standingspage'] + "/<int:league_id>/<int:year>")
def standings(league_id, year):
    league_standings = get_league_standings(league_id, year)
    if league_standings is None:
        return redirect(url_for("league_not_found", year=year))
    return render_template("website/standings.html",
                           route=Routes,
                           base=base_data(year),
                           league=league_standings,
                           title="Standings",
                           year=year)


@app.route(Routes['statspage'] + "/<int:year>")
def stats_page(year):
    players = player_summary(year=year)
    return render_template("website/stats.html",
                           route=Routes,
                           base=base_data(year),
                           title="Players Stats",
                           year=year,
                           players=players
                           )


@app.route(Routes['teampage'] + "/<int:year>/<int:team_id>")
def team_page(year, team_id):
    team = get_team(year, team_id)
    if team is not None:
        return render_template("website/team.html",
                               route=Routes,
                               base=base_data(year),
                               team=team,
                               title="Team - " + str(team['name']),
                               year=year)
    else:
        return render_template("website/notFound.html",
                               route=Routes,
                               base=base_data(year),
                               team=team,
                               title="Team not found",
                               year=year)


@app.route(Routes['playerpage'] + "/<int:year>/<int:player_id>")
def player_page(year, player_id):
    player = Player.query.get(player_id)
    if player is None:
        return render_template("website/notFound.html",
                               route=Routes,
                               base=base_data(year),
                               title="Player not found",
                               year=year)
    name = player.name
    years = []
    for team in player.teams:
        years.append((team.year, team.id))
    stats = []
    for entry in years:
        player = {}
        summary = player_summary(year=entry[0],
                                 team_id=entry[1],
                                 player_id=player_id)
        if name in summary:
            player = summary[name]
        else:
            player = {
                's': 0,
                'd': 0,
                'hr': 0,
                'ss': 0,
                'k': 0,
                'fo': 0,
                'fc': 0,
                'e': 0,
                'go': 0,
                'id': player_id,
                'rbi': 0,
                'avg': 0.000,
                'bats': 0
            }
        player['team'] = str(Team.query.get(entry[1]))
        player['team_id'] = entry[1]
        player['year'] = entry[0]
        stats.append(player)
    return render_template("website/player.html",
                           route=Routes,
                           base=base_data(year),
                           stats=stats,
                           title="Player Stats",
                           name=name,
                           year=year)


@app.route(Routes['leagueleaderpage'] + "/<int:year>")
def leaders_page(year):
    women = get_league_leaders("ss", year=year)[:5]
    men = get_league_leaders("hr", year=year)[:5]
    return render_template("website/new-leaders.html",
                           route=Routes,
                           base=base_data(year),
                           men=men,
                           women=women,
                           title="League Leaders",
                           year=year)


@app.route(Routes['schedulecache'] + "/<int:year>/<int:league_id>")
def cache_schedule_page(year, league_id):
    page = int(request.args.get('page', 1))
    return get_league_schedule(year, league_id, page)


@app.route(Routes['alltimeleaderspage'] + "/<int:year>")
def all_time_leaders_page(year):
    hrSingleSeason = get_league_leaders("hr")
    ssSingleSeason = get_league_leaders("ss")
    hrAllSeason = get_league_leaders("hr", group_by_team=True)
    ssAllSeason = get_league_leaders("ss", group_by_team=True)
    return render_template("website/all-time-leaders.html",
                           route=Routes,
                           base=base_data(year),
                           hrSingleSeason=hrSingleSeason,
                           ssSingleSeason=ssSingleSeason,
                           hrAllSeason=hrAllSeason,
                           ssAllSeason=ssAllSeason,
                           title="League Leaders",
                           year=year)


'''
# -----------------------------------------------------------------------------
#             STATIC PAGES
# -----------------------------------------------------------------------------
'''


@app.route(Routes["privacy"])
def privacy_policy():
    return render_template("website/privacy-policy.html")


@app.route(Routes['eventspage'] + "/<int:year>" + "/json")
def events_page_json(year):
    if year in EVENTS:
        return json.dumps(EVENTS[year])
    else:
        return json.dumps({year: {}})


@app.route(Routes['eventspage'] + "/<int:year>")
def events_page(year):
    if year in EVENTS:
        return render_template("website/events.html",
                               dates=EVENTS[year],
                               route=Routes,
                               base=base_data(year),
                               title="Events",
                               year=year)
    else:
        return render_template("website/notFound.html",
                               year=year,
                               route=Routes,
                               base=base_data(year),
                               title="Not Found")


@app.route(Routes['fieldsrulespage'] + "/<int:year>")
def rules_fields(year):
    return render_template("website/fields-and-rules.html",
                           route=Routes,
                           base=base_data(year),
                           title="Fields & Rules",
                           year=year)


@app.route(Routes['sponsorbreakdown'] + "/<int:year>")
def sponsor_breakdown(year):
    return render_template("website/sponsor_breakdown.html",
                           route=Routes,
                           base=base_data(year),
                           title="ESPYS Breakdown by Sponsor",
                           year=year,
                           teams=get_teams(year))


@app.route(Routes['sponsorbreakdown'] + "/<int:year>" + "/<int:garbage>")
def get_sponsor_breakdown(year, garbage):
    sponsors = DB.session.query(Sponsor).filter(Sponsor.active == True).all()
    tree = {'name': 'Sponsor Breakdown by ESPYS'}
    total = func.sum(Espys.points).label('espys')
    start = datetime(year, 1, 1)
    end = datetime(year, 12, 30)
    result = []
    for sponsor in sponsors:
        element = {}
        element['name'] = str(sponsor)
        children_list = []
        espys = (DB.session.query(total, Team)
                 .join(Sponsor)
                 .join(Team, Espys.team_id == Team.id)
                 .filter(Espys.date.between(start, end))
                 .filter(Espys.sponsor_id == sponsor.id)
                 .group_by(Team)).all()
        for espy in espys:
            point = {}
            point['name'] = str(espy[1])
            point['size'] = espy[0]
            children_list.append(point)
        if len(children_list) == 0:
            element['size'] = 0
        else:
            element['children'] = children_list
        result.append(element)
    tree['children'] = result
    return json.dumps(tree)


@app.route(Routes['espysbreakdown'] + "/<int:year>")
def espys_breakdown_request(year):
    return get_espys_breakdown(year)


'''
# -----------------------------------------------------------------------------
#                FUNCTIONS TO HELP with ROUTES
# -----------------------------------------------------------------------------
'''


def get_team(year, tid):
    result = Team.query.get(tid)
    team = None
    if result is not None:
        captain = "TBD"
        players = []
        for player in result.players:
            if player.name not in players:
                players.append(player.name)
        if result.player_id is not None:
            captain = str(Player.query.get(result.player_id))
        p_ = player_summary(team_id=tid)
        stats = []
        for name in p_:
            sp = (
                (
                    p_[name]["s"] +
                    p_[name]["ss"] +
                    p_[name]["d"] * 2 +
                    p_[name]["hr"] * 4
                ) / p_[name]['bats']
            )
            stats.append({
                'id': p_[name]['id'],
                'name': name,
                'ss': p_[name]['ss'],
                's': p_[name]['s'],
                'd': p_[name]['d'],
                'hr': p_[name]['hr'],
                'bats': p_[name]['bats'],
                'ba': "{0:.3f}".format(p_[name]['avg']),
                'sp': "{0:.3f}".format(sp)})
#            players.append(name)
        record = single_team(tid)
        team = {'name': str(result),
                'league': str(League.query.get(result.league_id)),
                'captain': str(captain),
                'players': players,
                'record': record,
                'wins': record[tid]['wins'],
                'losses': record[tid]['losses'],
                'ties': record[tid]['ties'],
                'stats': stats}
    return team


def get_teams(year):
    result = (DB.session.query(Team.id, Team.color, Sponsor.nickname)
              .join(Sponsor)
              .filter(Team.year == year)
              .order_by(Sponsor.nickname).all())
    teams = []
    for team in result:
        teams.append({'id': team[0],
                      'name': team[2] + " " + team[1]})
    return teams


# -----------------------------------------------------------------------------
#                FUNCTIONS TO DEAL WITH article posts
# -----------------------------------------------------------------------------
def get_all_descriptions(year):
    dire = os.path.join(POSTS, str(year))
    result = []
    for i in os.listdir(dire):
        if i.endswith(".html"):
            fname = str(i)
            fname.replace(".html", "")
            post_date = fname.split("_")[0]
            description = "_".join(fname.split("_")[1:])
            result.append({"date": post_date,
                           "description": description})
    return result


def get_summaries(year):
    dire = os.path.join(POSTS, str(year))
    result = []
    try:
        for i in os.listdir(dire):
            if i.endswith(".html"):
                result.append(rip_summary(i, year))
    except OSError:
        pass
    return result


def rip_summary(f, year):
    post_date = f.split("_")[0]
    description = "_".join(f.split("_")[1:])
    result = {"summary": [],
              "image": None,
              "title": None,
              "name": description,
              "date": post_date}
    f = os.path.join(POSTS, str(year), f)
    with open(f) as f:
        # read the header in
        line = f.readline().strip()
        while (not f.readline().strip().startswith("{% block content %}") and
               len(line) > 0):
            line = f.readline().strip()
        line = f.readline().strip()
        while not line.startswith("{% endblock %}") and len(line) > 0:
            if "<h" in line:
                line = line.replace("<h4>", "")
                line = line.replace("</h4>", "")
                if result['title'] is None:
                    result['title'] = line.strip()
            elif "<img" in line:
                image = line.split('filename="')[1]
                image = image.split('"')[0]
                image = image.split("/")[-1]
                if result['image'] is None:
                    result['image'] = image
            elif "<p" in line:
                while "</p>" not in line:
                    line = line + f.readline().strip()
                line = line.replace("<p>", "")
                line = line.replace("</p>", "")
                if len(result['summary']) < 24:
                    words = line.split(" ")
                    i = 0
                    while len(result['summary']) < 50 and i < len(words):
                        result['summary'].append(words[i])
                        i += 1
            line = f.readline().strip()
        if len(result['summary']) > 0:
            result['summary'] = " ".join(result['summary'] + ["..."])
        else:
            result['summary'] = "No summary"
    return result


def post_json(f, year):
    result = []
    f = os.path.join(POSTS, str(year), f)
    with open(f) as fn:
        line = fn.readline().strip()
        # read the header
        while not line.startswith("{% block content %}") and len(line) > 0:
            line = fn.readline().strip()
        lines = fn.readline().strip()
        while not lines.startswith("{% endblock %}") and len(lines) > 0:
            # read a p tag
            if "<p" in lines:
                # read the second p tag
                while "</p>" not in lines:
                    lines = lines + fn.readline().strip()
                lines = lines.replace("<p>", "")
                lines = lines.replace("</p>", "")
                result.append(lines)
            lines = fn.readline().strip()
    return result


def post_raw_html(f, year):
    f = os.path.join(POSTS, str(year), f)
    with open(f) as fn:
        line = fn.readline().strip()
        # read the header
        while not line.startswith("{% block content %}") and len(line) > 0:
            line = fn.readline().strip()
        lines = fn.readline().strip()
        result = ""
        while not lines.startswith("{% endblock %}") and len(lines) > 0:
            if "<img" not in lines:
                result += lines
            lines = fn.readline().strip()
    return result
