'''
Name: Dallas Fraser
Date: 2014-08-25
Project: MLSB API
Purpose: Holds the routes for the admin side
'''
from flask.ext.restful import Resource, reqparse
from flask import Response, render_template, make_response
from json import dumps
from api.routes import Routes
from api import app, PICTURES
from api.routes import Routes
from flask import render_template, send_file, url_for, send_from_directory
from api.model import Team, Player, Sponsor
from api.variables import SPONSORS

@app.route(Routes['aindex'])
def admin_home():
    return render_template("admin/index.html",
                           route=Routes,
                           title="Admin")