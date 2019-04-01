'''
@author: Dallas Fraser
@date: 2016-04-12
@organization: MLSB API
@summary: Holds a class TeamList that helps imports a team roster
'''
# imports
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
INVALID_ROW = "Unsure what to do with the following row: {}"
PLAYER_ROW_IDENTIFIER = "player"

# a dictionary of the headers needed with their keys
#and how they appear in csv
HEADERS = {"name": "Player Name",
           "email": "Player Email",
           "gender": "Gender (M/F)"}

# a dictionary of the background needed with their keys
#and how they appear in csv
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
        if (league.lower().startswith("ex.")or
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


def get_column_indices_lookup(header):
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


def parse_player_information(info, lookup):
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
    player = Player.query.filter(Player.email ==
                                 player_json['email'].lower()).first()
    if player is not None:
        player_id = player.id
    player_json['player_id'] = player_id
    return 


def extract_players(players, lookup, delimiter=","):
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
            player = parse_player_information(info, lookup)
            if player['name'].lower().startswith("ex."):
                warning = "Player example was left - {}".format(" ".join(info))
                warnings.append(warning)
            else:
                players_info.append(player)
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
            background: list of sponsor, color, captain, league
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
