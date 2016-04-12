'''
@author: Dallas Fraser
@author: 2016-04-12
@organization: MLSB API
@summary: Contains all the routes for the API
'''
Routes = {}
# -----------------------------------------------------------------------------
# APIs
# -----------------------------------------------------------------------------
# basic routes
Routes['player'] = "/api/players"
Routes['sponsor'] = "/api/sponsors"
Routes['league'] = "/api/leagues"
Routes['photo'] = "/api/photos"
Routes['team'] = "/api/teams"
Routes['game'] = "/api/games"
Routes['bat'] = "/api/bats"
Routes['team_roster'] = "/api/tearmroster"
Routes['espy'] = "/api/espys"
# advanced routes
Routes['vplayer'] = "/api/view/players"
Routes['vteam'] = "/api/view/teams"
Routes['vgame'] = "/api/view/games"
Routes['vplayerLookup'] = "/api/view/player_lookup"
# Kik APIS
Routes['kiksubscribe'] = "/api/kik/subscribe"
Routes['kiksubmitscore'] = "/api/kik/submit_score"
Routes['kikcaptain'] = "/api/kik/captain"
Routes['kikupcominggames'] = "/api/kik/upcoming_games"
Routes['kiktransaction'] = "/api/kik/transaction"
Routes['kikcaptaingames'] = "/api/kik/captain/games"

# -----------------------------------------------------------------------------
# documentation routes
# -----------------------------------------------------------------------------
Routes['dindex'] = "/documentation"
Routes['dresponse'] = "/documentation/object/response"
# do = documentation object
Routes['doplayer'] = "/documentation/object/player"
Routes['dobat'] = "/documentation/object/bat"
Routes['dogame'] = "/documentation/object/game"
Routes['dosponsor'] = "/documentation/object/sponsor"
Routes['doteam'] = "/documentation/object/team"
Routes['doteamroster'] = "/documentation/object/teamroster"
Routes['doleague'] = "/documentation/object/league"
# db = documentation basic
Routes['dbplayer'] = "/documentation/basic/player"
Routes['dbbat'] = "/documentation/basic/bat"
Routes['dbgame'] = "/documentation/basic/game"
Routes['dbsponsor'] = "/documentation/basic/sponsor"
Routes['dbteam'] = "/documentation/basic/team"
Routes['dbteamroster'] = "/documentation/basic/teamroster"
Routes['dbleague'] = "/documentation/basic/league"
# dv = documentation view
Routes['dvgame'] = "/documentation/views/game"
Routes['dvplayer'] = "/documentation/views/player"
Routes['dvteam'] = "/documentation/views/team"
# kik documentation 
Routes['dkiksubscribe'] = "/documentation/kik/subscribe"
Routes['dkiksubmitscore'] = "/documentation/kik/submit_score"
Routes['dkikcaptain'] = "/documentation/kik/captain"
Routes['dkikupcominggames'] = "/documentation/kik/upcoming_games"
Routes['dkiktransaction'] = "/documentation/kik/transaction"
Routes['dkikcaptaingames'] = "/documentation/kik/captain/games"

# -----------------------------------------------------------------------------
# Website
# -----------------------------------------------------------------------------
# static pages
Routes['fieldsrulespage'] = "/website/rulesAndFields"
Routes['about'] = "/about"
# sponsors pages
Routes['sponsorspage'] = "/website/sponsor"
Routes['sponsorspicture'] = "/website/sponsor/picture"
Routes['sponsorspage'] = "/website/sponsors_list"
# baseball pages
Routes['homepage'] = "/website"
Routes['teampage'] = "/website/teams"
Routes['schedulepage'] = "/website/schedule"
Routes['standingspage'] = "/website/standings"
Routes['teamspage'] = "/website/teams"
Routes['statspage'] = "/website/stats"
Routes['playerpage'] = "/website/player"
Routes['leagueleaderpage'] = "/website/leaders"
# events
Routes['eventspage'] = "/website/event"

# -----------------------------------------------------------------------------
# Admin
# -----------------------------------------------------------------------------
# editting columns
Routes['aindex'] = "/admin"
Routes['aportal'] = "/admin/portal"
Routes['alogin'] = "/admin/login"
Routes['alogout'] = "/admin/logout"
Routes['editplayer'] = "/admin/edit/player"
Routes['editgame'] = "/admin/edit/game"
Routes['editleague'] = "/admin/edit/league"
Routes['editteam'] = "/admin/edit/team"
Routes['editsponsor'] = "/admin/edit/sponsor"
Routes['editbat'] = "/admin/edit/bat"
Routes['editroster'] = "/admin/edit/roster"
Routes['nonactiveplayers'] = "/admin/edit/non_active_players"
Routes['adeactivateplayer'] = "/admin/edit/player/deactivate"
Routes['adeactivatesponsor'] = "/admin/edit/sponsor/deactivate"
# imports from csv
Routes['importteam'] = "/admin/import/team"
Routes['importgame'] = "/admin/import/game"
Routes['importbat'] = "/admin/import/score"
# import routes
Routes["import_team_list"] = "/admin/import/team/list"
Routes["import_game_list"] = "/admin/import/game/list"
Routes["import_bat_list"] = "/admin/import/bat/list"
# templates
Routes['team_template'] = "/admin/template/team"
Routes['game_template'] = "/admin/template/game"
Routes['bat_template'] = "/admin/template/bat"
# -----------------------------------------------------------------------------
