from .fun import fun_api
from .models import model_api
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
from .schedule import schedule_api
from .team_stats import team_stats_api
from flask_restx import Api
apiX = Api(
    version="0.1",
    title="MLSB V2 API",
    contact="dallas.fraser.waterloo@gmail.com",
    doc="/rest/swagger",
    prefix="/rest",
    endpoint="restx",
    authorizations={
        "google": {
            "type": "oauth2",
            "flow": "implicit",
            "authorizationUrl": "/login/google/authorized",
        },
        "github": {
            "type": "oauth2",
            "flow": "implicit",
            "authorizationUrl": "/login/github/authorized",
        },
        "azure": {
            "type": "oauth2",
            "flow": "implicit",
            "authorizationUrl": "/login/azure/authorized",
        },
        "facebook": {
            "type": "oauth2",
            "flow": "implicit",
            "authorizationUrl": "/login/facebook/authorized",
        },
    },
    security=["google", "github", "azure", "facebook"],
)
apiX.add_namespace(model_api)
apiX.add_namespace(bat_api)
apiX.add_namespace(division_api)
apiX.add_namespace(espys_api)
apiX.add_namespace(fun_api)
apiX.add_namespace(game_api)
apiX.add_namespace(league_api)
apiX.add_namespace(league_event_api)
apiX.add_namespace(league_event_date_api)
apiX.add_namespace(player_api)
apiX.add_namespace(schedule_api)
apiX.add_namespace(sponsor_api)
apiX.add_namespace(team_api)
apiX.add_namespace(team_stats_api)
