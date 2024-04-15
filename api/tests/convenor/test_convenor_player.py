import pytest
from datetime import datetime
from flask import url_for


NONEXISTENT=-1

@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('player_factory')
def test_edit_player(mlsb_app, client, player_factory):
    """Test able to edit an existing player."""
    with mlsb_app.app_context():
        player = player_factory()
        response = client.get(
            url_for("convenor.edit_player_page", player_id=player.id),
            follow_redirects=True,
        )
        assert response.status_code == 200
        data = response.data
        assert player.email in str(data)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_edit_nonexistent_player(mlsb_app, client):
    """Test handle error when  editing non-existent player."""
    with mlsb_app.app_context():
        response = client.get(
            url_for("convenor.edit_player_page", player_id=NONEXISTENT),
            follow_redirects=True,
        )
        assert response.status_code == 200
        data = response.data
        assert "Player does not exist" in str(data)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_new_player(mlsb_app, client):
    """Test handle error when  editing non-existent player."""
    with mlsb_app.app_context():
        response = client.get(
            url_for("convenor.new_player_page"),
            follow_redirects=True,
        )
        assert response.status_code == 200
        data = response.data
        assert "Save" in str(data)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('join_league_request_factory')
def test_player_page(
    mlsb_app, client, team_factory, player_factory, join_league_request_factory
):
    """Test players page that list league requests."""
    with mlsb_app.app_context():
        team = team_factory()
        player = player_factory()
        join_league_request_factory(
            team,
            email=player.email,
            name=player.name,
            gender=player.gender
        )
        response = client.get(
            url_for("convenor.players_page"),
            follow_redirects=True,
        )
        assert response.status_code == 200
        data = response.data
        assert player.email in str(data)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('player_factory')
def test_search_player(mlsb_app, client, player_factory):
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
        data = response.data
        assert player.email in str(data)

