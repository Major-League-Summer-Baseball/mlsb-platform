'''
@author: Dallas Fraser
@since: 2016-04-12
@organization: MLSB API
@summary: Holds the the views for the website
'''
from sqlalchemy.sql.expression import and_
from api import app, PICTURES
from api.routes import Routes
from flask import render_template, url_for, send_from_directory, \
                    redirect
from api.model import Team, Player, Sponsor, League, Game, Bat, Espys
from api.variables import SPONSORS, UNASSIGNED
from datetime import date, datetime, time
from api.advanced.team_stats import team_stats
from api.advanced.players_stats import post as player_summary
from api import DB
from sqlalchemy.sql import func

@app.route("/")
@app.route(Routes["homepage"])
def reroute():
    year = date.today().year
    return redirect(url_for("index", year=year))

@app.route(Routes["homepage"] + "/<int:year>")
def index(year):
    print(get_sponsors())
    return render_template("website/index.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           title="Recent news",
                           year=year)

@app.route(Routes['sponsorspicture'] + "/<int:id>")
def sponsor_picture(id):
    print(PICTURES)
    pic = SPONSORS.get(id, None)
    if pic is None:
        return send_from_directory(PICTURES,
                                   filename=SPONSORS[0])
    else:
        return send_from_directory(PICTURES, filename=pic)

@app.route(Routes['sponsorspage'] + "/<int:year>")
def sponsors_page(year):
    return render_template("website/sponsors.html",
                           route=Routes,
                           sponsors=get_sponsors(), 
                           title="Sponsors",
                           year=year)

@app.route(Routes['sponsorspage'] +"/<int:year>" +  "/<int:id>")
def sponsor_page(year, id):
    sponsor = get_sponsor(id)
    if sponsor is None:
        page = render_template("website/notFound.html",
                               route=Routes,
                               sponsors=get_sponsors(),
                               title = "Not Found",
                               year=year)
    else:
        page = render_template("website/sponsor.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           sponsor=sponsor, 
                           title="Sponsor | " + sponsor['name'],
                           year=year)
    return page


@app.route(Routes["schedulepage"] + "/<int:year>")
def schedule(year):
    return render_template("website/schedule.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           games=get_games(year),
                           title="Schedule",
                           year=year)

@app.route(Routes['standingspage'] + "/<int:year>")
def standings(year):
    return render_template("website/standings.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           leagues=get_leagues(year),
                           title="Standings",
                           year=year)
@app.route(Routes['statspage'] + "/<int:year>")
def stats_page(year):
    players = player_summary(year)
    return render_template("website/stats.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           title="Players Stats",
                           year=year,
                           players=players
                           )

@app.route(Routes['teampage'] + "/<int:year>/<int:team_id>")
def team_page(year, team_id):
    team = get_team(year, team_id)
    return render_template("website/team.html",
                       route=Routes,
                       sponsors=get_sponsors(),
                       team=team,
                       title="Team - " + str(team['name']),
                       year=year)

@app.route(Routes['playerpage']+ "/<int:year>/<int:player_id>")
def player_page(year, player_id):
    name = Player.query.get(player_id).name
    years = (DB.session.query(Team.year, Team.id).join(Player)
                .filter(Player.id==player_id)
                .order_by(Team.year.desc()).all())
    print(years)
    stats = []
    for entry in years:
        player = player_summary(year=entry[0],
                                team_id=entry[1],
                                player_id=player_id)[name]
        player['team'] = str(Team.query.get(entry[1]))
        player['team_id'] = entry[1]
        player['year'] = entry[0]
        stats.append(player)
    print(stats)
    return render_template("website/player.html",
                       route=Routes,
                       sponsors=get_sponsors(),
                       stats=stats,
                       title="Player Stats",
                       name=name,
                       year=year)

@app.route(Routes['leagueleaderpage'] + "/<int:year>")
def leaders_page(year):
    women = get_leaders("f", year, "ss")[:5]
    men = get_leaders("m", year, "hr")[:5]
    return render_template("website/new-leaders.html",
                       route=Routes,
                       sponsors=get_sponsors(),
                       men=men,
                       women=women,
                       title="League Leaders",
                       year=year)
'''
# -----------------------------------------------------------------------------
#             STATIC PAGES
# -----------------------------------------------------------------------------
'''
@app.route(Routes['eventspage'] + "/<int:year>")
def events_page(year):
    return render_template("website/events.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           title="Events",
                           year=year)

@app.route(Routes['fieldsrulespage'] + "/<int:year>")
def rules_fields(year):
    return render_template("website/fields-and-rules.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           title="Fields & Rules",
                           year=year)


'''
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
#                FUNCTIONS TO HELP with ROUTES
# -----------------------------------------------------------------------------
'''
def get_sponsor(id):
    s = Sponsor.query.get(id)
    expect = None
    if s is not None:
        expect = {"name": s.name,
                  "id": s.id}
    return expect

def get_leaders(gender, year, hit):
    leaders = []
    hits = func.count(Bat.player_id).label("total")
    d1 = date(year, 1, 1)
    t = time(0, 0)
    d2 = date(year, 12, 30)
    start = datetime.combine(d1, t)
    end = datetime.combine(d2, t)
    bats = (DB.session.query(Bat.player_id,
                            hits,
                            Bat.team_id,
                            Bat.classification,
                            Bat.team_id
                            ).join(Game)
                            .filter(Game.date.between(start, end))
                            .filter(Bat.player_id != UNASSIGNED)
                            .group_by(Bat.player_id)
                            .group_by(Bat.classification)
                            .group_by(Bat.team_id)).subquery("bats")
    players = (DB.session.query(Player.name,
                              Player.id,
                              bats.c.total,
                              bats.c.team_id,
                              bats.c.classification
                              )
                              .join(bats)
                              .filter(bats.c.classification == hit)
                              .order_by(bats.c.total.desc())
                              )
    players = players.all()
    for player in players:
        result = {'name': player[0],
                  'id': player[1],
                  'hits': player[2],
                  'team': str(Team.query.get(player[3]))
                  }
        leaders.append(result)
    return leaders

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

def get_team(year, tid):
    result = Team.query.get(tid)
    team = None
    if result is not None:
        captain = "TBD"
        p_ = player_summary(team_id=tid)
        players = []
        for name in p_:
            sp = (
                    (
                      p_[name]["s"]
                      + p_[name]["ss"]
                      + p_[name]["d"] * 2
                      + p_[name]["hr"] * 4
                      ) / p_[name]['bats']
                  )
            players.append({
                'id':p_[name]['id'],
                'name': name, 
                'ss': p_[name]['ss'],
                's': p_[name]['s'],
                'd': p_[name]['d'],
                'hr': p_[name]['hr'],
                'bats': p_[name]['bats'],
                'ba': "{0:.3f}".format(p_[name]['avg']),
                'sp': "{0:.3f}".format(sp)})
        team = {'name': str(result),
                'league': str(League.query.get(result.league_id)),
                'captain': str(captain),
                'players': players}
        print(team)
    return team

def get_teams(year):
    result = Team.query.filter_by(year=year).all()
    teams = []
    for team in result:
        teams.append({'id': team.id,
                     'name': str(team)})
    return teams

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
                result['score'] = (str(scores['home_score']) + '-' 
                                   + str(scores['away_score']))
            games[league.id]['games'].append(result)
    return games

def get_leagues(year):
    result = League.query.all()
    leagues = {}
    for league in result:
        leagues[league.id] = {'name':league.name, 'teams':[]} 
        teams = team_stats(year, league.id)
        for team in teams:
            valid_form = {'name': teams[team]['name'],
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
    info = Sponsor.query.filter_by(active=True).all()
    sponsors = []
    for i in range(0, len(info)):
        sponsors.append({"name":info[i].name,
                       "id": info[i].id})
    return sponsors
'''
# -----------------------------------------------------------------------------
'''