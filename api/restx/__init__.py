from .fun import fun_api
from .player import player_api
from .sponsor import sponsor_api
from .espys import espys_api
from .team import team_api
from .division import division_api
from .league import league_api
from .game import game_api
from .bat import bat_api
from .league_event import league_event_api
from .league_event_date import league_event_date_api
from flask_restx import Api
apiX = Api(
    version="0.1",
    title="MLSB V2 API",
    doc="/rest/swagger",
    prefix="/rest",
    endpoint="restx",
    authorizations={
        "admin": {
            "type": "basic",
        }
    },
)
apiX.add_namespace(fun_api)
apiX.add_namespace(player_api)
apiX.add_namespace(sponsor_api)
apiX.add_namespace(espys_api)
apiX.add_namespace(division_api)
apiX.add_namespace(team_api)
apiX.add_namespace(league_api)
apiX.add_namespace(game_api)
apiX.add_namespace(bat_api)
apiX.add_namespace(league_event_api)
apiX.add_namespace(league_event_date_api)
