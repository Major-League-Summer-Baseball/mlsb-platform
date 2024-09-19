"""Any models use across routes"""
from flask_restx import fields, Namespace, Model

model_api = Namespace(
    "models",
    description="Namespace for shared models"
)

team_payload = model_api.model('TeamPayload', {
    'color': fields.String(
        description="The color of the team"
    ),
    'sponsor_id': fields.Integer(
        description="The id of the teams's sponsor"
    ),
    'league_id': fields.Integer(
        description="The id of the league the team belongs to"
    ),
    'year': fields.Integer(
        description="The year the team played"
    )
})

player_payload = model_api.model('PlayerPayload', {
    'player_name': fields.String(
        description="The name of the player",
    ),
    'gender': fields.String(
        description="The gender of the player",
        default="M",
        enum=['F', 'M', 'T']
    ),
    'active': fields.Boolean(
        description="Whether the player is active in the league or not",
        default=True
    ),
    'email': fields.String(
        description="The email of the player"
    )
})

player = model_api.inherit('Player', player_payload, {
    'player_id': fields.Integer(
        description="The id of the player",
    ),
})

team = model_api.inherit('Team', team_payload, {
    'team_id': fields.Integer(
        description="The id of the team"
    ),
    'team_name': fields.String(
        description="The name of the team"
    ),
    'espys': fields.Integer(
        description="The total espys points awarded to the team"
    ),
    'captain': fields.Nested(
        player,
        description="The captain of the team"
    )
})


def get_pagination(api: Namespace) -> Model:
    """Add the pagination model to the given flask-rest API"""
    return api.model("Pagination", {
        'has_next': fields.Boolean(
            default=False,
            description="Whether more pagination exists"
        ),
        'has_prev': fields.Boolean(
            default=False,
            description="Whether previous pagination exists"
        ),
        'next_url': fields.Url(
            description="Url for the next pagination of items"
        ),
        'prev_url': fields.Url(
            description=("Url for the previous pagination of itmes")
        ),
        'total': fields.Integer(
            description="The total number of items"
        ),
        'pages': fields.Integer(
            description="The total number of paginations"
        ),
    })
