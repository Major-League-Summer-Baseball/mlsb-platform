from flask import render_template, request, session, url_for, redirect, \
    make_response, flash
from api.importers.team import TeamList
from api.extensions import DB
from api.models.join_league_request import JoinLeagueRequest
from api.variables import FILES
from api.authentication import require_to_be_convenor
from api.cached_items import handle_table_change
from api.convenor import allowed_file, convenor_blueprint, is_empty, get_int
from api.model import Team, League, Sponsor, Espys
from api.tables import Tables
from datetime import date
from os import path


def team_has_games(team: Team) -> bool:
    """Does the team have any games."""
    return (
        team.away_games.first() is not None or
        team.home_games.first() is not None
    )


@convenor_blueprint.route("teams", methods=["DELETE", "GET", "POST"])
@require_to_be_convenor
def teams_page():
    year = int(request.args.get('year', date.today().year))
    league_id = request.args.get('league_id', None)

    team_query = Team.query.filter(Team.year == year)
    if is_empty(league_id):
        league_id = None
    else:
        league_id = int(league_id)
        team_query = team_query.filter(Team.league_id == league_id)
    teams = [
        team.json()
        for team in team_query.order_by(Team.year).all()
    ]
    teams.sort(key=lambda t: t['team_name'].strip())
    years = [year for year in range(2015, date.today().year + 1)]
    return render_template(
        "convenor/teams.html",
        teams=teams,
        league_id=league_id,
        leagues=[league.json() for league in League.query.all()],
        selected_year=year,
        template=url_for('convenor.team_template'),
        years=years
    )


@convenor_blueprint.route("team/new")
@require_to_be_convenor
def new_team_page():
    year = int(request.args.get('year', date.today().year))
    team = {
        'team_id': None,
        'sponsor_id': None,
        'color': '',
        'year': year,
        'captain': None
    }
    players = []
    espys = []
    leagues = [league.json() for league in League.query.all()]
    return render_template(
        "convenor/team.html",
        team=team,
        espys=espys,
        players=players,
        leagues=leagues,
        sponsors=[sponsor.json() for sponsor in Sponsor.query.all()]
    )


@convenor_blueprint.route(
    "team/<int:team_id>", methods=["DELETE", "GET", "POST"]
)
@require_to_be_convenor
def edit_team_page(team_id: int):
    team = Team.query.get(team_id)
    players = [player.admin_json() for player in team.players]
    espys = [espy.json() for espy in team.espys]
    leagues = [league.json() for league in League.query.all()]
    return render_template(
        "convenor/team.html",
        team=team.json(),
        espys=espys,
        leagues=leagues,
        players=players,
        has_games=team_has_games(team),
        sponsors=[sponsor.json() for sponsor in Sponsor.query.all()]
    )


@convenor_blueprint.route(
    "team/<int:team_id>/delete", methods=["DELETE"]
)
def remove_team(team_id: int):
    """Delete the team."""
    try:
        team = Team.query.get(team_id)

        if team is None:
            session['error'] = f"Team does not exist {team_id}"
            return redirect(url_for('convenor.error_page'))
        if team_has_games(team):
            tid = team_id
            session['error'] = f"Please edit/remove games involving team {tid}"
            return redirect(url_for('convenor.error_page'))

        # clean up certain team data
        for espys in team.espys:
            DB.session.delete(espys)
        team_requests = JoinLeagueRequest.query.filter(
            JoinLeagueRequest.team_id == team_id
        ).all()
        for team_request in team_requests:
            DB.session.delete(team_request)

        DB.session.delete(team)
        DB.session.commit()
    except Exception as e:
        session['error'] = str(e)
        return redirect(url_for('convenor.error_page'))
    flash("Team was removed")
    handle_table_change(Tables.TEAM)
    return redirect(url_for("convenor.teams_page"))


@convenor_blueprint.route("team/submit", methods=["POST"])
@require_to_be_convenor
def submit_team():
    """Add/update team"""
    league_id = int(request.form.get("league_id"))
    sponsor_id = int(request.form.get("sponsor_id"))
    year = int(request.form.get("year"))
    color = request.form.get("color")
    team_id = request.form.get("team_id", None)
    image_id = request.form.get('image_id', None)
    try:
        if is_empty(team_id):
            team = Team(
                color=color,
                sponsor_id=sponsor_id,
                league_id=league_id,
                year=year,
                image_id=image_id
            )
            DB.session.add(team)
            flash("Team created")
            handle_table_change(Tables.TEAM)
        else:
            team = Team.query.get(team_id)
            if team is None:
                session['error'] = f"Team does not exist {team_id}"
                return redirect(url_for('convenor.error_page'))
            team.update(
                color=color,
                sponsor_id=sponsor_id,
                league_id=league_id,
                year=year,
                image_id=image_id
            )
            flash("Team updated")
            handle_table_change(Tables.TEAM)
    except Exception as e:
        session['error'] = str(e)
        return redirect(url_for('convenor.error_page'))
    DB.session.commit()
    return redirect(url_for("convenor.edit_team_page", team_id=team.id))


@convenor_blueprint.route(
    "team/<int:team_id>/player",
    methods=["POST"]
)
@require_to_be_convenor
def add_player_team_form(team_id: int):
    """Add player to team use a request form."""
    return add_player_team(team_id, int(request.form.get('player_id')), 0)


@convenor_blueprint.route(
    "team/<int:team_id>/player/<int:player_id>/<int:captain>",
    methods=["POST"]
)
@require_to_be_convenor
def add_player_team(team_id: int, player_id: int, captain: int):
    """Remove/Add player from/to the given team"""
    try:
        team = Team.query.get(team_id)
        if team is None:
            session['error'] = f"Team does not exist {team_id}"
            return redirect(url_for('convenor.error_page'))
        team.insert_player(player_id, captain=captain > 0)
        flash("Player added to team")
    except Exception as e:
        session['error'] = str(e)
        return redirect(url_for('convenor.error_page'))
    DB.session.commit()
    return redirect(url_for("convenor.edit_team_page", team_id=team_id))


@convenor_blueprint.route(
    "team/<int:team_id>/player/<int:player_id>", methods=["DELETE"]
)
@require_to_be_convenor
def remove_player_team(team_id: int, player_id: int):
    """Remove/Add player from/to the given team"""
    try:
        team = Team.query.get(team_id)
        if team is None:
            session['error'] = f"Team does not exist {team_id}"
            return redirect(url_for('convenor.error_page'))
        team.remove_player(player_id)
        flash("Player removed from team")
    except Exception as e:
        session['error'] = str(e)
        return redirect(url_for('convenor.error_page'))
    DB.session.commit()
    return redirect(url_for("convenor.edit_team_page", team_id=team_id))


@convenor_blueprint.route(
    "team/<int:team_id>/espys/<int:espy_id>", methods=["DELETE"]
)
@require_to_be_convenor
def remove_team_espy(team_id: int, espy_id: int):
    """Remove espy from given team"""
    try:
        team = Team.query.get(team_id)
        espys = Espys.query.get(espy_id)
        if team is None:
            session['error'] = f"Team does not exist {team_id}"
            return redirect(url_for('convenor.error_page'))
        if espys is None:
            session['error'] = f"Espy does not exist {espy_id}"
            return redirect(url_for('convenor.error_page'))
        DB.session.delete(espys)
        flash("Espys removed from team")
    except Exception as e:
        session['error'] = str(e)
        return redirect(url_for('convenor.error_page'))
    DB.session.commit()
    return redirect(url_for("convenor.edit_team_page", team_id=team_id))


@convenor_blueprint.route(
    "team/<int:team_id>/espys", methods=["POST"]
)
@require_to_be_convenor
def add_team_espy(team_id: int):
    """Remove/Add player from/to the given team"""
    try:
        sponsor_id = get_int(request.form.get("sponsor_id", None))
        description = request.form.get("description", None)
        points = float(request.form.get('points', 0.0))
        receipt = request.form.get('receipt', None)
        time = request.form.get('time', None)
        date = request.form.get('date', None)

        team = Team.query.get(team_id)
        if team is None:
            session['error'] = f"Team does not exist {team_id}"
            return redirect(url_for('convenor.error_page'))
        espy = Espys(
            team_id,
            sponsor_id=sponsor_id,
            description=description,
            points=points,
            receipt=receipt,
            time=time,
            date=date
        )
        DB.session.add(espy)
        flash("Espy added to team")
    except Exception as e:
        session['error'] = str(e)
        return redirect(url_for('convenor.error_page'))
    DB.session.commit()
    return redirect(url_for("convenor.edit_team_page", team_id=team_id))


@convenor_blueprint.route("teams/template")
@require_to_be_convenor
def team_template():
    uploads = path.join(FILES, "team_template.csv")
    result = ""
    with open(uploads, "r") as f:
        for line in f:
            result += line
    response = make_response(result)
    s = "attachment; filename=team_template.csv"
    response.headers["Content-Disposition"] = s
    return response


@convenor_blueprint.route("teams/template/submit", methods=["POST"])
@require_to_be_convenor
def submit_team_template():
    file = request.files['file']

    if not file or not allowed_file(file.filename):
        session['error'] = "File format not accepted (use csv)"
        return redirect(url_for('convenor.error_page'))

    content = (file.read()).decode("UTF-8")
    lines = content.replace("\r", "")
    lines = lines.split("\n")

    try:
        team = TeamList(lines)
        team.add_team_functional()
        if len(team.errors) > 0:
            session['error'] = ",".join(team.errors)
            return redirect(url_for('convenor.error_page'))
        if len(team.warnings) > 0:
            flash(",".join(team.warnings))
        else:
            flash("Team added!")
            handle_table_change(Tables.TEAM)
    except Exception as e:
        session['error'] = str(e)
        return redirect(url_for('convenor.error_page'))
    return redirect(url_for('convenor.teams_page'))
