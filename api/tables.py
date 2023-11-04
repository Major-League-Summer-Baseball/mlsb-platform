from enum import Enum


class Tables(Enum):
    """An enumeration of all table

    The tables of MLSB:
        * BAT
        * DIVISION
        * ESYPS
        * GAME
        * LEAGUE
        * SPONSOR
        * PLAYER
        * TEAM
    """
    BAT = 'bat'
    DIVISION = 'division'
    ESPYS = 'esyps'
    FUN = 'fun'
    GAME = 'game'
    LEAGUE = 'league'
    SPONSOR = 'sponsor'
    PLAYER = 'player'
    TEAM = 'team'

    def __str__(self):
        """Returns the string representation of the role"""
        return self.value
