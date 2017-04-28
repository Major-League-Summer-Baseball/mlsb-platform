'''
@author: Dallas Fraser
@date: 2016-04-12
@organization: MLSB API
@summary: Holds a class LeagueList that helps imports a League (list of games)
'''
# imports
from api.model import Sponsor, Team, Game, League
from api import DB
from api.validators import time_validator, string_validator, date_validator
from api.errors import InvalidField, LeagueDoesNotExist
import logging
# constants
CREATED = "Created Team (no league was specified)"
NO_LEAGUE = "Cannot find league, please ensure spelt correctly or create the league"
INVALID_FILE = "File was not given in right format (use template)"
EXAMPLE_FOUND = "First entry contain the templates example, just skipped it"
EMAIL_NAME = "Player {} email was found but had different name"
INVALID_FIELD = "{} had an invalid field"
INVALID_TEAM = "{} is not a team in the league"


class LeagueList():
    def __init__(self, lines, logger=None):
        self.success = False
        self.errors = []
        self.warnings = []
        self.lines = lines
        if logger is None:
            logging.basicConfig(level=logging.INFO,
                                format='%(asctime)s %(message)s')
            logger = logging.getLogger(__name__)
        self.logger = logger

    def import_league(self):
        '''
        a method that imports a bunch of games for a league
        based on a csv template
        Parameters:

        Updates:
            success: a boolean if the import was successful (boolean)
            errors: a list of possible error (list)
            warnings: a list of possible warnings (list)
        '''
        if self.lines is None:
            raise InvalidField("No lines were provided")
        if self.check_header(self.lines[0:2]):
                league, headers = self.parse_header(self.lines[0:2])
                self.logger.debug("Getting League ID")
                self.league_id = self.get_league_id(league)
                self.logger.debug("Got League id {}".format(self.league_id))
                self.set_columns_indices(headers)
                self.logger.debug("Got set column indcides")
                if self.league_id is not None:
                    self.set_teams()
                    games = self.lines[2:]
                    for game in games:
                        self.logger.debug(game)
                        self.import_game(game)
                        self.logger.debug("Done Import")
        else:
            self.errors.append(INVALID_FILE)
        if len(self.errors) < 1:
            self.logger.debug("Committing")
            # no major errors so commit changes
            DB.session.commit()
        return

    def get_league_id(self, league):
        '''
        a method that gets the league id for the name
        Parameters:
            league: the league's name (str)
        Returns:
            id: the id of the team (int) None if no league is found
        '''
        identification = None
        league = League.query.filter_by(name=league).first()
        if league is not None:
            identification = league.id
        else:
            # cant assume some league so return None
            s = "League does not exist: {}".format(league)
            raise LeagueDoesNotExist(payload={"details": s})
        return identification

    def set_teams(self):
        '''
        a method that sets the teams for the league
        Parameters:
            None
        Updates:
            self.teams: a dictionary with {name:id, etc..}
        '''
        self.teams = {}
        league = League.query.get(self.league_id)
        if league is None:
            raise LeagueDoesNotExist(payload={'details': league})
        for team in league.teams:
            self.teams[str(team)] = team.id
            sponsor = str(Sponsor.query.get(team.sponsor_id))
            self.teams[sponsor + " " + team.color] = team.id

    def set_columns_indices(self, headers):
        '''
        a method that set the indices for the column headers
        Parameters:
            headers: the list of headers (list of str)
        Returns:
        '''
        for i in range(0, len(headers)):
            if "home team" in headers[i].lower():
                self.home_index = i
            elif "away team" in headers[i].lower():
                self.away_index = i
            elif "date" in headers[i].lower():
                self.date_index = i
            elif "time" in headers[i].lower():
                self.time_index = i
            elif "field" in headers[i].lower():
                self.field_index = i
        return

    def import_game(self, info):
        '''
        a method the imports one game
        Parameters:
            info: the string that contains the information of a player (str)
        Returns:
        '''
        info = info.split(",")
        if (len(info) < self.away_index or
            len(info) < self.home_index or
            len(info) < self.time_index or
            len(info) < self.field_index or
            len(info) < self.date_index):
            s = "Game did not have the right number of fields"
            self.logger.debug(s)
            return  # probably just an empty line
        away = info[self.away_index].strip()
        home = info[self.home_index].strip()
        time = info[self.time_index].strip()
        field = info[self.field_index].strip()
        date = info[self.date_index].strip()
        # check if variables meet certain conditions
        # else should be good to add game
        away_team = self.teams.get(away, None)
        home_team = self.teams.get(home, None)
        if away_team is None:
            self.errors.append(INVALID_TEAM.format(away))
        if home_team is None:
            self.errors.append(INVALID_TEAM.format(home))
        if away_team is not None and home_team is not None:
            # else should be good to add the game
            game = Game(
                        date,
                        time,
                        home_team,
                        away_team,
                        self.league_id,
                        field=field)
            DB.session.add(game)
        return

    def check_header(self, header):
        '''
        a method that checks if the header is valid
        Parameters:
            header: the header to check (list of str)
        Returns:
            valid: True if the header meets the template (boolean)
        '''
        valid = True 
        if len(header) < 2:
            valid = False
        elif len(header[0].split(",")) < 2 or len(header[1].split(",")) < 5:
            valid = False
        else:
            columns = header[1].lower()
            if "home team" not in columns:
                valid = False
            elif "away team" not in columns:
                valid = False
            elif "date" not in columns:
                valid = False
            elif "time" not in columns:
                valid = False
            elif "field" not in columns:
                valid = False
        return valid

    def parse_header(self, header):
        '''
        a method that parses the header
        Parameters:
            header: the header to check (list of str)
        Returns:
            league: the mame of the league (str)
            headers: the column headers (list)
        '''
        first = header[0].split(",")
        league = first[1]
        headers = header[1].split(",")
        return league, headers
