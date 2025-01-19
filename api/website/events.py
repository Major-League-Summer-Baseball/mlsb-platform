# -*- coding: utf-8 -*-
""" MLSB Summer Events. """
from flask import render_template, Response
from api.extensions import DB
from api.model import LeagueEventDate
from api.website import website_blueprint
from api.authentication import \
    get_user_information, api_require_login, are_logged_in, get_player_id
from api.queries.league_events import get_year_events
import json


@website_blueprint.route("/website/event/<int:year>/json")
def events_page_json(year):
    return json.dumps(get_year_events(year))


@website_blueprint.route(
    "/website/event/signup/<int:league_event_date_id>",
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


@website_blueprint.route("/website/event/<int:year>")
def events_page(year):
    """The events page for a given year"""
    events = get_year_events(year)
    if are_logged_in():
        for i in range(0, len(events)):
            event = None
            league_event_date_id = events[i]['league_event_date_id']
            if league_event_date_id is not None:
                event = LeagueEventDate.query.get(league_event_date_id)
            if event is None:
                events[i]['registered'] = False
            else:
                events[i]['registered'] = event.is_player_signed_up(
                    get_player_id()
                )
    return render_template(
        "website/events.html",
        dates=events,
        title="Events",
        year=year,
        user_info=get_user_information()
    )
