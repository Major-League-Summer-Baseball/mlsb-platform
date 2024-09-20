import pytest
from flask import url_for
from api.tests.fixtures import random_name
from api.model import LeagueEvent
from api.helper import loads


@pytest.mark.rest
@pytest.mark.parametrize("league_event_data", [
    (True,),
    (False,),
    (1,),
    (0,)
])
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_able_create_league_event(
    mlsb_app,
    client,
    auth,
    convenor,
    league_event_data
):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        name = random_name("Rest")
        description = random_name("Description")
        active = league_event_data[0]
        active = active if bool(active) else active == 1
        response = client.post(
            url_for("rest.league_events"),
            json={
                "name": name,
                "description": description,
                "active": active
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['name'] == name
        assert data['description'] == description
        assert isinstance(data['league_event_id'], int) is True
        assert LeagueEvent.is_league_event(data['league_event_id']) is True


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_required_fields_of_league_event(mlsb_app, client, auth, convenor):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        name = random_name("Rest")
        description = random_name("Description")
        response = client.post(
            url_for("rest.league_events"),
            json={
                "name": name,
                "active": True
            },
            follow_redirects=True
        )
        assert response.status_code == 400

        response = client.post(
            url_for("rest.league_events"),
            json={
                "description": description,
                "active": True
            },
            follow_redirects=True
        )
        assert response.status_code == 400


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('league_event_factory')
def test_update_league_event(
    mlsb_app,
    client,
    auth,
    convenor,
    league_event_factory
):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        league_event = league_event_factory()
        name = random_name("Rest")
        response = client.put(
            url_for("rest.league_event", league_event_id=league_event.id),
            json={
                "name": name,
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['name'] == name
        assert data['league_event_id'] == league_event.id
        assert LeagueEvent.query.filter(
            LeagueEvent.name == name
        ).first() is not None


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('league_event_factory')
def test_delete_league_event(
    mlsb_app,
    client,
    auth,
    convenor,
    league_event_factory
):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        league_event = league_event_factory()
        response = client.delete(
            url_for("rest.league_event", league_event_id=league_event.id),
            follow_redirects=True
        )
        assert response.status_code == 200
        assert LeagueEvent.is_league_event(league_event.id) is False


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
def test_get_all_league_event(mlsb_app, client):
    with mlsb_app.app_context():
        response = client.get(
            url_for("rest.league_events"),
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
@pytest.mark.usefixtures('league_event_factory')
def test_get_league_event(
    mlsb_app,
    client,
    league_event_factory
):
    with mlsb_app.app_context():
        league_event = league_event_factory()
        response = client.get(
            url_for("rest.league_event", league_event_id=league_event.id),
            follow_redirects=True
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['league_event_id'] == league_event.id
        assert data['name'] == league_event.name
        assert data['description'] == league_event.description
        assert data['active'] == league_event.active
