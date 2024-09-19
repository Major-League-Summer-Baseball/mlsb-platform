from sqlalchemy import func
from api.cached_items import handle_table_change
from api.model import Sponsor, Game, League, Division
from api.extensions import DB
from api.errors import InvalidField, LeagueDoesNotExist, TeamDoesNotExist, \
    DivisionDoesNotExist
from api.tables import Tables
import logging
import datetime

# constants
MISSING_BACKGROUND = "Missing background: {}"
LEFT_BACKGROUND_EXAMPLE = "Background example was left: {}"
INVALID_TEAM = "{} is not a team in the league"
INVALID_ROW = "Unsure what to do with the following row: {}"
INVALID_LEAGUE = "League given was not found: {}"
INVALID_DIVISION = "Division given was not found: {}"
INVALID_GAME = "The game was invalid - {} with error {}"
TEAM_NOT_FOUND = "Did not find team {} - for row {}"
BACKGROUND = {"league": "League", "division": "Division"}
HEADERS = {"home": "Home Team",
           "away": "Away Team",
           "date": "Date",
           "time": "Time",
           "field": "Field"}


class LeagueList():

    def __init__(self,
                 lines,
                 year=datetime.datetime.now().year,
                 logger=None,
                 session=None):
        """A constructor

            lines: a list of lines from the csv
            year: the year the league was
            logger: a logger
            session: mock a database session
        """
        self.success = False
        self.errors = []
        self.warnings = []
        self.lines = lines
        if logger is None:
            logging.basicConfig(level=logging.INFO,
                                format='%(asctime)s %(message)s')
            logger = logging.getLogger(__name__)
        self.logger = logger
        self.year = year
        self.session = session
        if session is None:
            self.session = DB.session

    def import_league_functional(self):
        """ Add a team to the database using functions instead of methods"""

        # parse out the parts - background, header, players
        parts = parse_parts(self.lines)
        self.warnings = parts['warnings']

        # extract the background such a league, sponsor and color
        background = extract_background(parts['background'])
        league = background["league"]
        division = background["division"]

        # extract the players using the header as lookup
        lookup = extract_column_indices_lookup(parts['header'])

        # get the team map
        team_lookup = get_team_lookup(league)

        # extract the games
        games = extract_games(parts["games"], team_lookup, lookup)
        self.warnings = self.warnings + games['warnings']

        # add the players
        for game_json in games['games']:
            try:
                game = Game(game_json["date"],
                            game_json["time"],
                            game_json["home_team_id"],
                            game_json["away_team_id"],
                            league["league_id"],
                            division["division_id"],
                            field=game_json["field"])
                self.session.add(game)
            except Exception as error:
                game_list = [str(value) for value in game_json.values()]
                game_info = "-".join(game_list)
                self.warnings.append(INVALID_GAME.format(game_info,
                                                         str(error)))
        self.session.commit()
        handle_table_change(Tables.GAME)


def get_team_lookup(league, year=datetime.datetime.today().year):
    '''
    a method that sets the teams for the league
    Parameters:
        league: the json league object
        year: the year we are importing for
    Returns:
        teams: a dictionary object lookup for teams
    '''
    teams = {}
    league = League.query.get(league["league_id"])
    if league is None:
        raise LeagueDoesNotExist(payload={'details': league})
    for team in league.teams:
        if team.year == year:
            teams[str(team)] = team.id
            sponsor = str(Sponsor.query.get(team.sponsor_id))
            teams[sponsor + " " + team.color] = team.id
    return teams


def extract_column_indices_lookup(header):
    """ Returns a dictionary used to lookup indices for various fields
    Parameters:
        header: the header array
    Returns:
        a dictionary {str(field): int(index)}
    """
    lookup = {}
    for i in range(0, len(header)):
        for key, value in HEADERS.items():
            if is_entry_a_header(key, value, header[i]):
                lookup[key.lower()] = i

    # ensure all headers were found
    for key in HEADERS.keys():
        if key not in lookup.keys():
            error_message = "{} header missing".format(key.lower())
            raise InvalidField(payload={'details': error_message})
    return lookup


def is_entry_a_header(key, value, entry):
    """Returns whether the given entry in the header is a expected header."""
    return (key.lower() in entry.lower() or
            value.lower() in entry.lower())


def is_game_row_valid(game, lookup):
    """Returns whether all columns can be found in the game entry.
    Parameters:
        game: the entry for the game
        lookup: a lookup for fields to indexes in columns
    Returns:
        true if valid row otherwise False
    """
    for index in lookup.values():
        if index > len(game):
            return False
    return True


def extract_game(game, team_lookup, lookup):
    """Returns a game json object
    Parameters:
        game: the entry for the game
        team_lookup: a lookup for team names to player ids
        lookup: a lookup for fields to indexes in columns
    Returns:
        a json game object, None if game data not found
    """
    if not is_game_row_valid(game, lookup):
        return None
    away = game[lookup["away"]].strip()
    home = game[lookup["home"]].strip()
    time = game[lookup["time"]].strip()
    field = game[lookup["field"]].strip()
    date = game[lookup["date"]].strip()
    # check if variables meet certain conditions
    # else should be good to add game
    away_team = team_lookup.get(away, None)
    home_team = team_lookup.get(home, None)
    if away_team is None:
        error_message = INVALID_TEAM.format(away)
        raise TeamDoesNotExist(payload={'details': error_message})
    if home_team is None:
        error_message = INVALID_TEAM.format(home)
        raise TeamDoesNotExist(payload={'details': error_message})
    return {"away_team_id": away_team,
            "home_team_id": home_team,
            "time": time,
            "field": field,
            "date": date}


def extract_games(games, team_lookup, lookup):
    """Returns a dictionary with list of games and warnings
    Parameters:
        games: the games entry rows
        team_lookup: a lookup for team names to the team ids
        lookup: a lookup for column indices
    Returns:
        a dictionary with a list of games and a list of warnings
    """
    result = []
    warnings = []
    for game in games:
        try:
            game = extract_game(game, team_lookup, lookup)
            if game is not None:
                result.append(game)
        except TeamDoesNotExist as e:
            warnings.append(TEAM_NOT_FOUND.format(str(e), ",".join(game)))
    return {"games": result, "warnings": warnings}


def extract_background(background):
    """Returns a dictionary of the extracted json objects from the background.
    Parameters:
        background: dictionary of sponsor, color, captain, league
    Returns:
        a dictionary of league model
    """
    background_keys = [key.lower() for key in background.keys()]
    for value in BACKGROUND.values():
        if value.lower() not in background_keys:
            errorMessage = MISSING_BACKGROUND.format(value)
            raise InvalidField(payload={"details": errorMessage})

    # ensure able to find the division
    division_name = background['division']
    if division_name.lower().startswith("ex."):
        error_message = LEFT_BACKGROUND_EXAMPLE.format(division_name)
        raise InvalidField(payload={"details": error_message})
    division = Division.query.filter(func.lower(Division.name) ==
                                     func.lower(division_name)).first()

    # ensure able to find the league
    league_name = background['league']
    if league_name.lower().startswith("ex."):
        error_message = LEFT_BACKGROUND_EXAMPLE.format(league_name)
        raise InvalidField(payload={"details": error_message})
    league = League.query.filter(func.lower(League.name) ==
                                 func.lower(league_name)).first()
    if division is None:
        error_message = INVALID_DIVISION.format(division_name)
        raise DivisionDoesNotExist(payload={'details': error_message})
    if league is None:
        error_message = INVALID_LEAGUE.format(league_name)
        raise LeagueDoesNotExist(payload={'details': error_message})
    return {"league": league.json(), "division": division.json()}


def clean_cell(cell):
    """Returns a clean cell"""
    return cell.strip().lower().replace(":", "")


def parse_parts(lines, delimiter=","):
    """Parses the lines and returns a dictionary with the three parts
    Parameters:
        lines: a list of lines
        delimiter: the delimiter for the lines (default = ,)
    Returns:
        a dictionary with background, header, games, warnings where:
            background: dictionary of league
            header: the header row
            games: a list of games lines
            warnings: a list of lines that were not recognized
    """
    background = {}
    header = None
    games = []
    warnings = []
    header_keywords = ([key.lower() for key in HEADERS.keys()] +
                       [value.lower() for value in HEADERS.values()])
    background_keywords = ([key.lower() for key in BACKGROUND.keys()] +
                           [value.lower() for value in BACKGROUND.values()])
    for line in lines:
        info = line.split(delimiter)
        if clean_cell(info[0]).lower() in background_keywords:
            background[clean_cell(info[0])] = info[1].strip()
        elif info[0].lower().strip() in header_keywords:
            header = info
        elif len(info) >= len(HEADERS.keys()):
            games.append(info)
        else:
            warnings.append(INVALID_ROW.format(line))
    return {'background': background,
            'header': header,
            'games': games,
            'warnings': warnings}
