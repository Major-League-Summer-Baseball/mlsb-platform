from os.path import join
from flask import render_template, make_response, url_for, \
    redirect, session, request, Blueprint
from json import dumps
from datetime import date, time, datetime
from api.extensions import DB
from api.routes import Routes
from api.errors import InvalidField
from api.model import Team, Player, Sponsor, League, Game, Espys, Fun, \
    Division, JoinLeagueRequest, LeagueEvent, LeagueEventDate
from api.variables import BATS, FILES
from api.authentication import check_auth
from api.advanced.import_team import TeamList
from api.advanced.import_league import LeagueList


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
ALLOWED_EXTENSIONS = set(['csv'])
admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')
# -----------------------------------------------------------------------------


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@admin_blueprint.route("/import/team/list", methods=["POST"])
def import_team_list():
    results = {'errors': [], 'success': False, 'warnings': []}
    if not logged_in():
        results['errors'].append("Permission denied")
        return dumps(results)
    file = request.files['file']
    results = {'errors': [], 'success': False, 'warnings': []}
    if file and allowed_file(file.filename):
        content = (file.read()).decode("UTF-8")
        lines = content.replace("\r", "")
        lines = lines.split("\n")
        team = TeamList(lines)
        team.add_team_functional()
        results["warnings"] = team.warnings
        results["error"] = team.errors
        results['success'] = True
        if len(results['errors']) > 0:
            results['success'] = False
    else:
        s = "File format not accepted (csv)"
        raise InvalidField(payload={'detail': s})
    return dumps(results)


@admin_blueprint.route("/import/game/list", methods=["POST"])
def import_game_list():
    results = {'errors': [], 'success': False, 'warnings': []}
    if not logged_in():
        results['errors'].append("Permission denied")
        return dumps(results)
    file = request.files['file']
    if file and allowed_file(file.filename):
        content = (file.read()).decode("UTF-8")
        lines = content.replace("\r", "").replace("\ufeff", "")
        lines = lines.split("\n")
        team = LeagueList(lines)
        team.import_league_functional()
        results['errors'] = team.errors
        results['warnings'] = team.warnings
        results['success'] = True
        if len(results['errors']) > 0:
            results['success'] = False
    else:
        results['errors'] = "File should be a CSV"
        results['success'] = False
    return dumps(results)


@admin_blueprint.route("/edit/league_requests/<int:year>")
def view_league_requests(year):
    if not logged_in():
        return redirect(url_for('admin.login'))
    league_requests = JoinLeagueRequest.query.filter(
        JoinLeagueRequest.pending == True).all()
    league_requests = [request.json() for request in league_requests]
    return render_template("admin/joinLeagueRequests.html",
                           year=year,
                           route=Routes,
                           title="Players who request to join teams",
                           league_requests=league_requests)


@admin_blueprint.route(
    "/edit/league_requests/respond/<int:request_id>",
    methods=["POST"]
)
def respond_league_request(request_id):
    if not logged_in():
        return dumps(False)
    league_request = JoinLeagueRequest.query.get(request_id)
    if league_request is None:
        return dumps(False)
    accept = request.get_json()['accept']
    if accept:
        league_request.accept_request()
    else:
        league_request.decline_request()
    return dumps(True)


@admin_blueprint.route("/import/team")
def import_team():
    if not logged_in():
        return redirect(url_for('admin.login'))
    return render_template("admin/importForm.html",
                           year=date.today().year,
                           route=Routes,
                           title="Import Team from CSV",
                           template=url_for('admin.team_template'),
                           import_route=url_for('admin.import_team_list'),
                           type="Team")


@admin_blueprint.route("/import/game")
def import_game():
    if not logged_in():
        return redirect(url_for('admin.login'))
    return render_template("admin/importForm.html",
                           year=date.today().year,
                           route=Routes,
                           title="Import League's Game from CSV",
                           admin=session['admin'],
                           password=session['password'],
                           template=url_for('admin.game_template'),
                           import_route=url_for('admin.import_game_list'),
                           type="Games")


@admin_blueprint.route("/template/team")
def team_template():
    uploads = join(FILES, "team_template.csv")
    result = ""
    with open(uploads, "r") as f:
        for line in f:
            result += line
    response = make_response(result)
    s = "attachment; filename=team_template.csv"
    response.headers["Content-Disposition"] = s
    return response


@admin_blueprint.route("/template/game")
def game_template():
    uploads = join(FILES, "game_template.csv")
    result = ""
    with open(uploads, "r") as f:
        for line in f:
            result += line
    response = make_response(result)
    s = "attachment; filename=game_template.csv"
    response.headers["Content-Disposition"] = s
    return response


@admin_blueprint.route("/views/captains/<int:year>")
def get_captains_games_not_submitted(year):
    t1 = time(0, 0)
    t2 = time(23, 59)
    d1 = date(year, 1, 1)
    d2 = date.today()
    start = datetime.combine(d1, t1)
    end = datetime.combine(d2, t2)
    games = (DB.session.query(Game).filter(Game.date.between(start, end))
             ).order_by(Game.date)
    captains = []
    for game in games:
        away_bats = []
        home_bats = []
        for bat in game.bats:
            if bat.team_id == game.away_team_id:
                away_bats.append(bat)
            elif bat.team_id == game.home_team_id:
                home_bats.append(bat)
        if len(away_bats) == 0:
            team = Team.query.get(game.away_team_id)
            player = (Player.query.get(team.player_id))
            captains.append(player.name + "-" + player.email
                            + " on " + str(game.date))
        if len(home_bats) == 0:
            team = Team.query.get(game.home_team_id)
            player = (Player.query.get(team.player_id))
            captains.append(player.name + "-" + player.email
                            + " on " + str(game.date))
    return render_template("admin/viewGamesNotSubmitted.html",
                           route=Routes,
                           title="Captains with games to submit",
                           captains=captains,
                           year=year)


@admin_blueprint.route("/edit/roster/<int:year>/<int:team_id>")
def edit_roster(year, team_id):
    if not logged_in():
        return redirect(url_for('admin.login'))
    team = Team.query.get(team_id)
    if team is None:
        return render_template("admin/notFound.html",
                               route=Routes,
                               title="Team not found")
    else:
        players = []
        for player in team.players:
            players.append(player.json())
        players = quick_sort(players)
        all_players = Player.query.order_by(Player.name).all()
        non_roster = []
        for player in all_players:
            non_roster.append(player.json())
        return render_template("admin/editTeamRoster.html",
                               route=Routes,
                               title="Edit {} roster".format(str(team)),
                               players=players,
                               team_id=team_id,
                               non_roster=non_roster,
                               year=year)


def quick_sort(array):
    less = []
    equal = []
    greater = []
    if len(array) > 1:
        pivot = array[0]
        for x in array:
            if x['player_name'] < pivot['player_name']:
                less.append(x)
            if x['player_name'] == pivot['player_name']:
                equal.append(x)
            if x['player_name'] > pivot['player_name']:
                greater.append(x)
        # Don't forget to return something!
        # Just use the + operator to join lists
        return quick_sort(less) + equal + quick_sort(greater)
    # Note that you want equal ^^^^^ not pivot
    else:
        # You need to hande the part at the end of the recursion
        # when you only have one element in your array, just return the array.
        return array


@admin_blueprint.route("/edit/fun/<int:year>")
def edit_fun(year):
    if not logged_in():
        return redirect(url_for('admin.login'))
    return render_template("admin/editFun.html",
                           year=year,
                           route=Routes,
                           funs=get_funs(),
                           title="Edit Fun")


@admin_blueprint.route("/edit/league-event/<int:year>")
def edit_league_event(year):
    if not logged_in():
        return redirect(url_for('admin.login'))
    events = [event.json() for event in LeagueEvent.query.all()]
    return render_template("admin/editLeagueEvent.html",
                           year=year,
                           route=Routes,
                           events=events,
                           title="Edit League Events")


@admin_blueprint.route("/edit/league-event/<int:year>/<int:league_event_id>")
def edit_league_event_date(year, league_event_id):
    if not logged_in():
        return redirect(url_for('admin.login'))
    query = LeagueEventDate.query
    dates = [
        d.json()
        for d in query.filter(
            LeagueEventDate.league_event_id == league_event_id
        ).all()
    ]
    return render_template("admin/editLeagueEventDate.html",
                           year=year,
                           route=Routes,
                           event=LeagueEvent.query.get(league_event_id).json(),
                           dates=dates,
                           title="Edit League Event Dates")


attendance_route = "/<int:year>/attendance/<int:league_event_date_id>"


@admin_blueprint.route(
    "/edit/league-event/<int:year>/attendance/<int:league_event_date_id>"
)
def league_event_date_attendance(year, league_event_date_id):
    if not logged_in():
        return redirect(url_for('admin.login'))
    event = LeagueEventDate.query.get(league_event_date_id)
    players = [player.admin_json() for player in event.players]
    return render_template("admin/editLeagueEventAttendance.html",
                           year=year,
                           route=Routes,
                           event=event.json(),
                           players=players,
                           title="League Event Attendance")


@admin_blueprint.route("/edit/division/<int:year>")
def edit_division(year):
    if not logged_in():
        return redirect(url_for('admin.login'))
    return render_template("admin/editDivision.html",
                           year=year,
                           route=Routes,
                           divisions=get_divisions(),
                           title="Edit Division")


@admin_blueprint.route("/edit/league/<int:year>")
def edit_league(year):
    if not logged_in():
        return redirect(url_for('admin.login'))
    return render_template("admin/editLeague.html",
                           year=year,
                           route=Routes,
                           leagues=get_leagues(),
                           title="Edit Leagues")


@admin_blueprint.route("/edit/sponsor/<int:year>")
def edit_sponsor(year):
    if not logged_in():
        return redirect(url_for('admin.login'))
    return render_template("admin/editSponsor.html",
                           year=year,
                           route=Routes,
                           sponsors=get_sponsors(),
                           not_active=get_sponsors(active=False),
                           title="Edit Leagues")


@admin_blueprint.route("")
def _general_home():
    if not logged_in():
        return redirect(url_for('admin.login'))
    year = date.today().year
    return redirect(url_for("admin.home", year=year))


@admin_blueprint.route("/<int:year>")
def home(year):
    if not logged_in():
        return redirect(url_for('admin.login'))
    return render_template("admin/index.html",
                           year=year,
                           route=Routes,
                           title="Admin")


@admin_blueprint.route("/edit/player/<int:year>")
def edit_player(year):
    if not logged_in():
        return redirect(url_for('admin.login'))
    players = get_players()
    return render_template("admin/editPlayer.html",
                           year=year,
                           route=Routes,
                           players=players,
                           title="Edit Players")


@admin_blueprint.route("/edit/non_active_players/<int:year>")
def non_active_players(year):
    if not logged_in():
        return redirect(url_for('admin.login'))
    players = get_players(active=False)
    return render_template("admin/nonActivePlayers.html",
                           year=year,
                           route=Routes,
                           players=players,
                           title="Activate Old Players")


@admin_blueprint.route("/edit/team/<int:year>")
def edit_team(year):
    if not logged_in():
        return redirect(url_for('admin.login'))
    results = Team.query.filter(Team.year == year).all()
    # results = Team.query.all()
    teams = []
    for team in results:
        teams.append(team.json())
    return render_template("admin/editTeam.html",
                           year=year,
                           route=Routes,
                           teams=teams,
                           title="Edit Teams",
                           sponsors=get_sponsors(),
                           leagues=get_leagues())


@admin_blueprint.route("/edit/game/<int:year>")
def edit_game(year):
    if not logged_in():
        return redirect(url_for('admin.login'))
    results = Team.query.filter(Team.year == year).all()
    leagues = get_leagues()
    divisions = get_divisions()
    teams = []
    for league in leagues:
        while len(teams) < league['league_id'] + 1:
            teams.append([])
    for team in results:
        if team.league_id is not None:
            t = team.json()
            t['team_name'] = str(team)
            teams[team.league_id].append(t)
    d1 = date(year, 1, 1)
    d2 = date(year, 12, 31)
    results = Game.query.filter(Game.date.between(d1, d2)).all()
    games = []
    for game in results:
        games.append(game.json())
    return render_template("admin/editGame.html",
                           year=year,
                           route=Routes,
                           teams=teams,
                           title="Edit Game",
                           leagues=leagues,
                           divisions=divisions,
                           games=games)


@admin_blueprint.route("/edit/player/deactivate/<int:year>/<int:player_id>")
def activate_player(year, player_id):
    if not logged_in():
        return redirect(url_for('admin.login'))
    player = Player.query.get(player_id)
    if player is None:
        return render_template("admin/notFound.html",
                               route=Routes,
                               year=year,
                               title="Player not found"
                               )
    return render_template("admin/activatePlayer.html",
                           year=year,
                           player=player.json(),
                           route=Routes,
                           title="Activate/Deactivate Player")


@admin_blueprint.route(
    "/edit/player/deactivate/<int:year>/<int:player_id>",
    methods=["POST"]
)
def activate_player_post(year, player_id):
    if not logged_in():
        return dumps(False)
    player = Player.query.get(player_id)
    if player is None:
        return dumps(False)
    activate = request.get_json()['active']
    if activate:
        player.activate()
    else:
        player.deactivate()
    DB.session.commit()
    return dumps(True)


@admin_blueprint.route("/edit/sponsor/deactivate/<int:year>/<int:sponsor_id>")
def activate_sponsor(year, sponsor_id):
    if not logged_in():
        return redirect(url_for('admin.login'))
    sponsor = Sponsor.query.get(sponsor_id)
    if sponsor is None:
        return render_template("admin/notFound.html",
                               route=Routes,
                               year=year,
                               title="Sponsor not found"
                               )
    return render_template("admin/activateSponsor.html",
                           year=year,
                           sponsor=sponsor.json(),
                           route=Routes,
                           title="Activate/Deactivate Sponsor")


@admin_blueprint.route(
    "/edit/sponsor/deactivate/<int:year>/<int:sponsor_id>",
    methods=["POST"]
)
def activate_sponsor_post(year, sponsor_id):
    if not logged_in():
        return dumps(False)
    sponsor = Sponsor.query.get(sponsor_id)
    if sponsor is None:
        return dumps(False)
    activate = request.get_json()['active']
    if activate:
        sponsor.activate()
    else:
        sponsor.deactivate()
    DB.session.commit()
    return dumps(True)


@admin_blueprint.route("/edit/espys/<int:year>/<int:team_id>")
def edit_espys(year, team_id):
    if not logged_in():
        return redirect(url_for('admin.login'))
    espys = Espys.query.filter(Espys.team_id == team_id).all()
    result = []
    for espy in espys:
        result.append(espy.json())
    return render_template("admin/editEspys.html",
                           year=year,
                           route=Routes,
                           espys=result,
                           team_id=team_id,
                           title="Edit Espys",
                           sponsors=get_sponsors(True))


@admin_blueprint.route("/edit/bat/<int:year>/<int:game_id>")
def edit_bat(year, game_id):
    if not logged_in():
        return redirect(url_for('admin.login'))
    game = Game.query.get(game_id)
    results = game.bats
    away_team_id = game.away_team_id
    home_team_id = game.home_team_id
    if game is None:
        return render_template("admin/notFound.html",
                               route=Routes,
                               title="Game not found",
                               year=year
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
                           game=str(game),
                           players=get_players(),
                           BATS=BATS)


@admin_blueprint.route("/logout")
def logout():
    _logout()
    return redirect(url_for('website.reroute'))


@admin_blueprint.route("/portal", methods=['POST'])
def portal():
    if 'admin' in session and 'password' in session:
        admin = session['admin']
        password = session['password']
    else:
        admin = request.form.get('admin')
        password = request.form.get('password')
    if check_auth(admin, password):
        session['admin'] = admin
        session['password'] = password
        return redirect(url_for('admin.home', year=date.today().year))
    else:
        session['error'] = 'INVALID CREDENTIALS'
        return redirect(url_for('admin.login'))


@admin_blueprint.route("/login")
def login():
    post_url = url_for('admin.portal')
    error = None
    if 'error' in session:
        error = session.pop('error', None)
    _logout()
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


def _logout():
    session.pop('admin', None)
    session.pop('password', None)
    return


def get_sponsors(active=True):
    results = (Sponsor.query.filter(Sponsor.active == active).order_by("name")
               ).all()
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


def get_funs():
    results = Fun.query.all()
    return [fun.json() for fun in results]


def get_divisions():
    results = Division.query.all()
    return [division.json() for division in results]


def get_players(active=True):
    results = (Player.query.filter(Player.active == active).order_by("name")
               ).all()
    players = []
    for player in results:
        players.append(player.admin_json())

    return players


def get_team_players(team_id):
    team = Team.query.get(team_id)
    players = []
    for player in team.players:
        players.append(player.json())
    return players
