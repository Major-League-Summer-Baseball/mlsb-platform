'''
@author: Dallas Fraser
@author: 2015-08-25
@organization: MLSB API
@summary: Contains all the routes for the API
'''
Routes = {}
# basic routes
Routes['player'] = "/api/players"
Routes['sponsor'] = "/api/sponsors"
Routes['league'] = "/api/leagues"
Routes['photo'] = "/api/photos"
Routes['team'] = "/api/teams"
Routes['game'] = "/api/games"
Routes['bat'] = "/api/bats"
Routes['team_roster'] = "/api/tearmroster"
 
# advanced routes
Routes['vplayer'] = "/api/view/players"
Routes['vteam'] = "/api/view/teams"
Routes['vgame'] = "/api/view/games"

# website
Routes['about'] = "/about"

# documentation routes
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


# website routes
Routes['homepage'] = "/website"
Routes['teampage'] = "/website/team"
Routes['sponsorspage'] = "/website/sponsor"
Routes['sponsorspicture'] = "/website/sponsor/picture"
Routes['schedulepage'] = "/website/schedule"
Routes['standingspage'] = "/website/standings"
Routes['teamspage'] = "/website/teams"
Routes['mysterybuspage'] = "/website/event/mysterybus"
Routes['bluejayspage'] = "/website/event/bluejays"
Routes['beerfestpage'] = "/website/event/beerfest"
Routes['raftingpage'] = "/website/event/rafting"
Routes['beerwellpage'] = "/website/event/beerwell"
Routes['hftcpage'] = "/website/event/hftc"
Routes['summerweenpage'] = "/website/event/summerween"
Routes['espypage'] = "/website/event/espy"
Routes['sponsorspage'] = "/website/sponsors_list"
Routes['leaderspage'] = "/website/leaders"
Routes['wleaderspage'] = "/website/wleaders"
Routes['espystandingspage'] = "/website/espy"
Routes['rulespage'] = "/website/rules"
Routes['fieldspage'] = "/website/fields"


# admin routes
Routes['aindex'] = "/admin"
Routes['aportal'] = "/admin/portal"
Routes['alogin'] = "/admin/login"
Routes['alogout'] = "/admin/logout"
Routes['editplayer'] = "/admin/edit/player"
Routes['editgame'] = "/admin/edit/game"
Routes['editleague'] = "/admin/edit/league"
Routes['editteam'] = "/admin/edit/team"
Routes['editsponsor'] = "/admin/edit/sponsor"
Routes['importteam'] = "/admin/import/team"
Routes['importgame'] = "/admin/import/game"
Routes['importscore'] = "/admin/import/score"

