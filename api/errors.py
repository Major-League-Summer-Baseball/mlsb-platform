'''
@author: Dallas Fraser
@author: 2016-04-12
@organization: MLSB API
@summary: Holds the errors for the database
'''
ERROR = 431
IFSC = 400
PDNESC = 404
TDNESC = 404
LDNESC = 404
GDNESC = 404
SDNESC = 404
BDNESC = 404
EDNESC = 404
NUESC = 400
THCSC = 400
MPSC = 400
PNOT = 400
PAST = 400
PNS = 400
NTCSC = 401
class TeamDoesNotExist(Exception):
    status_code = TDNESC
    message = "Team does not exist"
    def __init__(self, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = self.message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class PlayerDoesNotExist(Exception):
    status_code = PDNESC
    message = "Player does not exist"
    def __init__(self, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = self.message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class GameDoesNotExist(Exception):
    status_code = GDNESC
    message = "Game does not exist"
    def __init__(self, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = self.message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class InvalidField(Exception):
    status_code = IFSC
    message = "Invalid field"
    def __init__(self, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = self.message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class LeagueDoesNotExist(Exception):
    status_code = LDNESC
    message = "League does not exist"
    def __init__(self, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = self.message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class SponsorDoesNotExist(Exception):
    status_code = SDNESC
    message = "Sponsor does not exist"
    def __init__(self, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = self.message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class TeamAlreadyHasCaptain(Exception):
    status_code = THCSC
    message = "Team has captain already"
    def __init__(self, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = self.message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class BatDoesNotExist(Exception):
    status_code = BDNESC
    message = "Bat does not exist"
    def __init__(self, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = self.message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class EspysDoesNotExist(Exception):
    status_code = EDNESC
    message = "Espys does not exist"
    def __init__(self, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = self.message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class NonUniqueEmail(Exception):
    status_code = NUESC
    message = "Email is not unique"
    def __init__(self, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = self.message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class PlayerNotOnTeam(Exception):
    status_code = PNOT
    message = "Player is not on team"
    def __init__(self, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = self.message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class PlayerNotSubscribed(Exception):
    status_code = PNS
    message = "Player is not subscribed"
    def __init__(self, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = self.message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class NotTeamCaptain(Exception):
    status_code = THCSC
    message = "Not team's captain"
    def __init__(self, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = self.message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
    
ERRORS = {
            'InvalidField': {
                'message': "A field given was invalid",
                'status': IFSC,
            },
            'PlayerDoesNotExist': {
                'message': "The player requested does not exist",
                'status': PDNESC,
            },
            'TeamDoesNotExist': {
                'message': "The team requested does not exist",
                'status': TDNESC,
            },
            'LeagueDoesNotExist': {
                'message': "The league requested does not exist",
                'status': LDNESC,
            },
            'SponsorDoesNotExist': {
                'message': "The sponsor requested does not exist",
                'status': SDNESC,
            },
            'GameoesNotExist': {
                'message': "The game requested does not exist",
                'status': GDNESC,
            },
            'NonUniqueEmail': {
                'message': "The player's email was not unique",
                'status': NUESC,
            },
            'MissingPlayer': {
                              'message': "Player was not a member of the team",
                              'status': 400
                              }
          }