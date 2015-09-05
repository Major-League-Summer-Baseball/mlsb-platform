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
# view routes
Routes['vplayer'] = "/api/view/players"
Routes['vteam'] = "/api/view/teams"
Routes['vgame'] = "/api/view/games"

# website
Routes['about'] = "/about"

# documentation routes
Routes['dindex'] = "/documentation"
# do = documentation object
Routes['doplayer'] = "/documentation/object/player"
Routes['dobat'] = "/documentation/object/bat"
Routes['dogame'] = "/documentation/object/game"
Routes['dosponsor'] = "/documentation/object/sponsor"
Routes['doteam'] = "/documentation/object/team"
Routes['doteamroster'] = "/documentation/object/teamroster"
Routes['dotournament'] = "/documentation/object/tournament"
# db = documentation basic
Routes['dbplayer'] = "/documentation/basic/player"
Routes['dobat'] = "/documentation/basic/bat"
Routes['dbgame'] = "/documentation/basic/game"
Routes['dbsponsor'] = "/documentation/basic/sponsor"
Routes['dbteam'] = "/documentation/basic/team"
Routes['dbteamroster'] = "/documentation/basic/teamroster"
Routes['dbleague'] = "/documentation/basic/league"
# dv = documentation view
Routes['dvgame'] = "/documentation/views/game"
Routes['dvplayer'] = "/documentation/views/player"
Routes['dvteam'] = "/documentation/views/team"
