import pytest
from api.errors import InvalidField
from api.model import LeagueEvent


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
