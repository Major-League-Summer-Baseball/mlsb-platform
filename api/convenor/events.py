from flask import render_template, send_from_directory
from api.variables import NOTFOUND, PICTURES, POSTS
from api.cached_items import get_upcoming_games
from api.authentication import get_user_information
from api.convenor import convenor_blueprint
from api.model import Game
import os.path
import json


@convenor_blueprint.route("events")
def events_page():
    return render_template(
        "convenor/events.html"
    )