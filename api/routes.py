# DEPRECATED - no longer needed - just use url_for
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
Routes['vplayerLookup'] = "/api/view/player_lookup"
Routes['vfun'] = "/api/view/fun"
Routes['vplayerteamLookup'] = "/api/view/players/team_lookup"
Routes['vleagueleaders'] = "/api/view/league_leaders"
Routes['vschedule'] = "/api/view/schedule"
Routes['vdivisions'] = "/api/view/divisions"
Routes['vleagueevents'] = "/api/view/league_events"
