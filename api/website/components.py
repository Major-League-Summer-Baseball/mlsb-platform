# -*- coding: utf-8 -*-
"""
    Any routes related to small web components
"""
from flask import render_template
from api.cached_items import get_upcoming_games, get_fun_meter, \
    get_sponsor_banner, get_fun_counts
from api.website import website_blueprint


@website_blueprint.route("/website/component/fun-meter/<int:year>")
def component_fun_meter(year):
    return render_template(
        "website/components/fun_meter.html",
        fun=get_fun_meter(year),
        funs=get_fun_counts(),
        year=year
    )


@website_blueprint.route("/website/component/score-banner/<int:year>")
def component_score_banner(year):
    return render_template(
        "website/components/score_banner.html",
        games=get_upcoming_games(year)
    )


@website_blueprint.route("/website/component/sponsor-banner/<int:year>")
def component_sponsor_banner(year):
    return render_template(
        "website/components/sponsor_banner.html",
        sponsors=get_sponsor_banner(year)
    )
