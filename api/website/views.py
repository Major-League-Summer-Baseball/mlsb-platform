'''
@author: Dallas Fraser
@since: 2016-04-12
@organization: MLSB API
@summary: Holds the the views for the website
'''
from sqlalchemy.sql.expression import and_
from api import app, PICTURES, POSTS, cache
from api.routes import Routes
from flask import render_template, url_for, send_from_directory, \
                    redirect, request
from api.model import Team, Player, Sponsor, League, Game, Bat, Espys, Fun
from api.variables import UNASSIGNED, EVENTS, NOTFOUND
from datetime import date, datetime, time
from api.advanced.team_stats import team_stats, single_team
from api.advanced.players_stats import post as player_summary
from api.advanced.league_leaders import get_leaders
from api import DB
from sqlalchemy.sql import func
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
    template = "/".join(["website","posts", str(year), file_name])
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
@cache.cached(timeout=50)
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
    if isinstance(name, int):
        name = Sponsor.query.get(name)
        if name is None:
            name = "notFound"
        else:
            name = str(name)
    name= name.lower().replace(" ", "_") + ".png"
    f = os.path.join(PICTURES, "sponsors",  name)
    fp = os.path.join(PICTURES, "sponsors")
    if os.path.isfile(f):
        return send_from_directory(fp, filename=name)
    else:
        return send_from_directory(fp, filename=NOTFOUND)

@app.route(Routes['teampicture'] + "/<int:team>")
def team_picture(team):
    if isinstance(team, int):
        team = Team.query.get(team)
        name = "notFound"
        if team.sponsor_id is not None:
            name = Sponsor.query.get(team.sponsor_id)
            if name is None:
                name = "notFound"
            else:
                name = str(name)
    name= name.lower().replace(" ", "_") + ".png"
    f = os.path.join(PICTURES, "sponsors",  name)
    fp = os.path.join(PICTURES, "sponsors")
    if os.path.isfile(f):
        return send_from_directory(fp, filename=name)
    else:
        return send_from_directory(fp, filename=NOTFOUND)

@app.route(Routes['postpicture'] + "/<name>")
def post_picture(name):
    f = os.path.join(PICTURES, "posts", name)
    fp = os.path.join(PICTURES,"posts" )
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

@app.route(Routes['sponsorspage'] +"/<int:year>" +  "/<int:id>")
def sponsor_page(year, id):
    sponsor = get_sponsor(id)
    if sponsor is None:
        page = render_template("website/notFound.html",
                               route=Routes,
                               base=base_data(year),
                               title = "Not Found",
                               year=year)
    else:
        page = render_template("website/sponsor.html",
                           route=Routes,
                           base=base_data(year),
                           sponsor=sponsor,
                           title="Sponsor | " + sponsor['name'],
                           year=year)
    return page

@app.route(Routes["schedulepage"] + "/<int:year>")
def schedule(year):
    return render_template("website/schedule.html",
                           route=Routes,
                           base=base_data(year),
                           games=get_games(year),
                           title="Schedule",
                           year=year)

@app.route(Routes['standingspage'] + "/<int:year>")
def standings(year):
    return render_template("website/standings.html",
                           route=Routes,
                           base=base_data(year),
                           leagues=get_leagues(year),
                           title="Standings",
                           year=year)

@app.route(Routes['statspage'] + "/<int:year>")
def stats_page(year):
    players = player_summary(year)
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

@app.route(Routes['playerpage']+ "/<int:year>/<int:player_id>")
def player_page(year, player_id):
    player = Player.query.get(player_id)
    name = player.name
    years = []
    for team in player.teams:
        years.append((team.year, team.id))
    stats = []
    for entry in years:
        player = player_summary(year=entry[0],
                                team_id=entry[1],
                                player_id=player_id)[name]
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
    women = get_leaders("ss", year=year)[:5]
    men = get_leaders("hr", year=year)[:5]
    return render_template("website/new-leaders.html",
                       route=Routes,
                       base=base_data(year),
                       men=men,
                       women=women,
                       title="League Leaders",
                       year=year)
'''
# -----------------------------------------------------------------------------
#             STATIC PAGES
# -----------------------------------------------------------------------------
'''

@app.route(Routes['eventspage'] + "/<int:year>" + "/json")
def events_page_json(year):
        if year in EVENTS:
            return json.dumps(EVENTS[year])
        else:
            return json.dumps({year:{}})

@app.route(Routes['eventspage'] + "/<int:year>")
def events_page(year):
        if year in EVENTS:
            return render_template("website/events.html",
                               dates = EVENTS[year],
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

@app.route("/test/<int:year>")
def test(year):
    return render_template("website/test.html",
                           route=Routes,
                           base=base_data(year),
                           title="Test",
                           year=year)

'''
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
#                FUNCTIONS TO HELP with ROUTES
# -----------------------------------------------------------------------------
'''
@cache.memoize(timeout=50)
def get_sponsor(id):
    s = Sponsor.query.get(id)
    expect = None
    if s is not None:
        expect = {"name": s.name,
                  "id": s.id}
    return expect

@cache.memoize(timeout=50)
def get_espy(year):
    espy = []
    espys = func.sum(Espys.points).label("espys")
    teams = (DB.session.query(Team,
                              espys
                               )
                               .join(Team.espys)
                               .filter(Team.year==year)
                               .group_by(Team.id)
                               .order_by(espys.desc()).all()
                               )
    for team in teams:
        espy.append({
                     'espys': team[1],
                     'name': str(team[0])})
    return espy

@cache.memoize(timeout=50)
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
                      p_[name]["s"]
                      + p_[name]["ss"]
                      + p_[name]["d"] * 2
                      + p_[name]["hr"] * 4
                      ) / p_[name]['bats']
                  )
            stats.append({
                'id':p_[name]['id'],
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

@cache.memoize(timeout=50)
def get_teams(year):
    result = Team.query.filter_by(year=year).all()
    teams = []
    for team in result:
        teams.append({'id': team.id,
                     'name': str(team)})
    return teams

@cache.memoize(timeout=50)
def get_games(year=None, summary=False):
    games = {}
    leagues = League.query.all()
    t = time(0, 0)
    if year is not None:
        d1 = date(year, 1, 1)
        d2 = date(year, 12, 30)
    elif summary:
        today = date.today()
        d1 = date(today.year, today.month, today.day - 3)
        d2 = date(today.year, today.month, today.day + 3)
    else:
        d1 = date(2014, 1, 1)
        d2 = date(date.today().year, 12, 30)
    start = datetime.combine(d1, t)
    end = datetime.combine(d2, t)
    for league in leagues:
        g = Game.query.filter(and_(Game.league_id==league.id,Game.date.between(start, end) )).order_by("date").all()
        games[league.id] = {'league_name': league.name, 'games': []}
        for game in g:
            result = game.json()
            if game.date < datetime.today():
                scores = game.summary()
                result['score'] = (str(scores['away_score']) + '-'
                                   + str(scores['home_score']))
            games[league.id]['games'].append(result)
    return games

@cache.memoize(timeout=50)
def get_leagues(year):
    result = League.query.all()
    leagues = {}
    for league in result:
        leagues[league.id] = {'name':league.name, 'teams':[]}
        teams = team_stats(year, league.id)
        for team in teams:
            valid_form = {'name': teams[team]['name'],
                          'id': team,
                          'espys': Team.query.get(team).espys_awarded(),
                          'games': teams[team]['games'],
                          'wins': teams[team]['wins'],
                          'losses': teams[team]['losses'],
                          'ties': teams[team]['ties'],
                          'runs_for': teams[team]['runs_for'],
                          'runs_against': teams[team]['runs_against'],
                          'plus_minus': teams[team]['runs_for'] - teams[team]['runs_against']
                   }
            leagues[league.id]['teams'].append(valid_form)
    return leagues

def get_sponsors():
    info = (DB.session.query(Sponsor)
                .filter(Sponsor.active==True)
                .order_by(Sponsor.name)).all()
    sponsors = []
    for i in range(0, len(info)):
        sponsors.append(info[i].json())
    return sponsors

from api.advanced.game_stats import post as game_summary
def get_upcoming_games(year):
    return game_summary(year=year, today=True)

@cache.memoize(timeout=100)
def base_data(year):
    base = {}
    base['games'] = get_upcoming_games(year)
    base['sponsors'] = get_sponsors()
    fun_count = Fun.query.filter_by(year=year).first()
    if fun_count is None:
        fun_count = {'year': year, 'count': 0}
    else:
        fun_count = fun_count
    base['fun'] = fun_count
    return base

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
                           "description":description})
    return result

def get_summaries(year):
    dire = os.path.join(POSTS, str(year))
    result = []
    for i in os.listdir(dire):
        if i.endswith(".html"):
            result.append(rip_summary(i, year))
    return result

def rip_summary(f, year):
    post_date = f.split("_")[0]
    description = "_".join(f.split("_")[1:])
    result = {"summary": [],
              "image": None,
              "title":  None,
              "name": description,
              "date": post_date}
    f = os.path.join(POSTS, str(year), f)
    with open (f) as f:
        # read the header in
        line = f.readline().strip()
        while not f.readline().strip().startswith("{% block content %}") and len(line) > 0:
            line = f.readline().strip()
        line = f.readline().strip()
        while not line.startswith("{% endblock %}") and len(line) > 0:
            if "<h" in line:
                line = line.replace("<h4>", "")
                line = line.replace("</h4>", "")
                if result['title'] is None:
                    result['title'] = line
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
                    lines = lines + fn.readline.strip()
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
'''
# -----------------------------------------------------------------------------
'''
    