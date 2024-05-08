# -*- coding: utf-8 -*-
""" Pages and routes related to the league schedule. """
from flask import \
    render_template, url_for, redirect, request, Response
from api.cached_items import \
    get_full_league_schedule, get_league_map, get_league_schedule, get_divisions_for_league_and_year
from api.website import website_blueprint
from api.authentication import get_user_information
from datetime import datetime
import json


@website_blueprint.route("/website/schedule/<int:league_id>/<int:year>")
def schedule(league_id, year):
    league = get_league_map().get(league_id, None)
    if league is None:
        return redirect(url_for("website.league_not_found", year=year))
    divisions = get_divisions_for_league_and_year(year, league_id)
    if len(divisions) == 1:
        divisions = []
    schedule = get_full_league_schedule(year, league_id)
    return render_template(
        "website/schedule.html",
        today=datetime.now().strftime("%Y-%m-%d"),
        title="Schedule",
        league=league,
        divisions=divisions,
        schedule=schedule,
        year=year,
        user_info=get_user_information()
    )


@website_blueprint.route(
    "/website/cache/view/schedule/<int:year>/<int:league_id>"
)
def cache_schedule_page(year, league_id):
    page = int(request.args.get('page', 1))
    data = get_league_schedule(year, league_id, page)
    return Response(json.dumps(data), status=200, mimetype="application/json")
