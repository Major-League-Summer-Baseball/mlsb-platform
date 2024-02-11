from flask import render_template, Blueprint
from api.routes import Routes
from api.errors import ERRORS

documentation_blueprint = Blueprint(
    "documentation", __name__, url_prefix="/documentation")


@documentation_blueprint.route("")
def index_doc():
    return render_template('documentation/documentation.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/object/response")
def response_object_doc():
    return render_template('documentation/responseObject.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/object/player")
def player_object_doc():
    return render_template('documentation/playerObject.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/object/team")
def team_object_doc():
    return render_template('documentation/teamObject.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/object/bat")
def bat_object_doc():
    return render_template('documentation/batObject.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/object/game")
def game_object_doc():
    return render_template('documentation/gameObject.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/object/league")
def league_object_doc():
    return render_template('documentation/leagueObject.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/object/league_event")
def league_event_object_doc():
    return render_template('documentation/leagueEventObject.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/object/league_event_date")
def league_event_date_object_doc():
    return render_template('documentation/leagueEventDateObject.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/object/division")
def division_object_doc():
    return render_template('documentation/divisionObject.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/object/sponsor")
def sponsor_object_doc():
    return render_template('documentation/sponsorObject.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/object/fun")
def fun_object_doc():
    return render_template('documentation/funObject.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/object/pagination")
def pagination_object_doc():
    return render_template('documentation/paginationObject.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/object/teamroster")
def teamroster_object_doc():
    return render_template('documentation/teamRosterObject.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/basic/league")
def teamroster_route_doc():
    return render_template('documentation/teamRosterRoute.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/basic/fun")
def fun_route_doc():
    return render_template('documentation/funRoute.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/basic/team")
def team_route_doc():
    return render_template('documentation/teamRoute.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/basic/player")
def player_route_doc():
    return render_template('documentation/playerRoute.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/basic/bat")
def bat_route_doc():
    return render_template('documentation/batRoute.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/basic/game")
def game_route_doc():
    return render_template('documentation/gameRoute.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/basic/sponsor")
def sponsor_route_doc():
    return render_template('documentation/sponsorRoute.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/basic/league")
def league_route_doc():
    return render_template('documentation/leagueRoute.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/basic/league_event")
def league_event_route_doc():
    return render_template('documentation/leagueEventRoute.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/basic/league_event_date")
def league_event_dateroute_doc():
    return render_template('documentation/leagueEventDateRoute.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/basic/division")
def division_route_doc():
    return render_template('documentation/divisionRoute.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/views/team")
def team_view_doc():
    return render_template('documentation/teamView.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/views/game")
def game_view_doc():
    return render_template('documentation/gameView.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/views/league_event")
def league_event_view_doc():
    return render_template('documentation/leagueEventView.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/views/player")
def player_view_doc():
    return render_template('documentation/playerView.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/views/fun")
def fun_meter_view_doc():
    return render_template('documentation/funView.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/view/player_lookup")
def player_lookup_view_doc():
    return render_template('documentation/playerLookupView.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/views/player/team_lookup")
def player_team_lookup_view_doc():
    return render_template('documentation/playerTeamLookupView.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/views/league_leader")
def league_leaders_view_doc():
    return render_template('documentation/leagueLeadersView.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/views/schedule")
def schedule_view_doc():
    return render_template('documentation/scheduleView.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/views/divisions")
def divisions_view_doc():
    return render_template('documentation/divisionsView.html',
                           route=Routes,
                           errors=ERRORS)

# -----------------------------------------------------------------------------
# Bot documentation
# -----------------------------------------------------------------------------


@documentation_blueprint.route("/bot/captain")
def authenticate_bot_doc():
    return render_template('documentation/botAuthenticateCaptain.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/bot/submit_score")
def submit_score_bot_doc():
    return render_template('documentation/botSubmitScore.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/bot/upcoming_games")
def upcoming_games_bot_doc():
    return render_template('documentation/botUpcomingGames.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/bot/captain/games")
def captain_games_bot_doc():
    return render_template('documentation/botCaptainGames.html',
                           route=Routes,
                           errors=ERRORS)


@documentation_blueprint.route("/bot/transaction")
def submit_transaction_bot_doc():
    return render_template('documentation/botSubmitTransaction.html',
                           route=Routes,
                           errors=ERRORS)
