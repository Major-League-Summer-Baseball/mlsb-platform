import pytest
from api.model import Image


@pytest.mark.usefixtures('mlsb_app')
def test_create_image(mlsb_app):
    with mlsb_app.app_context():
        Image('https://i.imgur.com/lZ0Nt92.jpeg')
