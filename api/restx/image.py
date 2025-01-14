
from flask_restx import Resource, reqparse, Namespace, fields
from flask import request, url_for

from api.models.image import Image
from .models import get_pagination
from api.extensions import DB
from api.authentication import require_to_be_convenor
from api.errors import ImageDoesNotExist
from api.variables import PAGE_SIZE
from api.helper import pagination_response
from api.cached_items import handle_table_change
from api.tables import Tables

parser = reqparse.RequestParser()
parser.add_argument('url', type=str, required=True)
post_parser = reqparse.RequestParser()
post_parser.add_argument('url', type=str, required=True)

image_api = Namespace("image", description="API for storing external images")
image_payload = image_api.model('ImagePayload', {
    'url': fields.String(description='The url to the image')
})
image = image_api.inherit("Image", image_payload, {
    'image_id': fields.Integer(description="The id of the image")
})

pagination = get_pagination(image_api)
image_pagination = image_api.inherit("ImagePagination", pagination, {
    'items': fields.List(fields.Nested(image))
})


@image_api.route("/<int:image_id>", endpoint="rest.image")
@image_api.doc(params={"image_id": "The id of the image"})
class SponsorAPI(Resource):
    @image_api.doc(security=[])
    @image_api.marshal_with(image)
    def get(self, image_id):
        # expose a single image
        entry = Image.query.get(image_id)
        if entry is None:
            raise ImageDoesNotExist(payload={'details': image_id})
        return entry.json()

    @require_to_be_convenor
    @image_api.doc(responses={403: 'Not Authorized', 200: 'Deleted'})
    @image_api.marshal_with(image)
    def delete(self, image_id):
        # delete a single image
        image = Image.query.get(image_id)
        if image is None:
            raise ImageDoesNotExist(payload={'details': image_id})
        DB.session.delete(image)
        DB.session.commit()
        handle_table_change(Tables.IMAGE, item=image.json())
        return image.json()

    @require_to_be_convenor
    @image_api.doc(responses={403: 'Not Authorized', 200: 'Updated'})
    @image_api.expect(image_payload)
    @image_api.marshal_with(image)
    def put(self, image_id):
        # update a single image
        image = Image.query.get(image_id)
        if image is None:
            raise ImageDoesNotExist(payload={'details': image_id})

        args = parser.parse_args()
        url = args.get('url')

        image.url = url
        DB.session.commit()
        handle_table_change(Tables.IMAGE, item=image.json())
        return image.json()

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}


@image_api.route("", endpoint="rest.images")
class ImageListAPI(Resource):
    @image_api.doc(security=[])
    @image_api.marshal_with(image_pagination)
    def get(self):
        # return a pagination of Images
        page = request.args.get('page', 1, type=int)
        pagination = Image.query.paginate(
            page=page, per_page=PAGE_SIZE, error_out=False
        )
        result = pagination_response(pagination, url_for('rest.images'))
        return result

    @require_to_be_convenor
    @image_api.doc(responses={403: 'Not Authorized', 200: 'Created'})
    @image_api.expect(image_payload)
    @image_api.marshal_with(image)
    def post(self):
        # create a new image
        args = post_parser.parse_args()

        url = args.get('url', None)

        image = Image(url)
        DB.session.add(image)
        DB.session.commit()
        handle_table_change(Tables.IMAGE, item=image.json())
        return image.json()

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}
