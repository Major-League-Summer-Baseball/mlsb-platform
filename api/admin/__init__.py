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
from api.model import Team, Player, Sponsor, League,Game
from api.variables import SPONSORS
from api.authentication import check_auth
from api.model import Player

@app.route(Routes['editleague'])
def admin_edit_league():
    if not logged_in():
        return redirect(url_for('admin_login'))
    return render_template("admin/editLeague.html",
                           route=Routes,
                           leagues=get_leagues(),
                           title="Edit Leagues",
                           admin=session['admin'],
                           password=session['password'])

@app.route(Routes['editsponsor'])
def admin_edit_sponsor():
    if not logged_in():
        return redirect(url_for('admin_login'))
    return render_template("admin/editSponsor.html",
                           route=Routes,
                           sponsors=get_sponsors(),
                           title="Edit Leagues",
                           admin=session['admin'],
                           password=session['password'])

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

@app.route(Routes['editteam'])
def admin_edit_team():
    if not logged_in():
        return redirect(url_for('admin_login'))
    results = Team.query.all()
    teams = []
    for team in results:
        teams.append(team.json())
    return render_template("admin/editTeam.html",
                           route=Routes,
                           teams=teams,
                           title="Edit Teams",
                           admin=session['admin'],
                           password=session['password'],
                           sponsors=get_sponsors(),
                           leagues=get_leagues())

@app.route(Routes['editgame'])
def admin_edit_game():
    if not logged_in():
        return redirect(url_for('admin_login'))
    results = Team.query.all()
    leagues = get_leagues()
    teams = []
    for league in leagues:
        while len(teams) < league['league_id'] + 1:
            teams.append([])
    for team in results:
        print(team)
        print(team.league_id)
        
        if team.league_id is not None:
            t = team.json()
            t['team_name'] = str(team)
            teams[team.league_id].append(t)
    print(teams)
    results = Game.query.all()
    games = []
    for game in results:
        games.append(game.json())
    return render_template("admin/editGame.html",
                           route=Routes,
                           teams=teams,
                           title="Edit Game",
                           admin=session['admin'],
                           password=session['password'],
                           leagues=get_leagues(),
                           games=games)

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

def get_sponsors():
    results = Sponsor.query.all()
    sponsors = []
    for sponsor in results:
        sponsors.append(sponsor.json())
    return sponsors

def get_leagues():
    results = League.query.all()
    leagues = []
    for league in results:
        leagues.append(league.json())
    return leagues

