'''
@author: Dallas Fraser
@since: 2015-09-22
@organization: MLSB API
@summary: Holds the the views for the website
'''
from api import app, PICTURES
from api.routes import Routes
from flask import render_template, send_file, url_for, send_from_directory
from api.model import Team, Player, Sponsor
from api.variables import SPONSORS

@app.route("/")
@app.route(Routes["homepage"])
def index():
    print(get_sponsors())
    return render_template("index.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           title="Recent news")

@app.route(Routes['sponsorspicture'] + "/<int:id>")
def sponsor_picture(id):
    print(PICTURES)
    return send_from_directory(PICTURES,
                               filename=SPONSORS[id])

@app.route(Routes['sponsorspage'])
def sponsors_page():
    return render_template("sponsors.html",
                           route=Routes,
                           sponsors=get_sponsors(), 
                           title="Sponsors")

@app.route(Routes['sponsorspage'] + "/<int:id>")
def sponsor_page(id):
    sponsor = get_sponsor(id)
    if sponsor is None:
        page = render_template("notFound.html",
                               route=Routes,
                               sponsors=get_sponsors(),
                               title = "Not Found")
    else:
        page = render_template("sponsor.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           sponsor=sponsor, 
                           title="Sponsor | " + sponsor['name'])
    return page

@app.route(Routes['mysterybuspage'])
def mystery_bus():
    return render_template("mysterybus.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           title="Mystery Bus")

@app.route(Routes['bluejayspage'])
def blue_jays():
    return render_template("bluejays.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           title="Blue Jays Game")

@app.route(Routes['beerfestpage'])
def beerfest():
    return render_template("beerfest.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           title="Beerfest")

@app.route(Routes['raftingpage'])
def rafting():
    return render_template("rafting.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           title="Rafting")

@app.route(Routes['beerwellpage'])
def beerwell():
    return render_template("beerwell.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           title="Beerwell")

@app.route(Routes['hftcpage'])
def hftc():
    return render_template("hftc.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           title="Hitting for the Cycle")

@app.route(Routes['summerweenpage'])
def summerween():
    return render_template("summerween.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           title="Summerween")

@app.route(Routes['espypage'])
def espy():
    return render_template("espy.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           title="ESPY Awards")

@app.route(Routes['rulespage'])
def rules():
    return render_template("rules.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           title="Rules")

@app.route(Routes['fieldspage'])
def fields():
    return render_template("fields.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           title="Fields")

@app.route(Routes["schedulepage"])
def schedule():
    return render_template("schedule.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           games=get_games(),
                           title="Schedule")

@app.route(Routes['standingspage'])
def standings():
    return render_template("standings.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           leauges=get_leagues(),
                           title="Standings")

@app.route(Routes['teamspage'])
def teams_page():
    return render_template("teams.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           teams=get_teams(),
                           title="Teams")

@app.route(Routes['leaderspage'])
def leaders():
    return render_template("leaders.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           leaders=get_leaders("m"),
                           title="Race for the Domus Cup")

@app.route(Routes['wleaderspage'])
def wleaders():
    return render_template("wleaders.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           leaders=get_leaders("f"),
                           title="Sentry Singles")

@app.route(Routes['espystandingspage'])
def espy_standings():
    return render_template("espystandings.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           standings=get_espy(),
                           title="ESPY Standings")

def get_sponsor(id):
    s = Sponsor.query.get(id)
    expect = None
    if s is not None:
        expect = {"name": s.name,
                  "id": s.id}
    return expect

def get_leaders(gender):
    leaders = []
    #TODO
    return leaders

def get_espy():
    espy = []
    #TODO
    return espy

def get_teams():
    teams =[]
    #TODO
    return teams

def get_games():
    games = []
    #TODO
    return games

def get_leagues():
    leagues = []
    #TODO
    return leagues

def get_sponsors():
    info = Sponsor.query.all()
    sponsors = []
    for i in range(0, len(info)):
        sponsors.append({"name":info[i].name,
                       "id": info[i].id})
    return sponsors
