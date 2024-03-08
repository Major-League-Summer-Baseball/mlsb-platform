"""Test all the captain functionality of the team page."""
import pytest
import uuid
from datetime import date
from flask import url_for
from api.helper import loads
from api.model import JoinLeagueRequest, Team, Player


THIS_YEAR = date.today().year
INVALID_ENTITY = 100000000


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('auth')
def test_team_page_captain(
    mlsb_app,
    client,
    team_factory,
    player_factory,
    auth
):
    with mlsb_app.app_context():
        teammate = player_factory()
        player = player_factory()
        team = team_factory(players=[teammate], captain=player)
        auth.login(player.email)
        url = url_for(
            "website.team_page",
            year=THIS_YEAR,
            team_id=team.id
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200
        data = response.data.decode("utf-8")

        # see controls for adding players
        assert "Add Players" in data
        assert 'id="rosterManagement"' in data


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_player_page(mlsb_app, client):
    with mlsb_app.app_context():
        player = Player.query.first()
        url = url_for(
            "website.player_page",
            year=THIS_YEAR,
            player_id=player.id
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_nonexistent_player_page(mlsb_app, client):
    with mlsb_app.app_context():
        url = url_for(
            "website.player_page",
            year=THIS_YEAR,
            player_id=INVALID_ENTITY
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200
        data = response.data.decode("utf-8")
        assert "<title>Player not found</title>" in data


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('auth')
def test_request_to_join_team(
    mlsb_app,
    client,
    team_factory,
    player_factory,
    auth
):
    with mlsb_app.app_context():
        new_player = player_factory()
        team = team_factory()
        auth.login(new_player.email)
        url = url_for(
            "website.request_to_join_team",
            team_id=team.id,
            year=THIS_YEAR
        )
        response = client.post(url, follow_redirects=True)
        assert response.status_code == 200
        data = str(response.data)
        assert "Submitted request to join" in data


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('team_factory')
def test_request_to_join_team_not_signed_in(
    mlsb_app,
    client,
    team_factory,
    auth
):
    with mlsb_app.app_context():
        auth.logout()
        team = team_factory()
        url = url_for(
            "website.request_to_join_team",
            team_id=team.id,
            year=THIS_YEAR
        )
        response = client.post(url)
        # should be redirect to login page
        assert response.status_code == 302
        assert url_for("website.loginpage").endswith(response.location)


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('auth')
def test_request_to_join_nonexistent_team(
    mlsb_app,
    client,
    player_factory,
    auth
):
    with mlsb_app.app_context():
        new_player = player_factory()
        auth.login(new_player.email)
        url = url_for(
            "website.request_to_join_team",
            team_id=INVALID_ENTITY,
            year=THIS_YEAR
        )
        response = client.post(url, follow_redirects=True)
        assert response.status_code == 404


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('auth')
def test_team_remove_player(
    mlsb_app,
    client,
    player_factory,
    team_factory,
    auth
):
    with mlsb_app.app_context():
        captain = player_factory()
        teammate = player_factory()
        team = team_factory(players=[teammate], captain=captain)
        auth.login(captain.email)
        url = url_for(
            "website.team_remove_player",
            team_id=team.id,
            player_id=teammate.id,
            year=THIS_YEAR
        )
        response = client.post(url, follow_redirects=True)
        assert response.status_code == 200
        assert teammate.name not in str(response.data)


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('auth')
def test_nonexistent_team_remove_player(
    mlsb_app,
    client,
    player_factory,
    team_factory,
    auth
):
    with mlsb_app.app_context():
        captain = player_factory()
        teammate = player_factory()
        team_factory(players=[teammate], captain=captain)
        auth.login(captain.email)
        url = url_for(
            "website.team_remove_player",
            team_id=INVALID_ENTITY,
            player_id=teammate.id,
            year=THIS_YEAR
        )
        response = client.post(url, follow_redirects=True)
        assert response.status_code == 404


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('auth')
def test_team_remove_nonexistent_player(
    mlsb_app,
    client,
    player_factory,
    team_factory,
    auth
):
    with mlsb_app.app_context():
        captain = player_factory()
        team = team_factory(captain=captain)
        auth.login(captain.email)
        url = url_for(
            "website.team_remove_player",
            team_id=team.id,
            player_id=INVALID_ENTITY,
            year=THIS_YEAR
        )
        response = client.post(url, follow_redirects=True)
        assert response.status_code == 404


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('auth')
def test_team_add_player(
    mlsb_app,
    client,
    player_factory,
    team_factory,
    auth
):
    with mlsb_app.app_context():
        captain = player_factory()
        new_player = player_factory()
        team = team_factory(captain=captain)
        auth.login(captain.email)
        url = url_for(
            "website.team_add_player_form",
            team_id=team.id,
            year=THIS_YEAR
        )
        response = client.post(
            url,
            data={'player_id': new_player.id},
            follow_redirects=True
        )
        assert response.status_code == 200
        assert new_player.name in str(response.data)


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('auth')
def test_team_add_player_already_on_team(
    mlsb_app,
    client,
    player_factory,
    team_factory,
    auth
):
    with mlsb_app.app_context():
        captain = player_factory()
        teammate = player_factory()
        team = team_factory(players=[teammate], captain=captain)
        auth.login(captain.email)
        url = url_for(
            "website.team_add_player_form",
            team_id=team.id,
            year=THIS_YEAR
        )
        response = client.post(
            url, follow_redirects=True, data={'player_id': teammate.id}
        )
        assert response.status_code == 400


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('auth')
def test_team_add_nonexistent_player(
    mlsb_app,
    client,
    player_factory,
    team_factory,
    auth
):
    with mlsb_app.app_context():
        captain = player_factory()
        team = team_factory(captain=captain)
        auth.login(captain.email)
        url = url_for(
            "website.team_add_player_form",
            team_id=team.id,
            year=THIS_YEAR
        )
        response = client.post(
            url, follow_redirects=True, data={'player_id': INVALID_ENTITY}
        )
        assert response.status_code == 404


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('auth')
def test_nonexistent_team_add_player(
    mlsb_app,
    client,
    player_factory,
    team_factory,
    auth
):
    with mlsb_app.app_context():
        captain = player_factory()
        new_player = player_factory()
        team_factory(captain=captain)
        auth.login(captain.email)
        url = url_for(
            "website.team_add_player_form",
            team_id=INVALID_ENTITY,
            player_id=new_player.id,
            year=THIS_YEAR
        )
        response = client.post(
            url, follow_redirects=True, data={'player_id': new_player.id}
        )
        assert response.status_code == 404
        data = loads(response.data)
        assert data['details'] == INVALID_ENTITY


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('join_league_request_factory')
@pytest.mark.usefixtures('auth')
def test_captain_accept_team_request(
    mlsb_app,
    client,
    player_factory,
    team_factory,
    join_league_request_factory,
    auth
):
    with mlsb_app.app_context():
        captain = player_factory()
        team = team_factory(captain=captain)
        request = join_league_request_factory(team)
        auth.login(captain.email)
        url = url_for(
            "website.captain_respond_league_request_form",
            team_id=team.id,
            year=THIS_YEAR
        )
        response = client.post(
            url,
            data={
                "accept": True,
                "request_id": request.id
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        assert request.name in str(response.data)


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('join_league_request_factory')
@pytest.mark.usefixtures('auth')
def test_captain_reject_team_request(
    mlsb_app,
    client,
    player_factory,
    team_factory,
    join_league_request_factory,
    auth
):
    with mlsb_app.app_context():
        captain = player_factory()
        team = team_factory(captain=captain)
        request = join_league_request_factory(team)
        auth.login(captain.email)
        url = url_for(
            "website.captain_respond_league_request_form",
            team_id=team.id,
            year=THIS_YEAR
        )
        response = client.post(
            url,
            data={
                "accept": False,
                "request_id": request.id
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        assert request.name not in str(response.data)


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('join_league_request_factory')
@pytest.mark.usefixtures('auth')
def test_not_captain_cannot_respond_team_request(
    mlsb_app,
    client,
    player_factory,
    team_factory,
    join_league_request_factory,
    auth
):
    with mlsb_app.app_context():
        player = player_factory()
        team = team_factory(players=[player])
        request = join_league_request_factory(team)
        auth.login(player.email)
        url = url_for(
            "website.captain_respond_league_request_form",
            team_id=team.id,
            year=THIS_YEAR
        )
        response = client.post(
            url,
            data={
                "accept": False,
                "request_id": request.id
            },
            follow_redirects=True
        )
        assert response.status_code == 401


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('auth')
def test_captain_cannot_respond_nonexistent_team_request(
    mlsb_app,
    client,
    player_factory,
    team_factory,
    auth
):
    with mlsb_app.app_context():
        captain = player_factory()
        team = team_factory(captain=captain)
        auth.login(captain.email)
        url = url_for(
            "website.captain_respond_league_request_form",
            team_id=team.id,
            year=THIS_YEAR
        )
        response = client.post(
            url,
            data={
                "accept": True,
                "request_id": INVALID_ENTITY
            },
            follow_redirects=True
        )
        assert response.status_code == 404


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('join_league_request_factory')
@pytest.mark.usefixtures('auth')
def test_captain_cannot_rerespond_team_request(
    mlsb_app,
    client,
    player_factory,
    team_factory,
    join_league_request_factory,
    auth
):
    with mlsb_app.app_context():
        captain = player_factory()
        team = team_factory(captain=captain)
        request = join_league_request_factory(team)
        auth.login(captain.email)
        url = url_for(
            "website.captain_respond_league_request_form",
            team_id=team.id,
            year=THIS_YEAR
        )
        response = client.post(
            url,
            data={"accept": True, "request_id": request.id},
            follow_redirects=True
        )
        assert response.status_code == 200

        response = client.post(
            url,
            json={"accept": True, "request_id": request.id},
            follow_redirects=True
        )
        assert response.status_code == 404
