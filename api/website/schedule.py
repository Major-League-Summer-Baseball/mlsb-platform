# -*- coding: utf-8 -*-
""" Pages and routes related to the league schedule. """
from flask import render_template, url_for, \
    redirect, request, Response
from api import app
from api.routes import Routes
from api.cached_items import get_league_map, get_league_schedule,\
    get_divisions_for_league_and_year

from api.cached_items import get_website_base_data as base_data
from api.authentication import get_user_information
import json


@app.route(Routes["schedulepage"] + "/<int:league_id>/<int:year>")
def schedule(league_id, year):
    league = get_league_map().get(league_id, None)
    if league is None:
        return redirect(url_for("league_not_found", year=year))
    divisions = get_divisions_for_league_and_year(year, league_id)
    if len(divisions) == 1:
        divisions = []
    return render_template("website/schedule.html",
                           route=Routes,
                           base=base_data(year),
                           title="Schedule",
                           league=league,
                           divisions=divisions,
                           year=year,
                           user_info=get_user_information())


@app.route(Routes['schedulecache'] + "/<int:year>/<int:league_id>")
def cache_schedule_page(year, league_id):
    page = int(request.args.get('page', 1))
    data = get_league_schedule(year, league_id, page)
    return Response(json.dumps(data), status=200, mimetype="application/json")
