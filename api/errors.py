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
PNS = 401
NTCSC = 401
BRSC = 400
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
    status_code = NTCSC
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

class BadRequestError(Exception):
    status_code = BRSC
    message = "Bad request"
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
                'message': InvalidField.message,
                'status_code': InvalidField.status_code,
            },
            'PlayerDoesNotExist': {
                'message': PlayerDoesNotExist.message,
                'status_code': PlayerDoesNotExist.status_code,
            },
            'TeamDoesNotExist': {
                'message': TeamDoesNotExist.message,
                'status_code': TeamDoesNotExist.status_code,
            },
            'LeagueDoesNotExist': {
                'message': LeagueDoesNotExist.message,
                'status_code': LeagueDoesNotExist.status_code,
            },
            'SponsorDoesNotExist': {
                'message': SponsorDoesNotExist.message,
                'status_code': SponsorDoesNotExist.status_code,
            },
            'GameDoesNotExist': {
                'message': GameDoesNotExist.message,
                'status_code': GameDoesNotExist.status_code,
            },
            'NonUniqueEmail': {
                'message': NonUniqueEmail.message,
                'status_code': NonUniqueEmail.status_code,
            },
            'NotTeamCaptain': {
                              'message': NotTeamCaptain.message,
                              'status_code': NotTeamCaptain.status_code
                              },
           'PlayerNotSubscribed': {
                              'message': PlayerNotSubscribed.message,
                              'status_code': PlayerNotSubscribed.status_code
                              },
            'PlayerNotOnTeam': {
                              'message': PlayerNotOnTeam.message,
                              'status_code': PlayerNotOnTeam.status_code
                              },
            'EspysDoesNotExist': {
                              'message': EspysDoesNotExist.message,
                              'status_code': EspysDoesNotExist.status_code
                              },
            'BatDoesNotExist': {
                              'message': BatDoesNotExist.message,
                              'status_code': BatDoesNotExist.status_code
                              },
            'TeamAlreadyHasCaptain': {
                              'message': TeamAlreadyHasCaptain.message,
                              'status_code': TeamAlreadyHasCaptain.status_code
                              },
            'BadRequestError':{
                          'message': BadRequestError.message,
                          'status_code': BadRequestError.status_code
                          }
          }