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
Routes['team_roster'] = "/api/teamroster"
Routes['espy'] = "/api/espys"
Routes['fun'] = "/api/fun"
Routes['division'] = "/api/division"
Routes['league_event'] = "/api/league_event"
Routes['league_event_date'] = "/api/league_event_date"

# advanced routes
Routes['vplayer'] = "/api/view/players"
Routes['vteam'] = "/api/view/teams"
Routes['vgame'] = "/api/view/games"
Routes['vplayerLookup'] = "/api/view/player_lookup"
Routes['vfun'] = "/api/view/fun"
Routes['vplayerteamLookup'] = "/api/view/players/team_lookup"
Routes['vleagueleaders'] = "/api/view/league_leaders"
Routes['vschedule'] = "/api/view/schedule"
Routes['vdivisions'] = "/api/view/divisions"
Routes['vleagueevents'] = "/api/view/league_events"


# Bot APIS
Routes['botsubmitscore'] = "/api/bot/submit_score"
Routes['botcaptain'] = "/api/bot/captain"
Routes['botupcominggames'] = "/api/bot/upcoming_games"
Routes['botcaptaingames'] = "/api/bot/captain/games"
Routes['bottransaction'] = "/api/bot/transaction"
