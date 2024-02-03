import pytest
from flask import url_for
from api.tests.fixtures import random_email, random_name
from api.model import Player
from api.helper import loads


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('admin_header')
def test_able_create_player(mlsb_app, client, admin_header):
    with mlsb_app.app_context():
        name = random_name("Rest")
        email = random_email()
        male = "M"
        response = client.post(
            url_for("rest.players"),
            json={
                "player_name": name,
                "email": email,
                "active": True,
                "gender": male
            },
            follow_redirects=True,
            headers=admin_header
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['player_name'] == name
        assert data['email'] == email
        assert data['gender'] == Player.normalize_gender(male)
        assert data['active'] == True
        assert isinstance(data['player_id'], int) is True
        assert Player.does_player_exist(data['player_id']) is True


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('admin_header')
def test_required_fields_of_player(mlsb_app, client, admin_header):
    with mlsb_app.app_context():
        name = random_name("Rest")
        email = random_email()
        male = "M"
        response = client.post(
            url_for("rest.players"),
            json={
                "email": email,
                "active": True,
                "gender": male
            },
            follow_redirects=True,
            headers=admin_header
        )
        assert response.status_code == 400
        response = client.post(
            url_for("rest.players"),
            json={
                "player_name": name,
                "active": True,
                "gender": male
            },
            follow_redirects=True,
            headers=admin_header
        )
        assert response.status_code == 400


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('admin_header')
@pytest.mark.usefixtures('player_factory')
def test_update_player(mlsb_app, client, admin_header, player_factory):
    with mlsb_app.app_context():
        player = player_factory()
        new_email = random_email()
        response = client.put(
            url_for("rest.player", player_id=player.id),
            json={
                "email": new_email
            },
            follow_redirects=True,
            headers=admin_header
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['email'] == new_email
        assert data['player_id'] == player.id
        assert Player.find_by_email(new_email) is not None


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('admin_header')
@pytest.mark.usefixtures('player_factory')
def test_delete_player(mlsb_app, client, admin_header, player_factory):
    with mlsb_app.app_context():
        player = player_factory()
        response = client.delete(
            url_for("rest.player", player_id=player.id),
            follow_redirects=True,
            headers=admin_header
        )
        assert response.status_code == 200
        assert Player.does_player_exist(player.id) is False


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('admin_header')
def test_get_all_player(mlsb_app, client, admin_header):
    with mlsb_app.app_context():
        response = client.get(
            url_for("rest.players"),
            follow_redirects=True,
            headers=admin_header
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert 'items' in data
        assert 'next_url' in data
        assert isinstance(data['items'], list) is True


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('player_factory')
def test_get_player(mlsb_app, client, admin_header, player_factory):
    with mlsb_app.app_context():
        player = player_factory()
        response = client.get(
            url_for("rest.player", player_id=player.id),
            follow_redirects=True,
            headers=admin_header
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['player_id'] == player.id
        assert data['email'] is None
