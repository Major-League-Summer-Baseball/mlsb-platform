from flask import render_template, send_from_directory
from api.variables import NOTFOUND, PICTURES, POSTS
from api.cached_items import get_upcoming_games
from api.authentication import get_user_information
from api.convenor import convenor_blueprint
from api.model import Team
import os.path
import json


@convenor_blueprint.route("teams")
def teams_page():
    return render_template(
        "convenor/teams.html"
    )

@convenor_blueprint.route("team/<int:team_id>")
def edit_team_page(team_id: int):
    team = Team.query.get(team_id)
    return render_template(
        "convenor/team.html",
        team=team.json()
    )