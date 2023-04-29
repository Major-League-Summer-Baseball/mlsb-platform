'''
Name: Dallas Fraser
Date: 2016-04-12
Project: MLSB API
Purpose: Holds the routes for the documentation
'''
from flask import render_template
from api.routes import Routes
from api import app
from api.errors import ERRORS


@app.route(Routes["dindex"])
def index_doc():
    return render_template('documentation/documentation.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes["dresponse"])
def response_object_doc():
    return render_template('documentation/responseObject.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes["doplayer"])
def player_object_doc():
    return render_template('documentation/playerObject.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes["doteam"])
def team_object_doc():
    return render_template('documentation/teamObject.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes["dobat"])
def bat_object_doc():
    return render_template('documentation/batObject.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes["dogame"])
def game_object_doc():
    return render_template('documentation/gameObject.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes["doleague"])
def league_object_doc():
    return render_template('documentation/leagueObject.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes["doleagueevent"])
def league_event_object_doc():
    return render_template('documentation/leagueEventObject.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes["doleagueeventdate"])
def league_event_date_object_doc():
    return render_template('documentation/leagueEventDateObject.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes["dodivision"])
def division_object_doc():
    return render_template('documentation/divisionObject.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes["dosponsor"])
def sponsor_object_doc():
    return render_template('documentation/sponsorObject.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes['dofun'])
def fun_object_doc():
    return render_template('documentation/funObject.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes['dopagination'])
def pagination_object_doc():
    return render_template('documentation/paginationObject.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes["doteamroster"])
def teamroster_object_doc():
    return render_template('documentation/teamRosterObject.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes["dbteamroster"])
def teamroster_route_doc():
    return render_template('documentation/teamRosterRoute.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes['dbfun'])
def fun_route_doc():
    return render_template('documentation/funRoute.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes["dbteam"])
def team_route_doc():
    return render_template('documentation/teamRoute.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes["dbplayer"])
def player_route_doc():
    return render_template('documentation/playerRoute.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes["dbbat"])
def bat_route_doc():
    return render_template('documentation/batRoute.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes["dbgame"])
def game_route_doc():
    return render_template('documentation/gameRoute.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes["dbsponsor"])
def sponsor_route_doc():
    return render_template('documentation/sponsorRoute.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes["dbleague"])
def league_route_doc():
    return render_template('documentation/leagueRoute.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes["dbleagueevent"])
def league_event_route_doc():
    return render_template('documentation/leagueEventRoute.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes["dbleagueeventdate"])
def league_event__dateroute_doc():
    return render_template('documentation/leagueEventDateRoute.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes["dbdivision"])
def division_route_doc():
    return render_template('documentation/divisionRoute.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes["dvteam"])
def team_view_doc():
    return render_template('documentation/teamView.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes["dvgame"])
def game_view_doc():
    return render_template('documentation/gameView.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes["dvleagueevent"])
def league_event_view_doc():
    return render_template('documentation/leagueEventView.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes["dvplayer"])
def player_view_doc():
    return render_template('documentation/playerView.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes['dvfun'])
def fun_meter_view_doc():
    return render_template('documentation/funView.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes['dvplayerLookup'])
def player_lookup_view_doc():
    return render_template('documentation/playerLookupView.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes['dvplayerteamLookup'])
def player_team_lookup_view_doc():
    return render_template('documentation/playerTeamLookupView.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes['dvleagueleaders'])
def league_leaders_view_doc():
    return render_template('documentation/leagueLeadersView.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes['dvschedule'])
def schedule_view_doc():
    return render_template('documentation/scheduleView.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes['dvdivisions'])
def divisions_view_doc():
    return render_template('documentation/divisionsView.html',
                           route=Routes,
                           errors=ERRORS)

# -----------------------------------------------------------------------------
# Bot documentation
# -----------------------------------------------------------------------------


@app.route(Routes['dbotcaptain'])
def authenticate_bot_doc():
    return render_template('documentation/botAuthenticateCaptain.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes['dbotsubmitscore'])
def submit_score_bot_doc():
    return render_template('documentation/botSubmitScore.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes['dbotupcominggames'])
def upcoming_games_bot_doc():
    return render_template('documentation/botUpcomingGames.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes['dbotcaptaingames'])
def captain_games_bot_doc():
    return render_template('documentation/botCaptainGames.html',
                           route=Routes,
                           errors=ERRORS)


@app.route(Routes['dbottransaction'])
def submit_transaction_bot_doc():
    return render_template('documentation/botSubmitTransaction.html',
                           route=Routes,
                           errors=ERRORS)
