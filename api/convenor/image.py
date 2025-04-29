from flask import make_response, jsonify, redirect, render_template, request, session, url_for
from datetime import date
from api.authentication import require_to_be_convenor
from api.convenor import allow_images_file, convenor_blueprint
from api.model import Image
from api.extensions import DB
from api.validators import int_validator
from api.variables import PICTURES
from api.logging import LOGGER
import os
import boto3
import uuid


def get_image_bucket():
    """Returns the image bucket """
    return os.environ.get("BUCKET_NAME", "")


def using_aws_storage():
    """Returns whether current setup supports aws for storage."""
    return os.environ.get("AWS_ACCESS_KEY_ID", "") != "" and \
        os.environ.get("AWS_ENDPOINT_URL_S3", "") != "" and \
        os.environ.get("AWS_REGION", "") != "" and \
        os.environ.get("AWS_SECRET_ACCESS_KEY", "") != "" and \
        os.environ.get("BUCKET_NAME", "") != ""


def get_bucket_path(category: str, filename: str) -> str:
    """Returns the bucket path for given category"""
    year = date.today().year
    if category == 'event-date':
        return f"events/{year}/{filename}"
    elif category == 'teams':
        return f"teams/{year}/{filename}"
    return f"{category}/{filename}"


@convenor_blueprint.route("image/upload/inline", methods=['POST'])
@require_to_be_convenor
def upload_inline_image():
    if 'image' not in request.files:
        return make_response(jsonify({'message': 'No image file'}), 400)

    print(request.files)
    file = request.files['image']

    # If the user doesn't select a file
    if file.filename == '':
        return make_response(jsonify({'message': 'No image file'}), 400)

    # Check if the file is allowed
    if file and not allow_images_file(file.filename):
        return make_response(jsonify({'message': 'File ext not allowed - use png'}), 400)

    # use local static pictures folder
    print(file)
    filename = os.path.join(PICTURES, file.filename)
    file.save(filename)
    url = url_for('static', filename=f'pictures/{file.filename}')

    if using_aws_storage():
        endpoint = 'https://fly.storage.tigris.dev'
        svc = boto3.client('s3', endpoint_url=endpoint)
        bucket_path = get_bucket_path('inline', file.filename)
        svc.upload_file(filename, get_image_bucket(), bucket_path)
        url = f"https://{get_image_bucket()}.fly.storage.tigris.dev/{bucket_path}"

    image = Image(url)
    DB.session.add(image)
    DB.session.commit()
    return make_response(jsonify({'url': url}), 200)


@convenor_blueprint.route("image/upload/<category>", methods=['POST'])
@require_to_be_convenor
def upload_image(category):
    image_id = request.form.get('image_id', None)
    if 'image' not in request.files:
        session['error'] = 'No image file'
        return error_image_control(category, image_id)

    file = request.files['image']

    # If the user doesn't select a file
    if file.filename == '':
        session['error'] = 'No image file'
        return error_image_control(category, image_id)

    # Check if the file is allowed
    if file and not allow_images_file(file.filename):
        session['error'] = 'File ext not allowed - use png'
        return error_image_control(category, image_id)

    # use local static pictures folder
    filename = os.path.join(PICTURES, category, file.filename)
    file.save(filename)
    url = url_for('static', filename=f'pictures/{category}/{file.filename}')

    if using_aws_storage():
        endpoint = 'https://fly.storage.tigris.dev'
        svc = boto3.client('s3', endpoint_url=endpoint)
        bucket_path = get_bucket_path(category, file.filename)
        svc.upload_file(filename, get_image_bucket(), bucket_path)
        url = f"https://{get_image_bucket()}.fly.storage.tigris.dev/{bucket_path}"

    image = None
    if image_id is not None and image_id != 'None':
        # re use existing image and update url
        image = Image.query.get(image_id)
        image.url = url
        if image is None:
            LOGGER.warning(f'Image not found - {image_id} - creating new one')

    if image is None:
        # add an new image
        image = Image(url)
        DB.session.add(image)
    DB.session.commit()
    return redirect(
        url_for(
            'convenor.get_image_control',
            category=category,
            image_id=image.id,
        ),
    )


@convenor_blueprint.route("image/new/<category>")
def new_image_control(category: str):
    """Get a new image control."""
    return image_control(category, None)


@convenor_blueprint.route("image/<category>/<int:image_id>")
@require_to_be_convenor
def get_image_control(category: str, image_id: int = None):
    """Get image control for an existing image."""
    return image_control(category, image_id)


def error_image_control(category: str, image_id: int | None):
    """There was an error so return to the image control displaying error."""
    if image_id is None or not int_validator(image_id):
        return redirect(
            url_for(
                'convenor.new_image_control',
                category=category,
                image_id=image_id
            )
        )
    return redirect(
        url_for(
            'convenor.get_image_control',
            category=category,
            image_id=int(image_id)
        )
    )


def image_control(category: str, image_id: int | None):
    """Return an image control for given category with existing image."""
    image = None
    error = session.pop('error', None)
    id = str(uuid.uuid4())
    if image_id is not None:
        image = Image.query.get(image_id)
        if image is None:
            error = 'Image not found'
    return render_template(
        'convenor/components/image_upload.html',
        id=id,
        category=category,
        image=image,
        error=error,
        image_id=image_id,
    )
