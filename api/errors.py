'''
@author: Dallas Fraser
@author: 2015-11-21
@organization: MLSB API
@summary: Holds the errors for the database
'''
class TeamDoesNotExist(Exception):
    pass

class PlayerDoesNotExist(Exception):
    pass

class GameDoesNotExist(Exception):
    pass

class InvalidField(Exception):
    status_code = 409
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
    pass

class SponsorDoesNotExist(Exception):
    pass

class TeamAlreadyHasCaptain(Exception):
    pass

class NonUniqueEmail(Exception):
    pass

ERRORS = {
            'InvalidField': {
                'message': "A field given was invalid",
                'status': 409,
            },
            'PlayerDoesNotExist': {
                'message': "The player requested does not exist",
                'status': 410,
            },
            'TeamDoesNotExist': {
                'message': "The team requested does not exist",
                'status': 411,
            },
            'LeagueDoesNotExist': {
                'message': "The league requested does not exist",
                'status': 412,
            },
            'SponsorDoesNotExist': {
                'message': "The sponsor requested does not exist",
                'status': 413,
            },
            'GameoesNotExist': {
                'message': "The game requested does not exist",
                'status': 413,
            },
            'NonUniqueEmail': {
                'message': "The player's email was not unique",
                'status': 414,
            }
          }
