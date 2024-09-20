import pytest
from flask import url_for
from api.tests.fixtures import random_name
from api.model import League
from api.helper import loads


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_able_create_league(mlsb_app, client, auth, convenor):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        name = random_name("Rest")
        response = client.post(
            url_for("rest.leagues"),
            json={
                "league_name": name,
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['league_name'] == name
        assert isinstance(data['league_id'], int) is True
        assert League.does_league_exist(data['league_id']) is True


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_required_fields_of_league(mlsb_app, client, auth, convenor):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        response = client.post(
            url_for("rest.leagues"),
            json={},
            follow_redirects=True
        )
        assert response.status_code == 400


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('league_factory')
def test_update_league(mlsb_app, client, auth, convenor, league_factory):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        league = league_factory()
        name = random_name("Rest")
        response = client.put(
            url_for("rest.league", league_id=league.id),
            json={
                "league_name": name
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['league_name'] == name
        assert data['league_id'] == league.id
        assert League.query.filter(League.name == name).first() is not None


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('league_factory')
def test_delete_league(mlsb_app, client, auth, convenor, league_factory):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        league = league_factory()
        response = client.delete(
            url_for("rest.league", league_id=league.id),
            follow_redirects=True
        )
        assert response.status_code == 200
        assert League.does_league_exist(league.id) is False


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
def test_get_all_league(mlsb_app, client):
    with mlsb_app.app_context():
        response = client.get(
            url_for("rest.leagues"),
            follow_redirects=True
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert 'items' in data
        assert 'next_url' in data
        assert isinstance(data['items'], list) is True


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('league_factory')
def test_get_league(mlsb_app, client, league_factory):
    with mlsb_app.app_context():
        league = league_factory()
        response = client.get(
            url_for("rest.league", league_id=league.id),
            follow_redirects=True
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['league_id'] == league.id
        assert data['league_name'] == league.name
