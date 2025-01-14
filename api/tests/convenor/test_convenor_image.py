import pytest
import os
from io import BytesIO
from api.model import Image
from flask import url_for
from api.variables import PICTURES

TEST_IMAGE = 'test.png'
TEST_CATEGORY = 'sponsors'


@pytest.fixture
def cleanup_test_image():
    """Clneaup the test image if one was potentially uploaded."""
    yield
    try:
        os.remove(os.path.join(PICTURES, TEST_CATEGORY, TEST_IMAGE))
    except OSError:
        pass


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_new_image_control(
    mlsb_app, client, auth, convenor
):
    """Test able to get control for new image."""
    with mlsb_app.app_context():
        auth.login(convenor.email)
        response = client.get(
            url_for("convenor.new_image_control", category=TEST_CATEGORY),
            follow_redirects=True,
        )
        assert response.status_code == 200
        data = response.data
        assert 'sponsors ' in str(data)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('image_factory')
def test_existing_image_control(
    mlsb_app, client, auth, convenor, image_factory
):
    """Test able to get control for an existing image."""
    with mlsb_app.app_context():
        image = image_factory()
        auth.login(convenor.email)
        response = client.get(
            url_for(
                "convenor.get_image_control",
                category=TEST_CATEGORY,
                image_id=image.id
            ),
            follow_redirects=True,
        )
        assert response.status_code == 200
        data = response.data
        assert TEST_CATEGORY in str(data)
        assert image.url in str(data)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('cleanup_test_image')
def test_upload_new_image(
    mlsb_app, client, auth, convenor
):
    """Test able to upload a new image."""
    with mlsb_app.app_context():
        auth.login(convenor.email)
        data = dict(
            image=(BytesIO(b'test'), TEST_IMAGE),
        )
        response = client.post(
            url_for(
                "convenor.upload_image",
                category=TEST_CATEGORY,
            ),
            content_type='multipart/form-data',
            data=data,
            follow_redirects=True,
        )
        assert response.status_code == 200
        data = response.data
        added_image = Image.query.order_by(Image.id.desc()).first()
        assert TEST_IMAGE in added_image.url
        assert TEST_CATEGORY in str(data)
        assert added_image.url in str(data)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('cleanup_test_image')
@pytest.mark.usefixtures('image_factory')
def test_upload_new_picture_for_existing_image(
    mlsb_app, client, auth, convenor, image_factory
):
    """Test able to upload a new picture for an image."""
    with mlsb_app.app_context():
        image = image_factory()
        current_url = image.url
        auth.login(convenor.email)
        data = dict(
            image=(BytesIO(b'test'), TEST_IMAGE),
            image_id=image.id
        )
        response = client.post(
            url_for(
                "convenor.upload_image",
                category=TEST_CATEGORY,
            ),
            content_type='multipart/form-data',
            data=data,
            follow_redirects=True,
        )
        assert response.status_code == 200
        data = response.data
        updated_image = Image.query.get(image.id)
        assert updated_image.id == image.id
        assert updated_image.url != current_url
        assert TEST_IMAGE in updated_image.url
        assert TEST_CATEGORY in str(data)
        assert updated_image.url in str(data)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_cannot_use_any_image_extension(
    mlsb_app, client, auth, convenor
):
    """Test able to upload a new image."""
    with mlsb_app.app_context():
        auth.login(convenor.email)
        data = dict(
            image=(BytesIO(b'test'), 'test.invalid'),
        )
        response = client.post(
            url_for(
                "convenor.upload_image",
                category=TEST_CATEGORY,
            ),
            content_type='multipart/form-data',
            data=data,
            follow_redirects=True,
        )
        assert response.status_code == 200
        data = response.data
        assert 'File ext not allowed - use png' in str(data)
