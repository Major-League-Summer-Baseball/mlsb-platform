# -*- coding: utf-8 -*-
""" MLSB Summer Events. """
from flask import render_template, send_from_directory
from api import app, PICTURES
from api.model import LeagueEvent
from api.routes import Routes
from api.cached_items import get_website_base_data as base_data
from api.authentication import get_user_information
from api.advanced.league_event import get_year_events
import os.path
import json
NOT_FOUND = "sorry.jpg"
EVENT_FOLDER = 'events'


@app.route(Routes['eventspage'] + "/<int:year>/image/<int:league_event_id>")
def mlsb_event_image(year, league_event_id):
    # two potential file paths
    filepath = os.path.join(PICTURES, EVENT_FOLDER)
    year_filepath = os.path.join(filepath, str(year))

    # does the event even exist
    event = LeagueEvent.query.get(league_event_id)
    if event is None:
        return send_from_directory(filepath, NOT_FOUND)

    filename = event.name.lower().replace(" ", "_").strip() + ".png"

    # see if this has a particular image
    if os.path.isfile(os.path.join(year_filepath, filename)):
        return send_from_directory(year_filepath, filename)

    # send the general event image
    if os.path.isfile(os.path.join(filepath, filename)):
        return send_from_directory(filepath, filename)

    # no image can be found for the given event
    return send_from_directory(filepath, NOT_FOUND)


@app.route(Routes['eventspage'] + "/<int:year>" + "/json")
def events_page_json(year):
    return json.dumps(get_year_events())


@app.route(Routes['eventspage'] + "/<int:year>")
def events_page(year):
    events = get_year_events(year)
    return render_template("website/events.html",
                           dates=events,
                           route=Routes,
                           base=base_data(year),
                           title="Events",
                           year=year,
                           user_info=get_user_information())
