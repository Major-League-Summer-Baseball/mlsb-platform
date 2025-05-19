# -*- coding: utf-8 -*-
""" Pages and routes related to the league's standings. """
from flask import render_template, url_for, redirect
from api.queries.player import player_summary
from api.queries.team_records import \
    rank_teams_by_espys, rank_teams_by_record, \
    rank_teams_by_runs_for, rank_teams_by_stats
from api.cached_items import \
    get_league_map, get_league_leaders, \
    get_espys_breakdown, get_divisions_for_league_and_year
from api.website import website_blueprint
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
        team_route=url_for('rest.team_stats'),
        league=league,
        divisions=divisions,
        title="Standings",
        year=year,
        user_info=get_user_information()
    )


@website_blueprint.route("/website/stats/<int:year>")
def stats_page(year):
    players = player_summary(year=year)
    return render_template(
        "website/stats.html",
        title="Players Stats",
        year=year,
        players=players,
        user_info=get_user_information()
    )


@website_blueprint.route("/website/leaders/<int:year>")
def leaders_page(year):
    women = get_league_leaders("ss", year=year)[:10]
    men = get_league_leaders("hr", year=year)[:10]
    return render_template(
        "website/new-leaders.html",
        men=men,
        women=women,
        title="League Leaders",
        year=year,
        user_info=get_user_information()
    )


@website_blueprint.route("/website/hall-of-fame/<int:year>")
def all_time_leaders_page(year):
    # player stats
    hrSingleGame = get_league_leaders('hr', single_game=True)
    ssSingleGame = get_league_leaders('ss', single_game=True)
    hrSingleSeason = get_league_leaders("hr")
    ssSingleSeason = get_league_leaders("ss")
    hrAllSeason = get_league_leaders("hr", group_by_team=True)
    ssAllSeason = get_league_leaders("ss", group_by_team=True)

    # team rankings
    hrTeamAllTime = rank_teams_by_stats('hr')
    espysTeamAllTime = rank_teams_by_espys()
    runsForTeamAllTime = rank_teams_by_runs_for()
    winsForTeamAllTime = rank_teams_by_record()
    return render_template(
        "website/all-time-leaders.html",
        hrSingleGame=hrSingleGame,
        ssSingleGame=ssSingleGame,
        hrSingleSeason=hrSingleSeason,
        ssSingleSeason=ssSingleSeason,
        hrAllSeason=hrAllSeason,
        ssAllSeason=ssAllSeason,
        hrTeamAllTime=hrTeamAllTime,
        espysTeamAllTime=espysTeamAllTime,
        runsForTeamAllTime=runsForTeamAllTime,
        winsForTeamAllTime=winsForTeamAllTime,
        title="Hall of Fame",
        year=year,
        user_info=get_user_information()
    )


@website_blueprint.route("/website/hall-of-fame/top/<stat>/<int:year>")
def top_hundred_players_all_time(stat, year):
    if stat == 'hr':
        players = get_league_leaders("hr", group_by_team=True, limit=100)
    else:
        players = get_league_leaders("ss", group_by_team=True, limit=100)
    return render_template(
        "website/top-hundred-players.html",
        stat_title='Homeruns' if stat == 'hr' else 'Sapporo Singles',
        players=players,
        title="Hall of Fame",
        year=year,
        user_info=get_user_information()
    )


@website_blueprint.route("/website/espysbreakdown/<int:year>")
def espys_breakdown_request(year):
    return get_espys_breakdown(year)
