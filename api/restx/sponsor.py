from flask_restx import Resource, reqparse, Namespace, fields
from flask import request, url_for
from .models import get_pagination
from api.extensions import DB
from api.model import Sponsor
from api.authentication import requires_admin
from api.errors import SponsorDoesNotExist
from api.variables import PAGE_SIZE
from api.routes import Routes
from api.helper import pagination_response
from api.cached_items import handle_table_change
from api.tables import Tables

parser = reqparse.RequestParser()
parser.add_argument('sponsor_name', type=str)
parser.add_argument('link', type=str)
parser.add_argument('description', type=str)
parser.add_argument('active', type=int)
post_parser = reqparse.RequestParser()
post_parser.add_argument('sponsor_name', type=str, required=True)
post_parser.add_argument('link', type=str)
post_parser.add_argument('description', type=str)
post_parser.add_argument('active', type=int)

sponsor_api = Namespace(
    "sponsor",
    description="API for all the League's Sponsors"
)
sponsor_payload = sponsor_api.model('SponsorPayload', {
    'sponsor_name': fields.String(
        description="The name of the sponsor",
    ),
    'link': fields.String(
        description="A link to the sponsor social media or website",
    ),
    'description': fields.String(
        description="A description of the sponsor",
    ),
    'active': fields.Boolean(
        description="Whether the sponsor is actively sponsoring the league",
        default=True
    )
})
sponsor = sponsor_api.inherit("Sponsor", sponsor_payload, {
    'sponsor_id': fields.Integer(
        description="The id of the sponsor"
    )
})
pagination = get_pagination(sponsor_api)
sponsor_pagination = sponsor_api.inherit("SponsorPagination", pagination, {
    'items': fields.List(fields.Nested(sponsor))
})


@sponsor_api.route("/<int:sponsor_id>", endpoint="rest.sponsor")
@sponsor_api.doc(params={"sponsor_id": "The id of the sponsor"})
class SponsorAPI(Resource):

    @sponsor_api.marshal_with(sponsor)
    def get(self, sponsor_id):
        # expose a single Sponsor
        entry = Sponsor.query.get(sponsor_id)
        if entry is None:
            raise SponsorDoesNotExist(payload={'details': sponsor_id})
        return entry.json()

    @requires_admin
    @sponsor_api.doc(responses={403: 'Not Authorized', 200: 'Deleted'})
    @sponsor_api.marshal_with(sponsor)
    def delete(self, sponsor_id):
        # delete a single user
        sponsor = Sponsor.query.get(sponsor_id)
        if sponsor is None:
            raise SponsorDoesNotExist(payload={'details': sponsor_id})
        DB.session.delete(sponsor)
        DB.session.commit()
        handle_table_change(Tables.SPONSOR, item=sponsor.json())
        return sponsor.json()

    @requires_admin
    @sponsor_api.doc(responses={403: 'Not Authorized', 200: 'Updated'})
    @sponsor_api.expect(sponsor_payload)
    @sponsor_api.marshal_with(sponsor)
    def put(self, sponsor_id):
        # update a single user
        sponsor = Sponsor.query.get(sponsor_id)
        if sponsor is None:
            raise SponsorDoesNotExist(payload={'details': sponsor_id})

        args = parser.parse_args()
        name = args.get('sponsor_name', None)
        link = args.get('link', None)
        is_active = args.get("active", True)
        active = is_active == 1 if isinstance(is_active, int) else is_active
        description = args.get('description', None)

        sponsor.update(
            name=name, link=link, description=description, active=active
        )
        DB.session.commit()
        handle_table_change(Tables.SPONSOR, item=sponsor.json())
        return sponsor.json()

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}


@sponsor_api.route("", endpoint="rest.sponsors")
class SponsorListAPI(Resource):

    @sponsor_api.marshal_with(sponsor_pagination)
    def get(self):
        # return a pagination of Sponsors
        page = request.args.get('page', 1, type=int)
        pagination = Sponsor.query.paginate(page, PAGE_SIZE, False)
        result = pagination_response(pagination, url_for('rest.sponsors'))
        return result

    @requires_admin
    @sponsor_api.doc(responses={403: 'Not Authorized', 200: 'Created'})
    @sponsor_api.expect(sponsor_payload)
    @sponsor_api.marshal_with(sponsor)
    def post(self):
        # create a new user
        args = post_parser.parse_args()

        sponsor_name = args.get('sponsor_name', None)
        link = args.get('link', None)
        is_active = args.get("active", True)
        active = is_active == 1 if isinstance(is_active, int) else is_active
        description = args.get('description', None)

        sponsor = Sponsor(
            sponsor_name, link=link, description=description, active=active
        )
        DB.session.add(sponsor)
        DB.session.commit()
        handle_table_change(Tables.SPONSOR, item=sponsor.json())
        return sponsor.json()

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}
