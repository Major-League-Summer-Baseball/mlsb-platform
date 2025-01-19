import pytest
from flask import url_for
from api.model import Image
from api.helper import loads

test_url = 'https://i.imgur.com/lZ0Nt92.jpeg'


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_able_create_image(mlsb_app, client, auth, convenor):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        response = client.post(
            url_for("rest.images"),
            json={'url': test_url},
            follow_redirects=True
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['url'] == test_url
        assert data['image_id'] is not None
        assert Image.query.get(data['image_id']) is not None


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('image_factory')
def test_update_image(mlsb_app, client, auth, convenor, image_factory):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        image = image_factory()
        new_extension = '.png'
        response = client.put(
            url_for("rest.image", image_id=image.id),
            json={'url': test_url.replace('.jpeg', new_extension)},
            follow_redirects=True
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['url'].endswith(new_extension)


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('image_factory')
def test_delete_image(mlsb_app, client, auth, convenor, image_factory):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        image = image_factory()
        response = client.delete(
            url_for("rest.image", image_id=image.id),
            follow_redirects=True
        )
        assert response.status_code == 200
        assert Image.query.get(image.id) is None


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
def test_get_all_images(mlsb_app, client):
    with mlsb_app.app_context():
        response = client.get(
            url_for("rest.images"),
            follow_redirects=True
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert 'items' in data
        assert 'next_url' in data
        assert isinstance(data['items'], list) is True


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('image_factory')
def test_get_image(mlsb_app, client, image_factory):
    with mlsb_app.app_context():
        image = image_factory()
        response = client.get(
            url_for("rest.image", image_id=image.id),
            follow_redirects=True
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['image_id'] == image.id
        assert data['url'] == image.url
