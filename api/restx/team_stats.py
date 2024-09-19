from flask_restx import Resource, reqparse, fields
from flask_restx import Namespace
from api.cached_items import team_stats as pull_team_stats


parser = reqparse.RequestParser()
parser.add_argument('year', type=int)
parser.add_argument('league_id', type=int)
parser.add_argument('team_id', type=int)
parser.add_argument('division_id', type=int)

team_stats_api = Namespace(
    "team_stats",
    description="API for team stats"
)
team_stats_payload = team_stats_api.model('TeamStatsPayload', {
    'team_id': fields.Integer(
        description="The id of the team",
        required=False,
    ),
    'year': fields.Integer(
        description="The year of the team(s)",
        required=False,
    ),
    'league_id': fields.Integer(
        description="The league id of the team(s)",
        required=False,
    ),
    'division_id': fields.Integer(
        description="The division id of the team(s)",
        required=False,
    ),
})

team_stats = team_stats_api.model('TeamStats', {
    'name': fields.String(
        description="The name of the team"
    ),
    'team_id': fields.Integer(
        description="The id of the team"
    ),
    'espys': fields.Float(
        description="The total espys of the team"
    ),
    'wins': fields.Integer(
        description="The total wins by the team"
    ),
    'losses': fields.Integer(
        description="The total losses by the team"
    ),
    'ties': fields.Integer(
        description="The total ties by the team"
    ),
    'games': fields.Integer(
        description="The total games by the team"
    ),
    'runs_for': fields.Integer(
        description="The total runs score by the team"
    ),
    'runs_against': fields.Integer(
        description="The total runs scored against the team"
    ),
})


@team_stats_api.route('', endpoint='rest.team_stats')
@team_stats_api.doc()
class TeamStatsAPIX(Resource):

    @team_stats_api.marshal_list_with(team_stats)
    @team_stats_api.expect(team_stats_payload)
    def post(self):
        args = parser.parse_args()
        team_id = args.get('team_id', None)
        year = args.get('year', None)
        league_id = args.get('league_id', None)
        division_id = args.get('division_id', None)
        team = pull_team_stats(team_id, year, league_id, division_id=division_id)
        return team
