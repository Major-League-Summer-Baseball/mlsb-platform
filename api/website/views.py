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
@app.route(Routes["homepage"])
def index():
    return render_template("index.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           title="Recent news")

@app.route(Routes['sponsorspicture'] + "/<int:id>")
def sponsor_picture(id):
    print(PICTURES)
    return send_from_directory(PICTURES,
                               filename=SPONSORS[id])

@app.route(Routes['sponsorspage'] + "/<int:id>")
def sponsor_page(id):
    return render_template("sponsor.html",
                           route=Routes,
                           sponsors=get_sponsors(), 
                           title="Sponsors")

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
def get_sponsors():
    info = Sponsor.query.all()
    sponsors = []
    for i in range(0, len(info)):
        sponsors.append({"name":info[i].name,
                       "id": info[i].id})
    return sponsors