import pytest
import uuid
from datetime import date
from api.errors import InvalidField, NonUniqueEmail
from api.model import Player
from api.variables import UNASSIGNED_EMAIL


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
@pytest.mark.usefixtures('player_factory')
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
@pytest.mark.usefixtures('player_factory')
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


@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('player_factory')
def test_captain_multiple_teams(mlsb_app, player_factory, team_factory):
    with mlsb_app.app_context():
        player = player_factory()
        current_team = team_factory(captain=player)
        old_team = team_factory(year=date.today().year - 1, captain=player)
        teams = Player.get_teams_captained(player.id)
        assert len(teams) == 2
        team_ids = [current_team.id, old_team.id]
        assert teams[0].id in team_ids
        assert teams[1].id in team_ids


@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('player_factory')
def test_not_captain_no_teams(mlsb_app, player_factory, team_factory):
    with mlsb_app.app_context():
        player = player_factory()
        not_captain = player_factory()
        team_factory(captain=player)
        team_factory(year=date.today().year - 1, captain=player)
        teams = Player.get_teams_captained(not_captain.id)
        assert len(teams) == 0


@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('player_factory')
def test_search_player(mlsb_app, player_factory):
    with mlsb_app.app_context():
        search_phrase = "some-secret-phrase"
        player_name = player_factory(
            name=search_phrase.upper() + str(uuid.uuid4())
        )
        player_email = player_factory(
            email=search_phrase.upper() + str(uuid.uuid4()) + "@mlsb.ca"
        )
        not_matched = player_factory(
            name="not", email=f"not{str(uuid.uuid4())}@mlsb.ca"
        )
        players = Player.search_player(search_phrase)
        assert len(players) >= 2
        player_ids = [player.id for player in players]
        assert player_name.id in player_ids
        assert player_email.id in player_ids
        assert not_matched.id not in player_ids


@pytest.mark.usefixtures('mlsb_app')
def test_search_player_does_not_include_unassigned(mlsb_app):
    with mlsb_app.app_context():
        search_phrase = UNASSIGNED_EMAIL
        players = Player.search_player(search_phrase)
        assert len(players) == 0


@pytest.mark.usefixtures('mlsb_app')
def test_get_unassigned_player(mlsb_app):
    with mlsb_app.app_context():
        player = Player.get_unassigned_player()
        assert player is not None
        assert player.email == Player.normalize_email(UNASSIGNED_EMAIL)
