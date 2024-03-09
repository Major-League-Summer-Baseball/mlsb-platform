# -*- coding: utf-8 -*-
""" Pages and routes related to the league's standings. """
from flask import render_template, url_for, redirect
from api.routes import Routes
from api.advanced.players_stats import post as player_summary
from api.cached_items import \
    get_league_map, get_league_leaders, \
    get_espys_breakdown, get_divisions_for_league_and_year
from api.website import website_blueprint
from api.cached_items import get_website_base_data as base_data
from api.authentication import get_user_information


@website_blueprint.route("/website/standings/<int:league_id>/<int:year>")
def standings(league_id, year):
    league = get_league_map().get(league_id, None)
    if league is None:
        return redirect(url_for("website.league_not_found", year=year))
    divisions = get_divisions_for_league_and_year(year, league_id)
    if len(divisions) == 1:
        divisions = []
    return render_template(
        "website/standings.html",
        route=Routes,
        team_route=url_for('vteam'),
        base=base_data(year),
        league=league,
        divisions=divisions,
        title="Standings",
        year=year,
        user_info=get_user_information()
    )


@website_blueprint.route("/website/stats/<int:year>")
def stats_page(year):
    players = player_summary(year=year)
    return render_template("website/stats.html",
                           route=Routes,
                           base=base_data(year),
                           title="Players Stats",
                           year=year,
                           players=players,
                           user_info=get_user_information())


@website_blueprint.route("/website/leaders/<int:year>")
def leaders_page(year):
    women = get_league_leaders("ss", year=year)[:5]
    men = get_league_leaders("hr", year=year)[:5]
    return render_template("website/new-leaders.html",
                           route=Routes,
                           base=base_data(year),
                           men=men,
                           women=women,
                           title="League Leaders",
                           year=year,
                           user_info=get_user_information())


@website_blueprint.route("/website/leaders/alltime/<int:year>")
def all_time_leaders_page(year):
    hrSingleSeason = get_league_leaders("hr")
    ssSingleSeason = get_league_leaders("ss")
    hrAllSeason = get_league_leaders("hr", group_by_team=True)
    ssAllSeason = get_league_leaders("ss", group_by_team=True)
    return render_template("website/all-time-leaders.html",
                           route=Routes,
                           base=base_data(year),
                           hrSingleSeason=hrSingleSeason,
                           ssSingleSeason=ssSingleSeason,
                           hrAllSeason=hrAllSeason,
                           ssAllSeason=ssAllSeason,
                           title="League Leaders",
                           year=year,
                           user_info=get_user_information())


@website_blueprint.route("/website/espysbreakdown/<int:year>")
def espys_breakdown_request(year):
    return get_espys_breakdown(year)
