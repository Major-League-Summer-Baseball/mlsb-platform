# -*- coding: utf-8 -*-
"""
    Any routes related to media and other assets.
"""
from flask import render_template
from api.routes import Routes
from api.cached_items import get_upcoming_games, get_fun_meter,\
    get_sponsor_banner
from api.website import website_blueprint


@website_blueprint.route("/website/component/fun-meter/<int:year>")
def component_fun_meter(year):
    return render_template(
        "website/components/fun_meter.html",
        route=Routes,
        fun=get_fun_meter(year),
        year=year
    )


@website_blueprint.route("/website/component/score-banner/<int:year>")
def component_score_banner(year):
    return render_template(
        "website/components/score_banner.html",
        route=Routes,
        games=get_upcoming_games(year)
    )


@website_blueprint.route("/website/component/sponsor-banner/<int:year>")
def component_sponsor_banner(year):
    return render_template(
        "website/components/sponsor_banner.html",
        route=Routes,
        sponsors=get_sponsor_banner(year)
    )
