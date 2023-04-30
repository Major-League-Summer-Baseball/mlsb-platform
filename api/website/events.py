# -*- coding: utf-8 -*-
""" MLSB Summer Events. """
from flask import render_template, send_from_directory, Response
from api import app, PICTURES, DB
from api.model import LeagueEvent, LeagueEventDate
from api.routes import Routes
from api.cached_items import get_website_base_data as base_data
from api.authentication import get_user_information, api_require_login,\
    are_logged_in, get_player_id
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


@app.route(
    Routes['eventspage'] + "/signup/<int:league_event_date_id>",
    methods=["POST"]
)
@api_require_login
def signup_event(league_event_date_id):
    """Signup player for given event date."""
    league_event_date = LeagueEventDate.query.get(league_event_date_id)
    if league_event_date is None:
        return Response(
            json.dumps(False),
            status=404,
            mimetype="application/json"
        )
    player_id = get_player_id()
    success = league_event_date.signup_player(player_id)
    DB.session.commit()
    return Response(
        json.dumps(success),
        status=200,
        mimetype="application/json"
    )


@app.route(Routes['eventspage'] + "/<int:year>")
def events_page(year):
    """The events page for a given year"""
    events = get_year_events(year)
    if are_logged_in():
        for i in range(0, len(events)):
            event = LeagueEventDate.query.get(
                events[i]['league_event_date_id']
            )
            if event is None:
                events[i]['registered'] = False
            else:
                events[i]['registered'] = event.is_player_signed_up(
                    get_player_id()
                )
            
    return render_template("website/events.html",
                           dates=events,
                           route=Routes,
                           base=base_data(year),
                           title="Events",
                           year=year,
                           user_info=get_user_information())
