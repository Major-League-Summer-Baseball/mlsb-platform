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
from flask import render_template, send_file, url_for, send_from_directory,\
                  redirect, session, request
from api.model import Team, Player, Sponsor
from api.variables import SPONSORS
from api.authentication import check_auth
from api.model import Player
@app.route(Routes['aindex'])
def admin_home():
    if not logged_in():
        return redirect(url_for('admin_login'))
    return render_template("admin/index.html",
                           route=Routes,
                           title="Admin")

@app.route(Routes['editplayer'])
def admin_edit_player():
    if not logged_in():
        return redirect(url_for('admin_login'))
    results = Player.query.all()
    players = []
    for player in results:
        players.append(player.json())
    return render_template("admin/editPlayer.html",
                           route=Routes,
                           players=players,
                           title="Edit Players",
                           admin=session['admin'],
                           password=session['password'])

@app.route(Routes['alogout'])
def admin_logout():
    logout()
    return redirect(url_for('index'))

@app.route(Routes['aportal'], methods=['POST'])
def admin_portal():
    if 'admin' in session and 'password' in session:
        return redirect(url_for('admin_form'))
    else:
        print(request.form)
        admin = request.form.get('admin')
        password = request.form.get('password')
        if check_auth(admin, password):
            session['admin'] = admin
            session['password'] = password
            return redirect(url_for('admin_home'))
        else:
            return redirect(url_for('admin_form'))

@app.route(Routes['alogin'])
def admin_login():
    post_url = Routes['aportal']
    error = None
    if 'error' in session:
        error = session.pop('error', None)
    logout()
    return render_template('admin/login.html',
                           type='Admin',
                           error=error,
                           route=Routes,
                           post_url=post_url)

def logged_in():
    logged = False
    if 'admin' in session and 'password' in session:
        logged = check_auth(session['admin'], session['password'])
    return logged

def logout():
    session.pop('admin', None)
    session.pop('password', None)
    return


