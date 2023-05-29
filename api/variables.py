'''
Name: Dallas Fraser
Date: 2016-04-12
Project: MLSB API
Purpose: Holds constant variables that used
'''
# cache timeouts for the main website (in seconds)
import os

SHORT_TERM_CACHE = os.environ.get('SHORT_TERM_CACHE', 60)
MEDIUM_TERM_CACHE = os.environ.get('MEDIUM_TERM_CACHE', 3600)
LONG_TERM_CACHE = os.environ.get('SHORT_TERM_CACHE', 3600)
CACHE_TIMEOUT = 600


NOTFOUND = "notFound.png"

# the UNASSIGNED player id used for bats that are not assigned to a player
UNASSIGNED = 1
UNASSIGNED_EMAIL = "unassignedBats@mlsb.ca"

# the hits that are available
HITS = ["s", "ss", "d", "hr", "t"]

# all the possible results from a bat
BATS = ['s', 'd', 'ss', 'hr', "t", 'k', 'e', 'fc', 'fo', 'go', 'sf']
# the genders currently supported
GENDERS = ["f", "m"]


# the fields we play at
FIELDS = ["WP1", "WP2", "WP3", "WP4", "Hillside Upper", "Hillside Lower"]

# the page size for the API paginated responses
PAGE_SIZE = 30
