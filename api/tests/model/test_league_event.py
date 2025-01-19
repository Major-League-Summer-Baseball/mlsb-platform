import pytest
from api.errors import ImageDoesNotExist, InvalidField
from api.model import LeagueEvent

INVALID_ENTITY = -1


@pytest.mark.parametrize("league_event_data", [
    ("Some Event of the League", "The description", True),
    ("Other Event of the League", "More description", False)
])
@pytest.mark.usefixtures('mlsb_app')
def test_create_league_event(mlsb_app, league_event_data):
    with mlsb_app.app_context():
        LeagueEvent(
            name=league_event_data[0],
            description=league_event_data[1],
            active=league_event_data[2]
        )


@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('image_factory')
def test_create_league_event_with_image(mlsb_app, image_factory):
    with mlsb_app.app_context():
        image = image_factory()
        LeagueEvent(
            name='Some Event',
            description='Some Description',
            active=True,
            image_id=image.id
        )


@pytest.mark.usefixtures('mlsb_app')
def test_create_league_event_with_invalid_image(mlsb_app):
    with mlsb_app.app_context():
        with pytest.raises(ImageDoesNotExist):
            LeagueEvent(
                name='Some Event',
                description='Some Description',
                active=True,
                image_id=INVALID_ENTITY
            )


@pytest.mark.parametrize("invalid_league_event_data", [
    ("Invalid Active", "The description", 1),
    (1, "Invalid Event Name", False),
    ("Invalid Description", 1, True),
])
@pytest.mark.usefixtures('mlsb_app')
def test_cannot_create_invalid_league_event(
    mlsb_app, invalid_league_event_data
):
    with mlsb_app.app_context():
        with pytest.raises(InvalidField):
            LeagueEvent(
                name=invalid_league_event_data[0],
                description=invalid_league_event_data[1],
                active=invalid_league_event_data[2]
            )


@pytest.mark.parametrize("league_event_data", [
    ("Some Event of the League", "The description", True),
    ("Other Event of the League", "More description", False)
])
@pytest.mark.usefixtures('mlsb_app')
def test_update_league_event(mlsb_app, league_event_data):
    with mlsb_app.app_context():
        event = LeagueEvent(
            name="Some League Event",
            description="Description",
            active=True
        )
        event.update(
            name=league_event_data[0],
            description=league_event_data[1],
            active=league_event_data[2]
        )


@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('image_factory')
def test_can_update_league_event_with_valid_image(mlsb_app, image_factory):
    with mlsb_app.app_context():
        image = image_factory()
        event = LeagueEvent(
            name="Some League Event",
            description="Description",
            active=True
        )
        event.update(image_id=image.id)


@pytest.mark.parametrize("invalid_league_event_data", [
    ("Invalid Active", "The description", 1),
    (1, "Invalid Event Name", False),
    ("Invalid Description", 1, True),
])
@pytest.mark.usefixtures('mlsb_app')
def test_cannot_update_invalid_league_event(
    mlsb_app, invalid_league_event_data
):
    with mlsb_app.app_context():
        with pytest.raises(InvalidField):
            event = LeagueEvent(
                name="Some League Event",
                description="Description",
                active=True
            )
            event.update(
                name=invalid_league_event_data[0],
                description=invalid_league_event_data[1],
                active=invalid_league_event_data[2]
            )


@pytest.mark.usefixtures('mlsb_app')
def test_cannot_update_league_event_with_invalid_image(mlsb_app):
    with mlsb_app.app_context():
        with pytest.raises(ImageDoesNotExist):
            event = LeagueEvent(
                name="Some League Event",
                description="Description",
                active=True
            )
            event.update(image_id=INVALID_ENTITY)
