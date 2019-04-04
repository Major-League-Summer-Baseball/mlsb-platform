'''
@author: Dallas Fraser
@date: 2016-04-12
@organization: MLSB API
@summary: Holds a class TeamList that helps imports a team roster
'''
# imports
from sqlalchemy import func, or_
from api.model import Sponsor, Team, Player, League
from api import DB
from datetime import date
from api.errors import InvalidField, SponsorDoesNotExist, LeagueDoesNotExist
import logging

# constants
CREATED = "Created Team (no league was specified)"
NO_SPONSOR = "No sponsor, please ensure spelt correctly or create sponsor"
INVALID_FILE = "File was not given in right format (use template)"
EXAMPLE_FOUND = "First entry contain the templates example, just skipped it"
EMAIL_NAME = "Player {} email was found but had different name"
INVALID_FIELD = "{} had an invalid field"
MISSING_BACKGROUND = "Missing background: {}"
LEFT_BACKGROUND_EXAMPLE = "Background example was left: {}"
LEFT_PLAYER_EXAMPLE = "Player example was left:  {}"
INVALID_SPONSOR = "Sponsor given was not found: {}"
INVALID_LEAGUE = "League given was not found: {}"
INVALID_PLAYER = "Player given {} had the following issue: {}"
PLAYER_MISMATCH_COLUMNS = "Player mismatched the headers: {}"
INVALID_ROW = "Unsure what to do with the following row: {}"
PLAYER_ROW_IDENTIFIER = "player"
CAPTAIN_NOT_ASSIGNED = "Captain was not assigned"

# a dictionary of the headers needed with their keys
# and how they appear in csv
HEADERS = {"name": "Player Name",
           "email": "Player Email",
           "gender": "Gender (M/F)"}

# a dictionary of the background needed with their keys
# and how they appear in csv
BACKGROUND = {"sponsor_name": "sponsor",
              "team_color": "color",
              "captain_name": "captain",
              "league_name": "league"}


class TeamList():
    def __init__(self, lines, logger=None, session=None):
        """The constructor

            lines: a list of lines parsed from csv
            logger: a logger
            session: a mocked database session
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
        self.team = None
        self.captain_name = None
        self.captain = None
        self.name_index = None
        self.email_index = None
        self.gender_index = None
        self.session = session
        if session is None:
            self.session = DB.session

    def add_team_functional(self):
        """ Add a team to the database using functions instead of methods"""
        # parse out the parts - background, header, players
        parts = parse_lines(self.lines)
        self.warnings = parts['warnings']

        # extract the background such a league, sponsor and color
        background = extract_background(parts['background'])

        # extract the players using the header as lookup
        lookup = extract_column_indices_lookup(parts['header'])
        players = extract_players(parts["players"], lookup)
        self.warnings = self.warnings + players['warnings']

        # add the players
        player_models = []
        for player_json in players['player_info']:
            try:
                if (player_json['player_id'] is None):
                    # need to create the player
                    player = Player(player_json['name'],
                                    player_json['email'],
                                    gender=player_json["gender"])
                    self.session.add(player)
                    self.session.commit()
                else:
                    email = player_json['email']
                    player = Player.query.filter(func.lower(Player.email) ==
                                                 func.lower(email)).first()
                player_models.append(player.json())
            except Exception as error:
                player_info = "-".join([player_json["name"],
                                        player_json["email"]])
                self.warnings.append(INVALID_PLAYER.format(player_info,
                                                           str(error)))

        # get the team, create if does not exist
        if background['team']['team_id'] is None:
            team = Team(color=background['team']['color'],
                        sponsor_id=background['sponsor']['sponsor_id'],
                        league_id=background['league']['league_id'],
                        year=date.today().year)
            self.session.add(team)
        else:

            # get the team and remove all players
            team = Team.query.get(background['team']['team_id'])
            team.players = []
        set_captain = False
        for player in player_models:
            if (player["player_name"].lower()
               == background["captain"]["player_name"].lower()):
                set_captain = True
                team.insert_player(player["player_id"], captain=True)
            else:
                team.insert_player(player["player_id"], captain=False)
        if not set_captain:
            self.warnings.append(CAPTAIN_NOT_ASSIGNED)
        self.session.commit()

    def add_team(self):
        """Adds a team to the database"""
        player_index = self.import_headers()
        self.logger.debug(self.lines[player_index - 1])
        self.set_columns_indices(self.lines[player_index - 1].split(","))
        self.logger.debug(self.name_index, self.email_index, self.gender_index)
        self.import_players(player_index)
        self.logger.debug("Imported players")
        # should be good no errors were raised
        self.session.commit()
        if self.captain is None:
            self.warnings.append("Captain was not assigned")
        else:
            # set the captain
            self.team.player_id = self.captain.id
            self.session.commit()
        self.logger.debug("Captain set")
        return

    def import_headers(self):
        """Parse the headers of the csv and add team"""
        done = False
        i = 0
        sponsor = None
        color = None
        captain = None
        league = None
        while not done:
            # read the headers
            line = self.lines[i]
            columns = line.split(",")
            if self.clean_cell(columns[0]) == "sponsor":
                sponsor = columns[1].strip()
            elif self.clean_cell(columns[0]) == "color":
                color = columns[1].strip()
            elif self.clean_cell(columns[0]) == "captain":
                captain = columns[1].strip()
            elif self.clean_cell(columns[0]) == "league":
                league = columns[1].strip()
            else:
                # assuming done reading the headers
                done = True
            i += 1
        player_index = i
        if sponsor is None:
            raise InvalidField(payload={"details": "No sponsor was given"})
        if captain is None:
            raise InvalidField(payload={"details": "No captain was given"})
        if color is None:
            raise InvalidField(payload={"details": "No color was given"})
        if league is None:
            raise InvalidField(payload={"details": "No league was given"})
        # check no examples were left and actually real info
        if (league.lower().startswith("ex.") or
            sponsor.lower().startswith("ex.") or
            color.lower().startswith("ex.") or
            captain.lower().startswith("ex.")):
            t = "The header's still had an example"
            raise InvalidField(payload={"details": t})
        sponsor_id = (DB.session.query(Sponsor).filter(Sponsor.name == sponsor)
                      .first())
        if sponsor_id is None:
            sponsor_id = (DB.session.query(Sponsor)
                          .filter(Sponsor.nickname == sponsor)
                          .first())
        if sponsor_id is None:
            # what kind of sponsor are you giving
            t = "The sponsor does not exist (check case)"
            raise SponsorDoesNotExist(payload={'details': t})
        sponsor_id = sponsor_id.id
        league_id = (DB.session.query(League)
                     .filter(League.name == league)).first()
        if league_id is None:
            t = "The league does not exist (check case)"
            raise LeagueDoesNotExist(payload={"details": t})
        league_id = league_id.id
        # check to see if team was already created
        teams = (DB.session.query(Team)
                 .filter(Team.color == color)
                 .filter(Team.sponsor_id == sponsor_id)
                 .filter(Team.year == date.today().year).all())
        team_found = None
        if len(teams) > 0:
            team_found = teams[0]
        # was the team not found then should create it
        if team_found is None:
            self.warnings.append("Team was created")
            team_found = Team(color=color,
                              sponsor_id=sponsor_id,
                              league_id=league_id)
        else:
            team_found.players = []  # remove all the players before
        self.team = team_found  # set the team
        self.captain_name = captain  # remember captains name
        return player_index

    def import_players(self, player_index):
        """Import a list of players"""
        while (player_index < len(self.lines) and
               len(self.lines[player_index].split(",")) > 1):
            info = self.lines[player_index].split(",")
            self.logger.debug(info, len(info))
            if len(info) < 3:
                raise InvalidField(payload={"details": "Missing a category"})
            name = info[self.name_index].strip()
            email = info[self.email_index].strip()
            gender = info[self.gender_index].strip()
            if not name.lower().startswith("ex."):
                player = (DB.session.query(Player)
                            .filter(Player.email == email)).first()
                if player is None:
                    self.logger.debug(name + " " + email + " " + gender)
                    player = Player(name, email, gender=gender)
                    self.session.add(player)
                    self.logger.debug("Player was created")
                else:
                    # this player is active
                    player.active = True
                self.team.players.append(player)
                if name == self.captain_name:
                    self.captain = player
            else:
                self.warnings.append("Player Example was left")
            player_index += 1
        return

    def clean_cell(self, cell):
        """Returns a clean cell"""
        return cell.strip().lower().replace(":", "")

    def set_columns_indices(self, header):
        '''
        a method that set the indices for the column headers
        Parameters:
            header: the list of columns for the header (list of str)
        Returns:
        '''
        for i in range(0, len(header)):
            if "email" in header[i].lower():
                self.email_index = i
            elif "name" in header[i].lower():
                self.name_index = i
            elif "gender" in header[i].lower():
                self.gender_index = i
        if self.email_index is None:
            raise InvalidField(payload={'details': "Email header missing"})
        if self.name_index is None:
            raise InvalidField(payload={'details': "Player header missing"})
        if self.gender_index is None:
            raise InvalidField(payload={'details': "Gender header missing"})
        return


def extract_background(background):
    """Returns a dictionary of the extracted json objects from the background.
    Parameters:
        background: dictionary of sponsor, color, captain, league
    Returns:
        a dictionary of sponsor model, team model, player model, league model
    """
    for value in BACKGROUND.values():
        if value not in background.keys():
            errorMessage = MISSING_BACKGROUND.format(value)
            raise InvalidField(payload={"details": errorMessage})
    league_name = background['league']
    sponsor_name = background['sponsor']
    team_color = background['color']
    captain_name = background['captain']
    if league_name.lower().startswith("ex."):
        error_message = LEFT_BACKGROUND_EXAMPLE.format(league_name)
        raise InvalidField(payload={"details": error_message})
    elif sponsor_name.lower().startswith("ex."):
        error_message = LEFT_BACKGROUND_EXAMPLE.format(sponsor_name)
        raise InvalidField(payload={"details": error_message})
    elif team_color.lower().startswith("ex."):
        error_message = LEFT_BACKGROUND_EXAMPLE.format(team_color)
        raise InvalidField(payload={"details": error_message})
    elif captain_name.lower().startswith("ex."):
        error_message = LEFT_BACKGROUND_EXAMPLE.format(captain_name)
        raise InvalidField(payload={"details": error_message})

    # nothing to do with the captain at this point
    captain = {"player_name": captain_name}

    # try to find sponsor and league
    sponsor = (Sponsor.query.filter(or_(func.lower(Sponsor.name)
                                        == func.lower(sponsor_name)),
                                    func.lower(Sponsor.nickname)
                                    == func.lower(sponsor_name))
               ).first()
    league = League.query.filter(func.lower(League.name)
                                 == func.lower(league_name)).first()
    if sponsor is None:
        error_message = INVALID_SPONSOR.format(sponsor_name)
        raise SponsorDoesNotExist(payload={'details': error_message})
    if league is None:
        error_message = INVALID_LEAGUE.format(league_name)
        raise LeagueDoesNotExist(payload={'details': error_message})

    # check to see if team was already created
    teams = (Team.query
             .filter(func.lower(Team.color) == func.lower(team_color))
             .filter(Team.sponsor_id == sponsor.id)
             .filter(Team.year == date.today().year)).all()
    if len(teams) > 0:
        team = teams[0].json()
    else:
        team = {'team_id': None,
                "color": team_color,
                "sponsor_id": sponsor.id,
                "league_id": league.id,
                "captain": None,
                "year": date.today().year}
    return {"captain": captain,
            "team": team,
            "league": league.json(),
            "sponsor": sponsor.json()}


def extract_column_indices_lookup(header):
    """ Returns a dictionary used to lookup indices for various fields
    Parameters:
        header: the header array
    Returns:
        a dictionary {str(field): int(index)}
    """
    lookup = {}
    for i in range(0, len(header)):
        if "email" in header[i].lower():
            lookup["email"] = i
        elif "name" in header[i].lower():
            lookup["name"] = i
        elif "gender" in header[i].lower():
            lookup["gender"] = i
    if "email" not in lookup:
        raise InvalidField(payload={'details': "Email header missing"})
    if "name" not in lookup:
        raise InvalidField(payload={'details': "Player header missing"})
    if "gender" not in lookup:
        raise InvalidField(payload={'details': "Gender header missing"})
    return lookup


def extract_player_information(info, lookup):
    """Parse a player and return a json object
    Parameters:
        info: a list of information about player
        lookup: the lookup for what fields and their indices in the info list
    Return:
        a dictionary {'player_id': int,
                      'name': str,
                      'email': str,
                      'gender': str}
    """
    player_json = {}
    for key, value in lookup.items():
        player_json[key] = info[value].strip()
    player_id = None
    player = Player.query.filter(func.lower(Player.email) ==
                                 func.lower(player_json['email'])).first()
    if player is not None:
        player_id = player.id
    player_json['player_id'] = player_id
    return player_json


def extract_players(players, lookup):
    """Extract the players and return a list of players in json format
    Parameters:
        players: a list of rows that contain player information
        lookup: the lookup for what fields and their indices in the players
    Return:
        a dictionary with players_info, warnings
        where
            players_info: an array of dictionary {'player_id': int,
                                                 'name': str,
                                                 'email': str,
                                                 'gender': str}
            warnings: a list of warnings encountered
    """
    players_info = []
    warnings = []
    for info in players:
        if len(info) == len(lookup):
            player = extract_player_information(info, lookup)
            if player['name'].lower().startswith("ex."):
                warnings.append(LEFT_PLAYER_EXAMPLE.format(" ".join(info)))
            else:
                players_info.append(player)
        else:
            warnings.append(PLAYER_MISMATCH_COLUMNS.format(" ".join(info)))
    return {'player_info': players_info, 'warnings': warnings}


def clean_cell(cell):
    """Returns a clean cell"""
    return cell.strip().lower().replace(":", "")


def parse_lines(lines, delimiter=","):
    """Parses the lines and returns a tuple with the three parts
    Parameters:
        lines: a list of lines
    Returns:
        a dictionary with background, header, players, warnings where:
            background: dictionary of sponsor, color, captain, league
            header: the header row
            players: a list of player lines
            warnings: a list of lines that were not recognized
    """
    background = {}
    header = None
    players = []
    warnings = []
    for line in lines:
        info = line.split(delimiter)
        if clean_cell(info[0]) in BACKGROUND.values():
            background[clean_cell(info[0])] = info[1].strip()
        elif PLAYER_ROW_IDENTIFIER in info[0].lower().strip():
            header = info
        elif len(info) >= len(HEADERS.keys()):
            players.append(info)
        else:
            warnings.append(INVALID_ROW.format(line))
    return {'background': background,
            'header': header,
            'players': players,
            'warnings': warnings}
