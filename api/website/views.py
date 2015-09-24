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


def get_sponsors():
    info = Sponsor.query.all()
    sponsors = []
    for i in range(0, len(info)):
        sponsors.append({"name":info[i].name,
                       "id": info[i].id})
    return sponsors