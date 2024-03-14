ERROR = 431
IFSC = 400
PDNESC = 404
TDNESC = 404
LDNESC = 404
GDNESC = 404
SDNESC = 404
BDNESC = 404
JLRDNESC = 404
EDNESC = 404
FDNESC = 404
NUESC = 400
THCSC = 400
MPSC = 400
LNPOT = 400
PNOT = 400
PAST = 400
PNS = 401
NTCSC = 401
BRSC = 400
OAESC = 400
HLRESC = 403
NPOLESC = 403


class BaseException(Exception):
    status_code = FDNESC
    message = "Fun count does not exist"

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

    def __str__(self):
        return f"{self.status_code}:{self.message} with {self.payload}"


class FunDoesNotExist(BaseException):
    status_code = FDNESC
    message = "Fun count does not exist"


class TeamDoesNotExist(BaseException):
    status_code = TDNESC
    message = "Team does not exist"


class PlayerDoesNotExist(BaseException):
    status_code = PDNESC
    message = "Player does not exist"


class GameDoesNotExist(BaseException):
    status_code = GDNESC
    message = "Game does not exist"


class InvalidField(BaseException):
    status_code = IFSC
    message = "Invalid field"


class LeagueDoesNotExist(BaseException):
    status_code = LDNESC
    message = "League does not exist"


class LeagueEventDoesNotExist(BaseException):
    status_code = LDNESC
    message = "League event does not exist"


class LeagueEventDateDoesNotExist(BaseException):
    status_code = LDNESC
    message = "League event date does not exist"


class DivisionDoesNotExist(BaseException):
    status_code = LDNESC
    message = "Division does not exist"


class SponsorDoesNotExist(BaseException):
    status_code = SDNESC
    message = "Sponsor does not exist"


class TeamAlreadyHasCaptain(BaseException):
    status_code = THCSC
    message = "Team has captain already"


class BatDoesNotExist(BaseException):
    status_code = BDNESC
    message = "Bat does not exist"


class RequestDoesNotExist(BaseException):
    status_code = JLRDNESC
    message = "League Request does not exist"


class EspysDoesNotExist(BaseException):
    status_code = EDNESC
    message = "Espys does not exist"


class NonUniqueEmail(BaseException):
    status_code = NUESC
    message = "Email is not unique"


class TeamNotPartOfLeague(BaseException):
    status_code = LNPOT
    message = "Team not part of league"


class PlayerNotOnTeam(BaseException):
    status_code = PNOT
    message = "Player is not on team"


class PlayerNotSubscribed(BaseException):
    status_code = PNS
    message = "Player is not subscribed"


class NotTeamCaptain(BaseException):
    status_code = NTCSC
    message = "Not team's captain"


class BadRequestError(BaseException):
    status_code = BRSC
    message = "Bad request"


class OAuthException(BaseException):
    """An exception while dealing with oauth provider."""
    status_code = OAESC
    message = "Exception when dealing with OAuth Provider"


class HaveLeagueRequestException(BaseException):
    """An exception when same email requests to join twice"""
    status_code = HLRESC
    message = "League Request already sent"


class NotPartOfLeagueException(BaseException):
    """An exception when player not part of league yet."""
    status_code = NPOLESC
    message = "Not part of the league"


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
    'LeagueEventDoesNotExist': {
        'message': LeagueEventDoesNotExist.message,
        'status_code': LeagueEventDoesNotExist.status_code,
    },
    'LeagueEventDateDoesNotExist': {
        'message': LeagueEventDateDoesNotExist.message,
        'status_code': LeagueEventDateDoesNotExist.status_code,
    },
    'DivisionDoesNotExist': {
        'message': DivisionDoesNotExist.message,
        'status_code': DivisionDoesNotExist.status_code,
    },
    'SponsorDoesNotExist': {
        'message': SponsorDoesNotExist.message,
        'status_code': SponsorDoesNotExist.status_code,
    },
    'GameDoesNotExist': {
        'message': GameDoesNotExist.message,
        'status_code': GameDoesNotExist.status_code,
    },
    'FunDoesNotExist': {
        'message': FunDoesNotExist.message,
        'status_code': FunDoesNotExist.status_code,
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
    'TeamNotPartOfLeague': {
        'message': TeamNotPartOfLeague.message,
        'status_code': TeamNotPartOfLeague.status_code
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
    'BadRequestError': {
        'message': BadRequestError.message,
        'status_code': BadRequestError.status_code
    },
    'OAuthException': {
        'message': OAuthException.message,
        'status_code': OAuthException.status_code
    },
    'NotPartOfLeagueException': {
        'message': NotPartOfLeagueException.message,
        'status_code': NotPartOfLeagueException.status_code
    },
    'HaveLeagueRequestException': {
        'message': HaveLeagueRequestException.message,
        'status_code': HaveLeagueRequestException.status_code
    }
}
