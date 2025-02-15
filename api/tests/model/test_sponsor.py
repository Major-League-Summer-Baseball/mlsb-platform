import pytest
from api.errors import ImageDoesNotExist, InvalidField
from api.model import Sponsor

INVALID_ENTITY = -1


@pytest.mark.parametrize("sponsor_data", [
    ("Some Sponsor", "http://good-sponsor.ca", "Some Description"),
])
@pytest.mark.usefixtures('mlsb_app')
def test_create_sponsor(mlsb_app, sponsor_data):
    with mlsb_app.app_context():
        Sponsor(
            sponsor_data[0],
            link=sponsor_data[1],
            description=sponsor_data[2]
        )


@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('image_factory')
def test_create_sponsor_with_image(mlsb_app, image_factory):
    with mlsb_app.app_context():
        image = image_factory()
        Sponsor(
            "Some sponsor",
            logo_id=image.id
        )


@pytest.mark.usefixtures('mlsb_app')
def test_cannot_create_sponsor_with_invalid_image(mlsb_app):
    with mlsb_app.app_context():
        with pytest.raises(ImageDoesNotExist):
            Sponsor("Some sponsor", logo_id=INVALID_ENTITY)


@pytest.mark.parametrize("invalid_sponsor_data", [
    (1, "http://bad-sponsor.ca", "Sponsor name cannot be a number"),
    ("Sponsor Description cannot be a number", "http://bad-sponsor.ca", 1),
    (1, "http://bad-sponsor.ca", "Sponsor name cannot be a number"),
    ("Sponsor link cannot be a number", 1, "Some Description"),
])
@pytest.mark.usefixtures('mlsb_app')
def test_cannot_create_invalid_sponsor(mlsb_app, invalid_sponsor_data):
    with mlsb_app.app_context():
        with pytest.raises(InvalidField):
            Sponsor(
                invalid_sponsor_data[0],
                link=invalid_sponsor_data[1],
                description=invalid_sponsor_data[2]
            )


@pytest.mark.parametrize("sponsor_data", [
    ("Sponsor Updated", "http://good-sponsor.ca", "Some Description"),
])
@pytest.mark.usefixtures('mlsb_app')
def test_update_sponsor(mlsb_app, sponsor_data):
    with mlsb_app.app_context():
        sponsor = Sponsor("Some Sponsor")
        sponsor.update(
            name=sponsor_data[0],
            link=sponsor_data[1],
            description=sponsor_data[2]
        )


@pytest.mark.parametrize("invalid_sponsor_data", [
    (1, "http://bad-sponsor.ca", "Sponsor name cannot be a number"),
    ("Sponsor Description cannot be a number", "http://bad-sponsor.ca", 1),
    (1, "http://bad-sponsor.ca", "Sponsor name cannot be a number"),
    ("Sponsor link cannot be a number", 1, "Some Description"),
])
@pytest.mark.usefixtures('mlsb_app')
def test_cannot_update_invalid_sponsor(
    mlsb_app,
    invalid_sponsor_data
):
    with mlsb_app.app_context():
        sponsor = Sponsor("Some Sponsor")
        with pytest.raises(InvalidField):
            sponsor.update(
                name=invalid_sponsor_data[0],
                link=invalid_sponsor_data[1],
                description=invalid_sponsor_data[2]
            )
