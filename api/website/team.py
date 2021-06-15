# -*- coding: utf-8 -*-
""" Pages and routes related a team. """
from flask import render_template, send_from_directory

from api import app, PICTURES
from api.model import Team, Player, JoinLeagueRequest, DB
from api.variables import NOTFOUND
from api.website.helpers import get_team
from api.routes import Routes
from api.advanced.players_stats import post as player_summary
from api.cached_items import get_team_map
from api.cached_items import get_website_base_data as base_data
from api.authentication import get_user_information, api_require_captain,\
    get_team_authorization, api_require_login
from flask_login import current_user
from flask import request, Response
import os.path
import json


@app.route(Routes['teampicture'] + "/<int:team>")
@app.route(Routes['teampicture'] + "/<team>")
def team_picture(team):
    name = team if team is not None and team != "None" else "notFound"
    if isinstance(team, int):
        team_id = int(team)
        team = get_team_map().get(team_id, None)
        if team is not None and team['sponsor_name'] is not None:
            name = team['sponsor_name']
        else:
            name = "notFound"
    name = name.lower().replace(" ", "_") + ".png"
    f = os.path.join(PICTURES, "sponsors", name)
    fp = os.path.join(PICTURES, "sponsors")
    if os.path.isfile(f):
        return send_from_directory(fp, name)
    else:
        return send_from_directory(fp, NOTFOUND)


@api_require_login
@app.route(Routes['teampage'] + "/<int:team_id>/join_team", methods=["POST"])
def request_to_join_team(team_id):
    # know the team will be found since decorator checks team exists
    team = Team.query.get(team_id)
    join = JoinLeagueRequest(
        current_user.email, current_user.name, team, current_user.gender)
    DB.session.add(join)
    DB.session.commit()
    return Response(
        json.dumps(join.json()), status=200, mimetype="application/json")


@api_require_captain
@app.route(Routes['teampage'] +
           "/<int:team_id>/request_response/<int:request_id>",
           methods=["POST"])
def captain_respond_league_request(team_id, request_id):
    league_request = JoinLeagueRequest.query.get(request_id)
    if league_request is None and not league_request.pending:
        return json.dumps(False)
    accept = request.get_json()['accept']
    if accept:
        league_request.accept_request()
    else:
        league_request.decline_request()
    return json.dumps(True)


@app.route(Routes['teampage'] + "/<int:year>/<int:team_id>")
def team_page(year, team_id):
    team = get_team(year, team_id)
    if team is None:
        return render_template("website/notFound.html",
                               route=Routes,
                               base=base_data(year),
                               team=team,
                               title="Team not found",
                               year=year,
                               user_info=get_user_information())
    team_authorization = get_team_authorization(Team.query.get(team_id))
    team_requests = []
    if team_authorization['is_captain']:
        team_requests = (JoinLeagueRequest.query
                         .filter(JoinLeagueRequest.team_id == team_id)
                         .filter(JoinLeagueRequest.pending == True)).all()
        team_requests = [request.json() for request in team_requests]
    return render_template("website/team.html",
                           route=Routes,
                           base=base_data(year),
                           team=team,
                           team_id=team_id,
                           title="Team - " + str(team['name']),
                           year=year,
                           user_info=get_user_information(),
                           team_requests=team_requests,
                           team_authorization=team_authorization)


@app.route(Routes['playerpage'] + "/<int:year>/<int:player_id>")
def player_page(year, player_id):
    player = Player.query.get(player_id)
    if player is None:
        return render_template("website/notFound.html",
                               route=Routes,
                               base=base_data(year),
                               title="Player not found",
                               year=year,
                               user_info=get_user_information())
    name = player.name
    years = []
    for team in player.teams:
        years.append((team.year, team.id))
    stats = []
    for entry in years:
        player = {}
        summary = player_summary(year=entry[0],
                                 team_id=entry[1],
                                 player_id=player_id)
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
    return render_template("website/player.html",
                           route=Routes,
                           base=base_data(year),
                           stats=stats,
                           title="Player Stats",
                           name=name,
                           year=year,
                           user_info=get_user_information())
