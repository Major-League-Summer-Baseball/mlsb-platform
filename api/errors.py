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
    pass

class LeagueDoesNotExist(Exception):
    pass

class SponsorDoesNotExist(Exception):
    pass

class TeamAlreadyHasCaptain(Exception):
    pass

class NonUniqueEmail(Exception):