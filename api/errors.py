'''
@author: Dallas Fraser
@author: 2015-11-21
@organization: MLSB API
@summary: Holds the errors for the database
'''
ERROR = 431
IFSC = ERROR + 1
PDNESC = ERROR + 2
TDNESC = ERROR + 3
LDNESC = ERROR + 4
GDNESC = ERROR + 5
SDNESC = ERROR + 6
NUESC = ERROR + 7
THCSC = ERROR + 8
MPSC = ERROR + 9

class TeamDoesNotExist(Exception):
    status_code = TDNESC
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class PlayerDoesNotExist(Exception):
    status_code = PDNESC
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class GameDoesNotExist(Exception):
    status_code = GDNESC
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class InvalidField(Exception):
    status_code = IFSC
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class LeagueDoesNotExist(Exception):
    status_code = LDNESC
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class SponsorDoesNotExist(Exception):
    status_code = SDNESC
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class TeamAlreadyHasCaptain(Exception):
    status_code = THCSC
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class MissingPlayer(Exception):
    status_code = MPSC
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class NonUniqueEmail(Exception):
    status_code = NUESC
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
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
            }
          }