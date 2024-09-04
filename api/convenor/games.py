from flask import render_template, request, session, url_for, redirect, \
    make_response, flash
from sqlalchemy import or_, and_
from datetime import date, time, datetime
from api.importers.league import LeagueList
from api.authentication import require_to_be_convenor
from api.cached_items import handle_table_change
from api.extensions import DB
from api.tables import Tables
from api.variables import FILES, BATS
from api.convenor import allowed_file, convenor_blueprint, is_empty, \
    normalize_field
from api.model import Game, Team, Division, League, Player, Bat
from os import path


@convenor_blueprint.route("games/new/<int:league_id>")
@require_to_be_convenor
def new_game_page(league_id: int):
    league = League.query.get(league_id)
    if league is None:
        session['error'] = f"League does not exist {league_id}"
        return redirect(url_for('convenor.error_page'))
    teams = [
        team.json()
        for team in Team.query.filter(
            and_(Team.league_id == league_id, Team.year == date.today().year)
        ).all()
    ]
    teams.sort(key=lambda t: t['team_name'].strip())
    game_data = {
        "home_team_id": None,
        "away_team_id": None,
        "home_bats": [],
        "away_bats": [],
        "division_id": None,
        "game_id": None,
        "date": "",
        "time": "",
        "status": "",
        "field": ""
    }
    divisions = [
        division.json()
        for division in Division.query.all()
    ]
    return render_template(
        "convenor/game.html",
        game=game_data,
        teams=teams,
        divisions=divisions,
        league=league.json(),
        bats=BATS
    )


@convenor_blueprint.route(
    "games/<int:game_id>", methods=["GET", "POST", "DELETE"]
)
@require_to_be_convenor
def edit_game_page(game_id: int):
    game = Game.query.get(game_id)
    if game is None:
        session['error'] = f"Game does not exist {game_id}"
        return redirect(url_for('convenor.error_page'))
    game_data = game.json()

    away_team = Team.query.get(game.away_team_id)
    away_players = [
        Player.get_unassigned_player().json()
    ] + ([] if away_team is None else [
        player.json() for player in away_team.players
    ])
    away_players.sort(key=lambda player: player['player_name'])
    game_data['away_score'] = game.away_team_score
    game_data['away_players'] = away_players
    game_data['away_bats'] = [
        bat.json()
        for bat in game.get_team_bats(game.away_team_id)
    ]

    home_team = Team.query.get(game.home_team_id)
    home_players = [
        Player.get_unassigned_player().json()
    ] + ([] if home_team is None else [
        player.json() for player in home_team.players
    ])
    home_players.sort(key=lambda player: player['player_name'])
    game_data['home_score'] = game.home_team_score
    game_data['home_bats'] = [
        bat.json()
        for bat in game.get_team_bats(game.home_team_id)
    ]
    game_data['home_players'] = home_players
    teams = [
        team.json()
        for team in Team.query.filter(
            and_(Team.league_id == game.league_id, Team.year == game.date.year)
        ).all()
    ]
    teams.sort(key=lambda t: t['team_name'].strip())
    divisions = [division.json() for division in Division.query.all()]
    league = League.query.get(game.league_id)
    return render_template(
        "convenor/game.html",
        game=game_data,
        divisions=divisions,
        teams=teams,
        bats=BATS,
        league=league.json()
    )


@convenor_blueprint.route("games", methods=["DELETE", "GET", "POST"])
@require_to_be_convenor
def games_page():
    year = int(request.args.get('year', date.today().year))
    team_id = request.args.get('team_id', None)
    pending_score = request.args.get('pending_score', "off") == "on"

    start = datetime.combine(date(year, 1, 1), time(0, 0))
    end = datetime.combine(date(year, 12, 30), time(23, 59))
    games = Game.query.filter(Game.date.between(start, end))
    teams = teams = [
        team.json()
        for team in Team.query.filter(Team.year == year).all()
    ]
    teams.sort(key=lambda t: t['team_name'].strip())
    if is_empty(team_id):
        team_id = None
    else:
        team_id = int(team_id)
        games = games.filter(or_(
            Game.away_team_id == team_id,
            Game.home_team_id == team_id
        ))
    if pending_score:
        games = games.filter(or_(
            Game.away_team_hits == 0,
            Game.home_team_hits == 0)
        )
    games = [game.json() for game in games.order_by(Game.date).all()]
    years = [year for year in range(2016, date.today().year + 1)]
    leagues = [league.json() for league in League.query.all()]
    return render_template(
        "convenor/games.html",
        games=games,
        teams=teams,
        years=years,
        leagues=leagues,
        selected_year=year,
        team_id=team_id,
        template=url_for('convenor.game_template'),
        pending_score=pending_score
    )


@convenor_blueprint.route("games/submit", methods=["POST"])
@require_to_be_convenor
def submit_game():
    """Submit edit/create a game."""
    home_team_id = int(request.form.get("home_team_id"))
    away_team_id = int(request.form.get("away_team_id"))
    league_id = int(request.form.get("league_id"))
    division_id = int(request.form.get("division_id"))
    date_str = request.form.get("date")
    time_str = request.form.get("time")
    status = normalize_field(request.form.get("status", None))
    field = request.form.get("field")
    game_id = request.form.get("game_id", None)
    try:
        if is_empty(game_id):
            game = Game(
                date_str,
                time_str,
                home_team_id,
                away_team_id,
                league_id,
                division_id,
                status=status,
                field=field
            )
            DB.session.add(game)
            flash("Game created")
            handle_table_change(Tables.GAME)
        else:
            game = Game.query.get(game_id)
            if game is None:
                session['error'] = f"Game does not exist {game_id}"
                return redirect(url_for('convenor.error_page'))
            game.update(
                date=date_str,
                time=time_str,
                home_team_id=home_team_id,
                away_team_id=away_team_id,
                league_id=league_id,
                division_id=division_id,
                status=status,
                field=field
            )
            flash("Game updated")
            handle_table_change(Tables.GAME)
    except Exception as e:
        session['error'] = str(e)
        return redirect(url_for('convenor.error_page'))
    DB.session.commit()
    return redirect(url_for("convenor.edit_game_page", game_id=game.id))


@convenor_blueprint.route(
    "games/<int:game_id>/team/<int:team_id>/bat", methods=["POST"]
)
@require_to_be_convenor
def submit_bat(game_id: int, team_id: int):
    """Submit edit/create a game."""
    player_id = int(request.form.get("player_id"))
    rbi = int(request.form.get("rbi"))
    inning = int(request.form.get("inning"))
    hit = request.form.get('hit')
    try:
        bat = Bat(
            player_id,
            team_id,
            game_id,
            hit,
            inning=inning,
            rbi=rbi
        )
        DB.session.add(bat)
        flash("Bat created")
        handle_table_change(Tables.BAT)
    except Exception as e:
        session['error'] = str(e)
        return redirect(url_for('convenor.error_page'))
    DB.session.commit()
    return redirect(url_for("convenor.edit_game_page", game_id=game_id))


@convenor_blueprint.route("games/<int:game_id>/delete", methods=["DELETE"])
@require_to_be_convenor
def delete_game(game_id: int):
    """Delete a game."""
    game = Game.query.get(game_id)
    if game is None:
        session['error'] = f"Game does not exist {game_id}"
        return redirect(url_for('convenor.error_page'))
    if game.bats.first() is not None:
        session['error'] = f"Please remove bats before deleting game {game_id}"
        return redirect(url_for('convenor.error_page'))
    DB.session.delete(game)
    DB.session.commit()
    flash("Game was removed")
    handle_table_change(Tables.GAME)
    return redirect(url_for("convenor.games_page"))


@convenor_blueprint.route(
    "games/<int:game_id>/bat/<int:bat_id>", methods=["DELETE"]
)
@require_to_be_convenor
def delete_bat(game_id: int, bat_id: int):
    """Delete a bat from the given game."""
    bat = Bat.query.get(bat_id)
    if bat is None:
        session['error'] = f"Bat does not exist {bat_id}"
        return redirect(url_for('convenor.error_page'))
    DB.session.delete(bat)
    DB.session.commit()
    handle_table_change(Tables.BAT)
    return redirect(url_for("convenor.edit_game_page", game_id=game_id))


@convenor_blueprint.route("games/template")
@require_to_be_convenor
def game_template():
    uploads = path.join(FILES, "game_template.csv")
    result = ""
    with open(uploads, "r") as f:
        for line in f:
            result += line
    response = make_response(result)
    s = "attachment; filename=team_template.csv"
    response.headers["Content-Disposition"] = s
    return response


@convenor_blueprint.route("games/template/submit", methods=["POST"])
@require_to_be_convenor
def submit_game_template():
    file = request.files['file']

    if not file or not allowed_file(file.filename):
        session['error'] = "File format not accepted (use csv)"
        return redirect(url_for('convenor.error_page'))

    content = (file.read()).decode("UTF-8")
    lines = content.replace("\r", "")
    lines = lines.split("\n")

    try:
        games = LeagueList(lines)
        games.import_league_functional()
        if len(games.errors) > 0:
            session['error'] = ",".join(games.errors)
            return redirect(url_for('convenor.error_page'))
        if len(games.warnings) > 0:
            flash(",".join(games.warnings))
        else:
            flash("Games added!")
            handle_table_change(Tables.GAME)
    except Exception as e:
        session['error'] = str(e)
        return redirect(url_for('convenor.error_page'))
    return redirect(url_for('convenor.games_page'))
