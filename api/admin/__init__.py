'''
Name: Dallas Fraser
Date: 2014-08-25
Project: MLSB API
Purpose: Holds the routes for the admin side
'''
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from os.path import join
from flask.ext.restful import Resource, reqparse
from flask import Response, render_template, make_response
from json import dumps
from api.routes import Routes
from api import app, PICTURES
from api.routes import Routes
from flask import render_template, send_file, url_for, send_from_directory,\
                  redirect, session, request, make_response
from api.model import Team, Player, Sponsor, League, Game, Bat
from api.variables import SPONSORS, BATS
from api.authentication import check_auth
from api.model import Player
from datetime import date
from api.advanced.import_team import TeamList
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
ALLOWED_EXTENSIONS = set(['csv'])
# -----------------------------------------------------------------------------


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route(Routes['import_team_list'], methods=["POST"])
def admin_import_team_list():
    results = {'errors': [], 'success':False, 'warnings': []}
    if not logged_in():
        results['errors'].append("Permission denied")
        return dumps(results)
    file = request.files['file']
    if file and allowed_file(file.filename):
        content = (file.read()).decode("UTF-8")
        print(content)
        lines = content.replace("\r", "")
        lines = lines.split("\n")
        team = TeamList(lines)
        team.import_team()
        results['errors'] = team.errors
        results['warnings'] = team.warnings
        results['success'] = True
        if len(results['errors']) > 0:
            results['success'] = False
        return dumps(results)

@app.route(Routes['importteam'])
def admin_import_team():
    if not logged_in():
        return redirect(url_for('admin_login'))
    return render_template("admin/importTeam.html",
                           year=date.today().year,
                           route=Routes,
                           title="Import Team from CSV",
                           admin=session['admin'],
                           password=session['password'])

@app.route(Routes['importgame'])
def admin_import_game():
    if not logged_in():
        return redirect(url_for('admin_login'))
    return render_template("admin/importGame.html",
                           year=date.today().year,
                           route=Routes,
                           title="Import Game from CSV",
                           admin=session['admin'],
                           password=session['password'])

@app.route(Routes['importbat'])
def admin_import_bat():
    if not logged_in():
        return redirect(url_for('admin_login'))
    return render_template("admin/importBat.html",
                           year=date.today().year,
                           route=Routes,
                           title="Import Game Scores from CSV",
                           admin=session['admin'],
                           password=session['password'])

@app.route(Routes['team_template'])
def admin_team_template():
    print(app.root_path)
    uploads = join(app.root_path, "static", "files", "team_template.csv")
    result = ""
    with open (uploads, "r") as f:
        for line in f:
            result += line
    print(result)
    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename=team_template.csv"
    return response

@app.route(Routes['game_template'])
def admin_game_template():
    print(app.root_path)
    uploads = join(app.root_path, "static", "files", "game_template.csv")
    result = ""
    with open (uploads, "r") as f:
        for line in f:
            result += line
    print(result)
    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename=game_template.csv"
    return response

@app.route(Routes['bat_template'])
def admin_bat_template():
    print(app.root_path)
    uploads = join(app.root_path, "static", "files", "bat_template.csv")
    result = ""
    with open (uploads, "r") as f:
        for line in f:
            result += line
    print(result)
    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename=bat_template.csv"
    return response

@app.route(Routes['editroster'] + "/<int:year>" + "/<int:team_id>")
def admin_edit_roster(year, team_id):
    if not logged_in():
        return redirect(url_for('admin_login'))
    
@app.route(Routes['editleague'] + "/<int:year>")
def admin_edit_league(year):
    if not logged_in():
        return redirect(url_for('admin_login'))
    return render_template("admin/editLeague.html",
                           year=year,
                           route=Routes,
                           leagues=get_leagues(),
                           title="Edit Leagues",
                           admin=session['admin'],
                           password=session['password'])

@app.route(Routes['editsponsor']+ "/<int:year>")
def admin_edit_sponsor(year):
    if not logged_in():
        return redirect(url_for('admin_login'))
    return render_template("admin/editSponsor.html",
                           year=year,
                           route=Routes,
                           sponsors=get_sponsors(),
                           title="Edit Leagues",
                           admin=session['admin'],
                           password=session['password'])

@app.route(Routes['aindex'] + "/<int:year>")
def admin_home(year):
    if not logged_in():
        return redirect(url_for('admin_login'))
    return render_template("admin/index.html",
                           year=year,
                           route=Routes,
                           title="Admin")

@app.route(Routes['editplayer'] + "/<int:year>")
def admin_edit_player(year):
    if not logged_in():
        return redirect(url_for('admin_login'))
    results = Player.query.all()
    players = []
    for player in results:
        players.append(player.json())
    return render_template("admin/editPlayer.html",
                           year=year,
                           route=Routes,
                           players=players,
                           title="Edit Players",
                           admin=session['admin'],
                           password=session['password'])

@app.route(Routes['editteam'] + "/<int:year>")
def admin_edit_team(year):
    if not logged_in():
        return redirect(url_for('admin_login'))
    results = Team.query.filter(Team.year==year).all()
    #results = Team.query.all()
    teams = []
    for team in results:
        teams.append(team.json())
    return render_template("admin/editTeam.html",
                           year=year,
                           route=Routes,
                           teams=teams,
                           title="Edit Teams",
                           admin=session['admin'],
                           password=session['password'],
                           sponsors=get_sponsors(),
                           leagues=get_leagues())

@app.route(Routes['editgame'] + "/<int:year>")
def admin_edit_game(year):
    if not logged_in():
        return redirect(url_for('admin_login'))
    results = Team.query.all()
    leagues = get_leagues()
    teams = []
    for league in leagues:
        while len(teams) < league['league_id'] + 1:
            teams.append([])
    for team in results:
        if team.league_id is not None:
            t = team.json()
            t['team_name'] = str(team)
            teams[team.league_id].append(t)
    results = Game.query.all()
    games = []
    for game in results:
        games.append(game.json())
    return render_template("admin/editGame.html",
                           year=year,
                           route=Routes,
                           teams=teams,
                           title="Edit Game",
                           admin=session['admin'],
                           password=session['password'],
                           leagues=get_leagues(),
                           games=games)

@app.route(Routes['editbat'] + "/<int:year>" + "/<int:game_id>")
def admin_edit_bat(year, game_id):
    if not logged_in():
        return redirect(url_for('admin_login'))
    game = Game.query.get(game_id)
    results = game.bats
    away_team_id = game.away_team_id
    home_team_id = game.home_team_id
    if game is None:
        return render_template("admin/notFound.html",
                               route=Routes,
                               title="Game not found",
                               admin=session['admin'],
                               password=session['password'],
                               )
    away_bats = []
    home_bats = []
    for bat in results:
        if bat.team_id == game.home_team_id:
            home_bats.append(bat.json())
        elif bat.team_id == game.away_team_id:
            away_bats.append(bat.json())
    away_players = get_team_players(game.away_team_id)
    home_players = get_team_players(game.home_team_id)
    return render_template("admin/editBat.html",
                           year=year,
                           game_id=game_id,
                           route=Routes,
                           away_bats=away_bats,
                           home_bats=home_bats,
                           home_players=home_players,
                           away_players=away_players,
                           away_team_id=away_team_id,
                           home_team_id=home_team_id,
                           title="Edit Bats",
                           admin=session['admin'],
                           password=session['password'],
                           game=str(game),
                           players=get_players(),
                           BATS=BATS)

@app.route(Routes['alogout'])
def admin_logout():
    logout()
    return redirect(url_for('index'))

@app.route(Routes['aportal'], methods=['POST'])
def admin_portal():
    if 'admin' in session and 'password' in session:
        return redirect(url_for('admin_form'))
    else:
        admin = request.form.get('admin')
        password = request.form.get('password')
        if check_auth(admin, password):
            session['admin'] = admin
            session['password'] = password
            return redirect(url_for('admin_home', year=date.today().year))
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

def get_players():
    results = Player.query.all()
    players = []
    for player in results:
        players.append(player.json())
    return players

def get_team_players(team_id):
    team = Team.query.get(team_id)
    players = []
    for player in team.players:
        players.append(player.json())
    return players
