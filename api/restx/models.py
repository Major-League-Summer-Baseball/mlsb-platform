"""Any models use across routes"""
from flask_restx import fields, Namespace, Model


def get_pagination(api: Namespace) -> Model:
    """Add the pagination model to the given flask-restAPI"""
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
