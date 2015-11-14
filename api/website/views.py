'''
@author: Dallas Fraser
@since: 2015-09-22
@organization: MLSB API
@summary: Holds the the views for the website
'''
from sqlalchemy.sql.expression import and_
from api import app, PICTURES
from api.routes import Routes
from flask import render_template, send_file, url_for, send_from_directory, \
                    redirect
from api.model import Team, Player, Sponsor, League, Game, Bat
from api.variables import SPONSORS
from datetime import date, datetime, time
from sqlalchemy import desc
from api.advanced.team_stats import single_team
from api.variables import HITS


@app.route("/")
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

@app.route(Routes['teamspage'] + "/<int:year>")
def teams_page(year):
    return render_template("website/teams.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           teams=get_teams(year),
                           title="Teams",
                           year=year)

@app.route(Routes['teampage'] + "/<int:year>/<int:id>")
def team_page(year, id):
    team = get_team(year, id)
    return render_template("website/team.html",
                       route=Routes,
                       sponsors=get_sponsors(),
                       team=team,
                       title="Team - " + str(team['name']),
                       year=year)

@app.route(Routes['leaderspage'] + "/<int:year>")
def leaders(year):
    return render_template("website/leaders.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           leaders=get_leaders("m", year, "hr"),
                           title="Race for the Domus Cup",
                           year=year)

@app.route(Routes['wleaderspage'] + "/<int:year>")
def wleaders(year):
    return render_template("website/wleaders.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           leaders=get_leaders("f", year, "ss"),
                           title="Sentry Singles",
                           year=year)

@app.route(Routes['espystandingspage'] + "/<int:year>")
def espy_standings(year):
    return render_template("website/espystandings.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           standings=get_espy(year),
                           title="ESPY Standings",
                           year=year)
'''
# -----------------------------------------------------------------------------
#             STATIC PAGES
# -----------------------------------------------------------------------------
'''
@app.route(Routes['mysterybuspage'] + "/<int:year>")
def mystery_bus(year):
    return render_template("website/mysterybus.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           title="Mystery Bus",
                           year=year)

@app.route(Routes['bluejayspage'] + "/<int:year>")
def blue_jays(year):
    return render_template("website/bluejays.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           title="Blue Jays Game",
                           year=year)

@app.route(Routes['beerfestpage'] + "/<int:year>")
def beerfest(year):
    return render_template("website/beerfest.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           title="Beerfest",
                           year=year)

@app.route(Routes['raftingpage'] + "/<int:year>")
def rafting(year):
    return render_template("website/rafting.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           title="Rafting",
                           year=year)

@app.route(Routes['beerwellpage'] + "/<int:year>")
def beerwell(year):
    return render_template("website/beerwell.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           title="Beerwell",
                           year=year)

@app.route(Routes['hftcpage'] + "/<int:year>")
def hftc(year):
    return render_template("website/hftc.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           title="Hitting for the Cycle",
                           year=year)

@app.route(Routes['summerweenpage'] + "/<int:year>")
def summerween(year):
    return render_template("website/summerween.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           title="Summerween",
                           year=year)

@app.route(Routes['espypage'] + "/<int:year>")
def espy(year):
    return render_template("website/espy.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           title="ESPY Awards",
                           year=year)

@app.route(Routes['rulespage'] + "/<int:year>")
def rules(year):
    return render_template("website/rules.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           title="Rules",
                           year=year)

@app.route(Routes['fieldspage'] + "/<int:year>")
def fields(year):
    return render_template("website/fields.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           title="Fields",
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
    teams = Team.query.filter_by(year=year).all()
    for team in teams:
        # loop through each team and its games7
        result = {}
        players = {}
        for player in team.players:
            # initialize a lookup for the players
            if player.gender == gender:
                players[player.id] = player.name
                result[player.name] = 0
        for game in team.away_games:
            for bat in game.bats:
                player = players.get(bat.player_id, None)
                print(player, bat)
                if player is not None and bat.classification == hit:
                    result[player] += 1
        for game in team.home_games:
            for bat in game.bats:
                player = players.get(bat.player_id, None)
                print(player, bat)
                if player is not None and bat.classification == hit:
                    result[player] += 1
        for player, hits in result.items():
            print(player)
            if hits > 0:
                leaders.append({'name':player, 
                                'team':str(team),
                                'hits':hits})
    #TODO
    print(leaders)
    return leaders

def get_espy(year):
    espy = []
    teams = Team.query.filter_by(year=year).order_by("espys desc").all()
    rank = 0
    for team in teams:
        rank += 1
        espy.append({'rank': rank,
                     'espys': team.espys,
                     'name': str(team)})
    return espy

def get_team(year, id):
    result = Team.query.get(id)
    team = None
    print(result)
    print(result.player_id)
    if result is not None:
        captain = "TBD"
        stats = {}
        players = {}
        if result.player_id is not None:
            captain = Player.query.get(result.player_id)
            players[result.player_id] = captain
            stats[captain] = {'s': 0,
                               'd': 0,
                               'ss': 0,
                               'hr': 0,
                               'bats': 0,
                               'id': result.player_id}
        for player in result.players:
            # initialize a lookup for the players
            players[player.id] = player.name
            stats[player.name] = {'s': 0,
                                   'd': 0,
                                   'ss': 0,
                                   'hr': 0,
                                   'bats': 0,
                                   'id': player.id}
        for game in result.away_games:
            for bat in game.bats:
                player = players.get(bat.player_id, None)
                if player is not None:
                    if bat.classification in HITS:
                        stats[player][bat.classification] += 1
                    stats[player]['bats'] += 1
        for game in result.home_games:
            for bat in game.bats:
                player = players.get(bat.player_id, None)
                if player is not None:
                    if bat.classification in HITS:
                        stats[player][bat.classification] += 1
                    stats[player]['bats'] += 1
        players = []
        for player, hits in stats.items():
            if hits['bats'] > 0:
                ba = (hits['ss'] + hits['s'] + hits['d'] + hits['hr']) / hits['bats']
                sp = ((hits['ss'] + hits['s'] + hits['d'] * 2 + hits['hr'] * 4)
                      / hits['bats'])
            else:
                ba = 0
                sp = 0
            players.append({
                            'id':hits['id'],
                            'name': player, 
                            'ss': hits['ss'],
                            's': hits['s'],
                            'd': hits['d'],
                            'hr': hits['hr'],
                            'bats': hits['bats'],
                            'ba': "{0:.3f}".format(ba),
                            'sp': "{0:.3f}".format(sp)})
        print(players)
        team = {'name': str(result),
                'league': str(League.query.get(result.league_id)),
                'captain': str(captain),
                'players': players}
        print(team)
    return team

def get_teams(year):
    result =teams = Team.query.filter_by(year=year).all()
    teams = []
    for team in result:
        teams.append({'id': team.id,
                     'name': str(team)})
    #TODO
    return teams

def get_games(year):
    games = {}
    leagues = League.query.all()
    if year is not None:
        d1 = date(year, 1, 1)
        t1 = time(0, 0)
        d2 = date(year, 12, 30)
        t2 = time(0 , 0)
    start = datetime.combine(d1, t1)
    end = datetime.combine(d2, t2)
    for league in leagues:
        g = Game.query.filter(and_(Game.league_id==league.id,Game.date.between(start, end) )).order_by("date").all()
        games[league.id] = {'league_name': league.name, 'games': []}
        for game in g:
            result = game.json()
            if game.date < datetime.today():
                result['score'] = get_score(game)
            games[league.id]['games'].append(result)
    print(games)
    return games

def get_score(game):
    home_team_id = game.home_team_id
    home_score = 0
    away_score = 0
    for bat in game.bats:
        if bat.team_id == home_team_id:
            home_score += bat.rbi
        else:
            away_score += bat.rbi
    return str(home_score) + " - " + str(away_score)

def get_leagues(year):
    result = League.query.all()
    leagues = {}
    for league in result:
        leagues[league.id] = {'name':league.name, 'teams':[]}
    teams = Team.query.filter_by(year=year).all()
    for team in teams:
        result = single_team(team.id)[team.id]
        print(result)
        format = {'name': str(team),
                  'games': result['games'],
                  'wins': result['away_wins'] + result['home_wins'],
                  'losses': result['away_losses'] + result['home_losses'],
                  'runs_for': result['runs_for'],
                  'runs_against': result['runs_against'],
                  'plus_minus': result['runs_for'] - result['runs_against']
                   }
        leagues[team.league_id]['teams'].append(format)
    return leagues

def get_sponsors():
    info = Sponsor.query.all()
    sponsors = []
    for i in range(0, len(info)):
        sponsors.append({"name":info[i].name,
                       "id": info[i].id})
    return sponsors
'''
# -----------------------------------------------------------------------------
'''