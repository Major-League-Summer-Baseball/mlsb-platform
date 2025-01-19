from datetime import date
import pytest
from api.errors import ImageDoesNotExist, InvalidField, LeagueDoesNotExist, PlayerDoesNotExist, \
    PlayerNotOnTeam, SponsorDoesNotExist
from api.model import Team

INVALID_ENTITY = -1


@pytest.mark.usefixtures('mlsb_app')
def test_team_cannot_nonexistent_sponsor(mlsb_app):
    with mlsb_app.app_context():
        with pytest.raises(SponsorDoesNotExist):
            Team(color="some color", year=2023, sponsor_id=-1)


@pytest.mark.usefixtures('mlsb_app')
def test_team_cannot_be_nonexistent_league(mlsb_app):
    with mlsb_app.app_context():
        with pytest.raises(LeagueDoesNotExist):
            Team(color="some color", year=2023, league_id=-1)


@pytest.mark.parametrize("team_data", [
    ("Color", 2023),
])
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('image_factory')
def test_create_team(mlsb_app, team_data, image_factory):
    with mlsb_app.app_context():
        image = image_factory()
        Team(
            color=team_data[0], year=team_data[1], image_id=image.id
        )


@pytest.mark.parametrize("team_data", [
    ("Color", 2023),
])
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('image_factory')
def test_update_team(mlsb_app, team_data, image_factory):
    with mlsb_app.app_context():
        image = image_factory()
        team = Team(color="Some Color", year=2016)
        team.update(
            color=team_data[0], year=team_data[1], image_id=image.id
        )
        assert team.color == team_data[0]
        assert team.year == team_data[1]


@pytest.mark.parametrize("invalid_team_data", [
    (1, 2023),
    ("Color", "Invalid Year"),
])
@pytest.mark.usefixtures('mlsb_app')
def test_cannot_create_invalid_team(mlsb_app, invalid_team_data):
    with mlsb_app.app_context():
        with pytest.raises(InvalidField):
            Team(color=invalid_team_data[0], year=invalid_team_data[1])


@pytest.mark.parametrize("invalid_team_data", [
    (1, None),
    (None, "invalid year")
])
@pytest.mark.usefixtures('mlsb_app')
def test_cannot_update_invalid_team(mlsb_app, invalid_team_data):
    with mlsb_app.app_context():
        team = Team(color="Some Color", year=2016)
        with pytest.raises(InvalidField):
            team.update(color=invalid_team_data[0], year=invalid_team_data[1])


@pytest.mark.usefixtures('mlsb_app')
def test_cannot_update_invalid_image(mlsb_app):
    with mlsb_app.app_context():
        team = Team(color="Some Color", year=2016)
        with pytest.raises(ImageDoesNotExist):
            team.update(image_id=INVALID_ENTITY)


@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('mlsb_app')
def test_team_name_includes_sponsor(mlsb_app, sponsor_factory, team_factory):
    with mlsb_app.app_context():
        sponsor = sponsor_factory()
        team = team_factory(color="Some Color", sponsor=sponsor)
        assert sponsor.name in str(team)


@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('mlsb_app')
def test_team_name_includes_color(mlsb_app, team_factory):
    with mlsb_app.app_context():
        color = "Some Color"
        team = team_factory(color=color)
        assert color in str(team)


@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('mlsb_app')
def test_team_name_fallback(mlsb_app, team_factory):
    with mlsb_app.app_context():
        team = team_factory(color=None)
        assert str(team.id) in str(team)


@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('mlsb_app')
def test_team_add_player(mlsb_app, player_factory):
    with mlsb_app.app_context():
        player = player_factory()
        team = Team()
        assert team.insert_player(player.id) is True
        assert team.is_player_on_team(player) is True


@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('mlsb_app')
def test_team_cannot_add_player_twice(mlsb_app, player_factory):
    with mlsb_app.app_context():
        player = player_factory()
        team = Team()
        assert team.insert_player(player.id) is True
        assert team.insert_player(player.id) is False
        assert team.is_player_on_team(player) is True


@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('mlsb_app')
def test_team_add_captain(mlsb_app, player_factory):
    with mlsb_app.app_context():
        player = player_factory()
        team = Team()
        assert team.insert_player(player.id, captain=True) is True
        assert team.is_player_on_team(player) is True
        assert team.check_captain(player.name, "default")


@pytest.mark.usefixtures('mlsb_app')
def test_team_cannot_add_nonexistent_player(mlsb_app):
    with mlsb_app.app_context():
        team = Team()
        with pytest.raises(PlayerDoesNotExist):
            team.insert_player(-1, captain=True)


@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('mlsb_app')
def test_team_remove_player(mlsb_app, player_factory, team_factory):
    with mlsb_app.app_context():
        player = player_factory()
        team = team_factory(players=[player])
        team.remove_player(player.id)
        assert team.is_player_on_team(player) is False


@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('mlsb_app')
def test_team_remove_captain(mlsb_app, player_factory, team_factory):
    with mlsb_app.app_context():
        captain = player_factory()
        team = team_factory(players=[captain], captain=captain)
        team.remove_player(captain.id)
        assert team.is_player_on_team(captain) is False
        assert team.player_id is None


@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('mlsb_app')
def test_team_cannot_remove_player_twice(
    mlsb_app,
    player_factory,
    team_factory
):
    with mlsb_app.app_context():
        player = player_factory()
        team = team_factory(players=[player])
        team.remove_player(player.id)
        with pytest.raises(PlayerNotOnTeam):
            team.remove_player(player.id)


@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('mlsb_app')
def test_team_cannot_remove_nonexistent_player(mlsb_app, team_factory):
    with mlsb_app.app_context():
        team = team_factory()
        with pytest.raises(PlayerDoesNotExist):
            team.remove_player(-1)


@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('mlsb_app')
def test_determine_not_captain(mlsb_app, player_factory):
    with mlsb_app.app_context():
        player = player_factory()
        team = Team()
        assert team.insert_player(player.id, captain=True) is True
        assert team.is_player_on_team(player) is True
        assert team.check_captain("Some other name", "default") is False


@pytest.mark.usefixtures('mlsb_app')
def test_determine_not_captain_no_team_captain(mlsb_app):
    with mlsb_app.app_context():
        team = Team()
        assert team.check_captain("Some other name", "default") is False


@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('team_factory')
def test_captain_multiple_teams(mlsb_app, player_factory, team_factory):
    with mlsb_app.app_context():
        player = player_factory()
        current_team = team_factory(captain=player)
        old_team = team_factory(year=date.today().year - 1, captain=player)
        teams = Team.get_teams_captained(player.id)
        assert len(teams) == 2
        team_ids = [current_team.id, old_team.id]
        assert teams[0].id in team_ids
        assert teams[1].id in team_ids


@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('team_factory')
def test_not_captain_no_teams(mlsb_app, player_factory, team_factory):
    with mlsb_app.app_context():
        player = player_factory()
        not_captain = player_factory()
        team_factory(captain=player)
        team_factory(year=date.today().year - 1, captain=player)
        teams = Team.get_teams_captained(not_captain.id)
        assert len(teams) == 0


@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('team_factory')
def test_player_multiple_teams(mlsb_app, player_factory, team_factory):
    with mlsb_app.app_context():
        player = player_factory()
        current_team = team_factory(players=[player])
        old_team = team_factory(year=date.today().year - 1, players=[player])
        teams = Team.get_teams(player.id)
        assert len(teams) == 2
        team_ids = [current_team.id, old_team.id]
        assert teams[0].id in team_ids
        assert teams[1].id in team_ids
