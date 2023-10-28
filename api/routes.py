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

# -----------------------------------------------------------------------------
# Website
# -----------------------------------------------------------------------------
# static pages
Routes['fieldsrulespage'] = "/website/rulesAndFields"
Routes['about'] = "/about"
Routes["privacy"] = "/privacy-policy"
Routes["termsandconditions"] = "/terms-and-conditions"

# stuff that changes each year
Routes['logo'] = "/logo"
Routes['favicon'] = "/favicon"
Routes['accents'] = "/accents"

# sponsors pages
Routes['sponsorspicture'] = "/website/sponsor/picture"
Routes['sponsorspage'] = "/website/sponsors_list"
Routes['teampicture'] = "/website/team/picture"

# baseball pages
Routes['homepage'] = "/website"
Routes['teampage'] = "/website/teams"
Routes['schedulepage'] = "/website/schedule"
Routes['standingspage'] = "/website/standings"
Routes['teamspage'] = "/website/teams"
Routes['statspage'] = "/website/stats"
Routes['playerpage'] = "/website/player"
Routes['leagueleaderpage'] = "/website/leaders"
Routes['alltimeleaderspage'] = Routes['leagueleaderpage'] + "/alltime"
Routes['leaguenotfoundpage'] = "/website/leagueNotFound"
Routes['promos'] = "/website/promos"

# events
Routes['eventspage'] = "/website/event"

# posts pages
Routes['posts'] = "/website/posts"
Routes['postpicture'] = "/website/post/pictures"


# Captain help
Routes['espysbreakdown'] = "/website/espysbreakdown"
Routes['sponsorbreakdown'] = "/website/sponsorbreakdown"
Routes['schedulecache'] = "/website/cache/view/schedule"
