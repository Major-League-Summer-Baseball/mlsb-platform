import pytest
from api.tests.fixtures import random_email, random_name
from api.model import Player
from flask import url_for


NONEXISTENT=-1


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.parametrize("route", [
    "edit_player_page",
    "new_player_page",
    "players_page"
])
def test_all_routes_require_convenor_auth(mlsb_app, client, route):
    with mlsb_app.app_context():
        url = url_for(f"convenor.{route}")
        response = client.get(url, follow_redirects=True)
        assert url_for("website.loginpage").endswith(response.request.path)
        assert response.status_code == 200


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_edit_player(mlsb_app, client, player_factory, auth, convenor):
    """Test able to edit an existing player."""
    with mlsb_app.app_context():
        player = player_factory()
        auth.login(convenor.email)
        response = client.get(
            url_for("convenor.edit_player_page", player_id=player.id),
            follow_redirects=True,
        )
        assert response.status_code == 200
        data = response.data
        assert player.email in str(data)
        assert not url_for("website.loginpage").endswith(response.request.path)
        


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_edit_nonexistent_player(mlsb_app, client, auth, convenor):
    """Test handle error when  editing non-existent player."""
    with mlsb_app.app_context():
        auth.login(convenor.email)
        response = client.get(
            url_for("convenor.edit_player_page", player_id=NONEXISTENT),
            follow_redirects=True,
        )
        assert response.status_code == 200
        data = response.data
        assert "Player does not exist" in str(data)
        assert not url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_new_player(mlsb_app, client, auth, convenor):
    """Test handle error when  editing non-existent player."""
    with mlsb_app.app_context():
        auth.login(convenor.email)
        response = client.get(
            url_for("convenor.new_player_page"),
            follow_redirects=True,
        )
        assert response.status_code == 200
        data = response.data
        assert "Save" in str(data)
        assert not url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('join_league_request_factory')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_player_page(
    mlsb_app,
    client,
    team_factory,
    player_factory,
    join_league_request_factory,
    auth,
    convenor
):
    """Test players page lists league requests."""
    with mlsb_app.app_context():
        team = team_factory()
        player = player_factory()
        join_league_request_factory(
            team,
            email=player.email,
            name=player.name,
            gender=player.gender
        )
        auth.login(convenor.email)
        response = client.get(
            url_for("convenor.players_page"),
            follow_redirects=True,
        )
        assert response.status_code == 200
        data = response.data
        assert player.email in str(data)
        assert not url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_search_player(mlsb_app, client, player_factory, auth, convenor):
    """Test search players page."""
    with mlsb_app.app_context():
        player = player_factory()
        another_player = player_factory()
        auth.login(convenor.email)
        response = client.post(
            url_for("convenor.search_players"),
            follow_redirects=True,
             json={"player": player.email}
        )
        assert response.status_code == 200
        data = response.data
        assert player.email in str(data)
        assert another_player.email not in str(data)
        assert not url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('player_factory')
def test_search_player_only_convenor(mlsb_app, client, player_factory):
    """Test search players page."""
    with mlsb_app.app_context():
        player = player_factory()
        another_player = player_factory()
        response = client.post(
            url_for("convenor.search_players"),
            follow_redirects=True,
             json={"player": player.email}
        )
        assert response.status_code == 200
        assert url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_submit_valid_new_player(mlsb_app, client, auth, convenor):
    """Test able to create a player."""
    with mlsb_app.app_context():
        email = random_email()
        auth.login(convenor.email)
        response = client.post(
            url_for("convenor.submit_player"),
            follow_redirects=True,
             data={
                 "is_female": False,
                 "email": email,
                 "name": random_name("convenor-testing"),
                 "is_convenor": False
            }
        )
        assert response.status_code == 200
        assert "Error:" not in str(response.data)
        assert "Player created" in str(response.data)
        assert not url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_submit_player_only_convenor(mlsb_app, client):
    """Test able to create a player."""
    with mlsb_app.app_context():
        email = random_email()
        response = client.post(
            url_for("convenor.submit_player"),
            follow_redirects=True,
             data={
                 "is_female": False,
                 "email": email,
                 "name": random_name("convenor-testing"),
                 "is_convenor": False
            }
        )
        assert response.status_code == 200
        assert Player.is_email_unique(email) is True
        assert url_for("website.loginpage").endswith(response.request.path)



@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_submit_valid_update_player(
    mlsb_app, client, player_factory, auth, convenor
):
    """Test able to update a player."""
    with mlsb_app.app_context():
        player = player_factory()
        new_email = random_email()
        auth.login(convenor.email)
        response = client.post(
            url_for("convenor.submit_player"),
            follow_redirects=True,
             data={
                 "is_female": False,
                 "email": new_email,
                 "name": random_name("convenor-testing"),
                 "is_convenor": False,
                 "player_id": player.id
            }
        )
        assert response.status_code == 200
        assert "Error:" not in str(response.data)
        assert "Player updated" in str(response.data)
        assert Player.query.get(player.id).email == new_email
        assert not url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_submit_player_handles_errors(
    mlsb_app, client, player_factory, auth, convenor
):
    """Test handling errors when creating a player."""
    with mlsb_app.app_context():
        player = player_factory()
        auth.login(convenor.email)
        response = client.post(
            url_for("convenor.submit_player"),
            follow_redirects=True,
             data={
                 "is_female": False,
                 "email": player.email,
                 "name": random_name("convenor-testing"),
                 "is_convenor": False,
            }
        )
        assert response.status_code == 200
        assert "Error:" in str(response.data)
        assert "Player updated" not in str(response.data)
        assert not url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_submit_player_handles_making_convenor(
    mlsb_app, client, player_factory, auth, convenor
):
    """Test able to make someone a convenor."""
    with mlsb_app.app_context():
        player = player_factory()
        auth.login(convenor.email)
        response = client.post(
            url_for("convenor.submit_player"),
            follow_redirects=True,
             data={
                 "is_female": False,
                 "email": player.email,
                 "name": random_name("convenor-testing"),
                 "is_convenor": True,
                 "player_id": player.id
            }
        )
        assert response.status_code == 200
        assert "Error:" not in str(response.data)
        assert Player.query.get(player.id).is_convenor is True
        assert not url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('join_league_request_factory')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_accepting_league_request(
    mlsb_app,
    client,
    team_factory,
    join_league_request_factory,
    auth,
    convenor
):
    """Test able to accept a join league request."""
    with mlsb_app.app_context():
        team = team_factory()
        league_request = join_league_request_factory(team)
        auth.login(convenor.email)
        response = client.post(
            url_for(
                "convenor.respond_league_request",
                request_id=league_request.id,
                accept=1
            ),
            follow_redirects=True
        )
        assert response.status_code == 200
        assert "Error:" not in str(response.data)
        assert league_request.email not in str(response.data)
        assert Player.is_email_unique(league_request.email) is False
        assert not url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('join_league_request_factory')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_rejecting_league_request(
    mlsb_app,
    client,
    team_factory,
    join_league_request_factory,
    auth,
    convenor
):
    """Test able to decline a join league request."""
    with mlsb_app.app_context():
        team = team_factory()
        league_request = join_league_request_factory(team)
        auth.login(convenor.email)
        response = client.post(
            url_for(
                "convenor.respond_league_request",
                request_id=league_request.id,
                accept=0
            ),
            follow_redirects=True
        )
        assert response.status_code == 200
        assert "Error:" not in str(response.data)
        assert league_request.email not in str(response.data)
        assert Player.is_email_unique(league_request.email) is True
        assert not url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('join_league_request_factory')
def test_accepting_league_request_only_convenor(
    mlsb_app,
    client,
    team_factory,
    join_league_request_factory
):
    """Test able to accept a join league request."""
    with mlsb_app.app_context():
        team = team_factory()
        league_request = join_league_request_factory(team)
        response = client.post(
            url_for(
                "convenor.respond_league_request",
                request_id=league_request.id,
                accept=1
            ),
            follow_redirects=True
        )
        assert response.status_code == 200
        assert Player.is_email_unique(league_request.email) is True
        assert url_for("website.loginpage").endswith(response.request.path)