# -*- coding: utf-8 -*-
""" Pages and routes related a team. """
from datetime import date
from flask import redirect, render_template, url_for
from sqlalchemy import not_
from api.errors import PlayerNotOnTeam, RequestDoesNotExist, TeamDoesNotExist
from api.extensions import DB
from api.model import Team, Player, JoinLeagueRequest
from api.variables import UNASSIGNED_EMAIL, PLAYER_PAGE_SIZE
from api.website.helpers import get_team
from api.queries.player import player_summary
from api.authentication import \
    get_user_information, get_team_authorization, require_captain, require_login
from api.website import website_blueprint
from flask_login import current_user
from flask import request


@website_blueprint.route("/website/teams/<int:year>/<int:team_id>")
def team_page(year, team_id):
    team = get_team(year, team_id)
    if team is None:
        return render_template(
            "website/notFound.html",
            team=team,
            title="Team not found",
            year=year,
            user_info=get_user_information()
        )
    team_authorization = get_team_authorization(Team.query.get(team_id))
    team_requests = []
    all_players = []
    if team_authorization['is_captain']:
        team_requests = (
            JoinLeagueRequest.query
            .filter(JoinLeagueRequest.team_id == team_id)
            .filter(JoinLeagueRequest.pending == True)
        ).all()
        team_requests = [request.json() for request in team_requests]
        all_players = [
            player.admin_json()
            for player in Player.query.filter(
                not_(Player.email.ilike(UNASSIGNED_EMAIL))
            ).all()
        ]
    return render_template(
        "website/team.html",
        team=team,
        team_id=team_id,
        title="Team - " + str(team['name']),
        year=year,
        user_info=get_user_information(),
        team_requests=team_requests,
        all_players=all_players,
        team_authorization=team_authorization
    )


@website_blueprint.route("/website/player/<int:year>/<int:player_id>")
def player_page(year, player_id):
    player = Player.query.get(player_id)
    if player is None:
        return render_template(
            "website/notFound.html",
            title="Player not found",
            year=year,
            user_info=get_user_information()
        )
    name = player.name
    years = []
    for team in player.teams:
        years.append((team.year, team.id))
    stats = []
    for entry in years:
        player = {}
        summary = player_summary(
            year=entry[0],
            team_id=entry[1],
            player_id=player_id
        )
        if name in summary:
            player = summary[name]
        else:
            player = {
                's': 0,
                'd': 0,
                'hr': 0,
                'ss': 0,
                'k': 0,
                'fo': 0,
                'fc': 0,
                'e': 0,
                'go': 0,
                'id': player_id,
                'rbi': 0,
                'avg': 0.000,
                'bats': 0
            }
        player['team'] = str(Team.query.get(entry[1]))
        player['team_id'] = entry[1]
        player['year'] = entry[0]
        stats.append(player)
    return render_template(
        "website/player.html",
        stats=stats,
        title="Player Stats",
        name=name,
        year=year,
        user_info=get_user_information()
    )


@website_blueprint.route(
    "/website/<int:year>/team/<int:team_id>/add-new-player", methods=["POST"]
)
@require_captain
def add_new_player(year: int, team_id: int):
    """Form Request to add a new player"""
    gender = "F" if request.form.get("is_female", False) else "M"
    player_name = request.form.get("name", None)
    email = request.form.get("email")
    # create a new player
    player = Player(player_name, email, gender)
    DB.session.add(player)
    DB.session.commit()

    # add the player to the team
    team = Team.query.get(team_id)
    if team is None:
        raise TeamDoesNotExist(payload={
            'details': team_id
        })

    team.insert_player(player.id)
    DB.session.commit()
    return redirect(url_for("website.team_page", team_id=team_id, year=year))


@website_blueprint.route(
    "/website/<int:team_id>/search_players", methods=["POST"]
)
@require_captain
def search_players(team_id):
    # ensure only search by logged in captain
    if request.is_json:
        search_phrase = request.get_json()['player']
    else:
        search_phrase = request.form['player']
    players = Player.search_player(search_phrase)
    player_data = []
    for player in players:
        # include email since only should be searchable by captains
        json = player.admin_json()
        json['first_year'] = min(
            [team.year for team in player.teams] + [date.today().year]
        )
        player_data.append(json)

    return render_template(
        "website/components/player_list.html",
        players=player_data,
        show_add=len(players) <= PLAYER_PAGE_SIZE
    )


@website_blueprint.route(
    "/website/<int:year>/teams/<int:team_id>/join_team", methods=["POST"]
)
@require_login
def request_to_join_team(year, team_id):
    """Request to join a given team as a logged in user"""
    team = Team.query.get(team_id)
    if team is None:
        raise TeamDoesNotExist(payload={'details': team_id})
    join = JoinLeagueRequest(
        current_user.email, current_user.name, team, current_user.gender)
    DB.session.add(join)
    DB.session.commit()
    return redirect(url_for("website.league_request_sent"))


@website_blueprint.route("/website/team/<int:team_id>/join", methods=["POST"])
def join_team_request(team_id: int):
    """Form Request to join a given team for not logged in user"""
    gender = "F" if request.form.get("is_female", False) else "M"
    player_name = request.form.get("name", None)
    email = request.form.get("email")
    # create a request
    DB.session.add(
        JoinLeagueRequest.create_request(player_name, email, gender, team_id)
    )
    DB.session.commit()
    return redirect(url_for("website.league_request_sent"))


@website_blueprint.route(
    "/website/<int:year>/teams/<int:team_id>/drop_player/<int:player_id>",
    methods=["POST"]
)
@require_captain
def team_remove_player(year, team_id, player_id):
    # know teams exist since user is captain
    team = Team.query.get(team_id)
    team.remove_player(player_id)
    DB.session.commit()
    return redirect(url_for("website.team_page", team_id=team_id, year=year))


@website_blueprint.route(
    "/website/<int:year>/teams/<int:team_id>/add_player",
    methods=["POST"]
)
@require_captain
def team_add_player_form(year, team_id):
    # know teams exist since user is captain
    player_id = request.form.get("player_id", -1)
    team = Team.query.get(team_id)
    success = team.insert_player(player_id)
    if not success:
        raise PlayerNotOnTeam(payload={
            'details': player_id
        })

    DB.session.commit()
    return redirect(url_for("website.team_page", team_id=team_id, year=year))


@website_blueprint.route(
    "/website/<int:year>/teams/<int:team_id>/request_response",
    methods=["POST"]
)
@require_captain
def captain_respond_league_request_form(year, team_id):
    request_id = request.form.get("request_id", -1)
    accept = True if request.form.get(
        "accept", False) in ["true", "True", 1, True] else False
    league_request = JoinLeagueRequest.query.get(request_id)
    if league_request is None or not league_request.pending:
        raise RequestDoesNotExist(payload={
            'details': request_id
        })

    if accept:
        league_request.accept_request()
    else:
        league_request.decline_request()
    DB.session.commit()
    return redirect(url_for("website.team_page", team_id=team_id, year=year))
