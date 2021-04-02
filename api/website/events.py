# -*- coding: utf-8 -*-
""" MLSB Summer Events. """
from flask import render_template
from api import app
from api.variables import EVENTS
from api.routes import Routes
from api.cached_items import get_website_base_data as base_data
import json


@app.route(Routes['eventspage'] + "/<int:year>" + "/json")
def events_page_json(year):
    if year in EVENTS:
        return json.dumps(EVENTS[year])
    else:
        return json.dumps({year: {}})


@app.route(Routes['eventspage'] + "/<int:year>")
def events_page(year):
    if year in EVENTS:
        return render_template("website/events.html",
                               dates=EVENTS[year],
                               route=Routes,
                               base=base_data(year),
                               title="Events",
                               year=year)
    else:
        return render_template("website/notFound.html",
                               year=year,
                               route=Routes,
                               base=base_data(year),
                               title="Not Found")
