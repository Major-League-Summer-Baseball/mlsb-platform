import pytest
import uuid
from api.errors import InvalidField, NonUniqueEmail
from api.model import Player


@pytest.mark.parametrize("player_date", [
    ("Player Name", "player@mlsb.ca", 'm'),
    ("Female Name", "player@mlsb.ca", 'f'),
])
@pytest.mark.usefixtures('mlsb_app')
def test_create_player(mlsb_app, player_date):
    with mlsb_app.app_context():
        player = Player(
            name=player_date[0],
            email=player_date[1],
            gender=player_date[2],
        )
        assert player.active == True


@pytest.mark.parametrize("invalid_player_date", [
    ("Invalid Email", 1, 'm'),
    ("Invalid Gender", "player@mlsb.ca", 'X'),
    (1, "invalid-name@mlsb.ca", 'm'),
])
@pytest.mark.usefixtures('mlsb_app')
def test_cannot_create_invalid_player(mlsb_app, invalid_player_date):
    with mlsb_app.app_context():
        with pytest.raises(InvalidField):
            Player(
                name=invalid_player_date[0],
                email=invalid_player_date[1],
                gender=invalid_player_date[2],
            )


@pytest.mark.parametrize("player_date", [
    ("Player Name", "player@mlsb.ca", 'm'),
    ("Female Name", "player@mlsb.ca", 'f'),
])
@pytest.mark.usefixtures('mlsb_app')
def test_update_player(mlsb_app, player_date):
    with mlsb_app.app_context():
        player = Player(name="d", email="someemail@mlsb.ca", gender="M")
        player.update(
            name=player_date[0],
            email=player_date[1],
            gender=player_date[2],
        )
        assert player.active == True


@pytest.mark.parametrize("invalid_player_date", [
    ("Invalid Email", 1, 'm'),
    ("Invalid Gender", "player@mlsb.ca", 'X'),
    (1, "invalid-name@mlsb.ca", 'm'),
])
@pytest.mark.usefixtures('mlsb_app')
def test_cannot_update_invalid_player(mlsb_app, invalid_player_date):
    with mlsb_app.app_context():
        player = Player(name="d", email="someemail@mlsb.ca", gender="M")
        with pytest.raises(InvalidField):
            player.update(
                name=invalid_player_date[0],
                email=invalid_player_date[1],
                gender=invalid_player_date[2],
            )


@pytest.mark.usefixtures('mlsb_app')
def test_json_does_include_personal_info(mlsb_app):
    with mlsb_app.app_context():
        player = Player(name="d", email="someemail@mlsb.ca", gender="M")
        json = player.json()
        assert "email" not in json, "General json should not include email"


@pytest.mark.usefixtures('mlsb_app')
def test_player_email_must_be_unique(mlsb_app, player_factory):
    with mlsb_app.app_context():
        player = player_factory(
            name="player",
            email=f"{str(uuid.uuid4())}@mlsb.ca",
            gender="M"
        )
        with pytest.raises(NonUniqueEmail):
            email_unique = Player.is_email_unique(player.email)
            assert email_unique is False
            player = Player(
                name="other player",
                email=player.email,
                gender="f"
            )


@pytest.mark.usefixtures('mlsb_app')
def test_player_email_must_be_unique_when_updating(mlsb_app, player_factory):
    with mlsb_app.app_context():
        player = player_factory(
            name="player",
            email=f"{str(uuid.uuid4())}@mlsb.ca",
            gender="M"
        )
        with pytest.raises(NonUniqueEmail):
            other_player = Player(
                name="other player",
                email=f"{str(uuid.uuid4())}@mlsb.ca",
                gender="f"
            )
            other_player.update(email=player.email)
