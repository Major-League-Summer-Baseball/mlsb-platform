from os.path import join
from os import getcwd, environ


# variables for various statis files and templates
PICTURES = join(getcwd(), "api", "static", "pictures")
CSS_FOLDER = join(getcwd(), "api", "static", "css")
POSTS = join(getcwd(), "api", "templates", "website", "posts")
FILES = join(getcwd(), "api", "static", "files")
NOTFOUND = "notFound.png"

# cache timeouts for the main website (in seconds)
SHORT_TERM_CACHE = environ.get('SHORT_TERM_CACHE', 60)
MEDIUM_TERM_CACHE = environ.get('MEDIUM_TERM_CACHE', 3600)
LONG_TERM_CACHE = environ.get('LONG_TERM_CACHE', 3600)
CACHE_TIMEOUT = 600

# the UNASSIGNED player id used for bats that are not assigned to a player
UNASSIGNED = 1
UNASSIGNED_EMAIL = "unassignedBats@mlsb.ca"
UNASSIGNED_TEAM = 'unassigned-team'

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
PLAYER_PAGE_SIZE = 5
HALL_OF_FAME_SIZE = 10
