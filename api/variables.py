'''
Name: Dallas Fraser
Date: 2016-04-12
Project: MLSB API
Purpose: Holds constant variables that used
'''
# cache timeout for the main website (how ofter things are cached for)
CACHE_TIMEOUT = 600

NOTFOUND = "notFound.png"

# the UNASSIGNED player id used for bats that are not assigned to a player
UNASSIGNED = 1
UNASSIGNED_EMAIL = "unassignedBats@mlsb.ca"

# the hits that are available
HITS = ["s", "ss", "d", "hr"]

# all the possible results from a bat
BATS = ['s', 'd', 'ss', 'hr', 'k', 'e', 'fc', 'fo', 'go']
# the genders currently supported
GENDERS = ["f", "m"]

# all the events baby
EVENTS = {
    2016: {
        "Beerfest": "May 13th",
        "ESPYS_Awards": "July 27th",
        "Jays_Game": "May 17th",
        "Summerween": "June 11th",
        "Mystery_Bus": "March 19th",
        "Rafting": "July 9th",
        "Hitting_for_the_Cycle": "July 16th",
        "Beerwell_Classic": "July 23rd",
        "Tournaments": "May 21st, May27th, July 15th, July 22nd"},
    2017: {
        "Beerfest": "May 17th",
        "ESPYS_Awards": "July 28th",
        "Jays_Game": "May 9th",
        "Summerween": "June 3rd",
        "Mystery_Bus": "March 24th",
        "Rafting": "July 7-9th",
        "Hitting_for_the_Cycle": "July 16th",
        "Beerwell_Classic": "?",
        "Tournaments": "May 19th, June 9th, July 14th, July 21st"
    },
    2018: {
        "Beerlympics": "June 9th",
        "Jays_Game": "May 22nd",
        "Summerween": "June 23rd",
        "Mystery_Bus": "March 24th",
        "Rafting": "July 6-8th",
        "Grand Bender": "July 28th",
        "Tournaments": "June 1st, June 8th, June 29th, July 20th",
        "Chainsaw Idol": "July 13th"
    },
    2019: {
        "Beerlympics": "TBD",
        "Jays_Game": "TBD",
        "Summerween": "TBD",
        "Mystery_Bus": "TBD",
        "Rafting": "TBD",
        "Grand Bender": "TBD",
        "Tournaments": "TBD, TBD, TBD, TBD",
        "Chainsaw Idol": "TBD"
    }
}

# the fields we play at
FIELDS = ["WP1", "WP2", "WP3", "WP4", "Hillside Upper", "Hillside Lower"]

# the kik points assigned for subscription
KIKPOINTS = 2
PAGE_SIZE = 30
