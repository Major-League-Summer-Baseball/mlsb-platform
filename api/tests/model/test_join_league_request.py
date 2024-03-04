import pytest
from api.errors import HaveLeagueRequestException, InvalidField, \
    TeamDoesNotExist
from api.model import JoinLeagueRequest


INVALID_ENTITY = -1


@pytest.mark.parametrize("request_data", [
    ("someone@mlsb.ca", "Some Player", "M"),
    ("someone@mlsb.ca", "Some Player", "F"),
])
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
def test_create_join_league_request(
    mlsb_app,
    team_factory,
    request_data
):
    with mlsb_app.app_context():
        team = team_factory()
        JoinLeagueRequest(
            email=request_data[0],
            name=request_data[1],
            gender=request_data[2],
            team=team
        )


@pytest.mark.parametrize("invalid_request_data", [
    (1, "Some Player", "M"),
    ("someone@mlsb.ca", 1, "F"),
    ("someone@mlsb.ca", 1, "X"),
])
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
def test_cannot_create_invalid_join_league_request(
    mlsb_app,
    team_factory,
    invalid_request_data
):
    with mlsb_app.app_context():
        team = team_factory()
        with pytest.raises(InvalidField):
            JoinLeagueRequest(
                email=invalid_request_data[0],
                name=invalid_request_data[1],
                gender=invalid_request_data[2],
                team=team
            )


@pytest.mark.parametrize("request_data", [
    ("someone@mlsb.ca", "Some Player", "M")
])
@pytest.mark.usefixtures('mlsb_app')
def test_cannot_join_nonexistent_team(
    mlsb_app,
    request_data
):
    with mlsb_app.app_context():
        with pytest.raises(TeamDoesNotExist):
            JoinLeagueRequest(
                email=request_data[0],
                name=request_data[1],
                gender=request_data[2],
                team=INVALID_ENTITY
            )


@pytest.mark.parametrize("request_data", [
    ("someone@mlsb.ca", "Some Player", "m"),
])
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
def test_accepted_request_creates_player(
    mlsb_app,
    team_factory,
    request_data
):
    with mlsb_app.app_context():
        team = team_factory()
        request = JoinLeagueRequest(
            email=request_data[0],
            name=request_data[1],
            gender=request_data[2],
            team=team
        )
        player = request.accept_request()
        assert player.email == request_data[0]
        assert player.name == request_data[1]
        assert player.gender == request_data[2]


@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
def test_accepted_request_reuse_existing_player(
    mlsb_app,
    team_factory,
    player_factory
):
    with mlsb_app.app_context():
        team = team_factory()
        player = player_factory()
        request = JoinLeagueRequest(
            email=player.email,
            name=player.name,
            gender=player.gender,
            team=team
        )
        accepted_player = request.accept_request()
        assert accepted_player.id == player.id


@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
def test_create_request(
    mlsb_app,
    team_factory,
    player_factory
):
    with mlsb_app.app_context():
        team = team_factory()
        player = player_factory()
        request = JoinLeagueRequest.create_request(
            player.name,
            player.email,
            player.gender,
            team.id
        )
        assert request.team_id == team.id
        assert request.email == player.email


@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('join_league_request_factory')
def test_cannot_create_duplicate_request(
    mlsb_app,
    team_factory,
    player_factory,
    join_league_request_factory
):
    with mlsb_app.app_context():
        team = team_factory()
        player = player_factory()
        request = join_league_request_factory(
            team,
            email=player.email,
            name=player.name,
            gender=player.gender
        )

        with pytest.raises(HaveLeagueRequestException):
            JoinLeagueRequest.create_request(
                player.name,
                player.email,
                player.gender,
                team.id
            )
