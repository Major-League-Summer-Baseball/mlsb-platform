import pytest
from flask import url_for
from datetime import datetime
from api.model import LeagueEventDate, split_datetime
from api.helper import loads


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('league_event_factory')
def test_able_create_league_event_date(
    mlsb_app,
    client,
    auth,
    convenor,
    league_event_factory
):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        league_event = league_event_factory()
        event_date, event_time = split_datetime(datetime.today())
        response = client.post(
            url_for("rest.league_event_dates"),
            json={
                "league_event_id": league_event.id,
                "date": event_date,
                "time": event_time
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['league_event_id'] == league_event.id
        assert data['date'] == event_date
        assert data['time'] == event_time
        assert isinstance(data['league_event_date_id'], int) is True
        assert LeagueEventDate.query.filter(
            LeagueEventDate.league_event_id == league_event.id
        ).first() is not None


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('league_event_factory')
def test_required_fields_of_league_event_date(
    mlsb_app,
    client,
    auth,
    convenor,
    league_event_factory
):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        league_event = league_event_factory()
        event_date, event_time = split_datetime(datetime.today())
        response = client.post(
            url_for("rest.league_event_dates"),
            json={
                "date": event_date,
                "time": event_time
            },
            follow_redirects=True
        )
        assert response.status_code == 400

        response = client.post(
            url_for("rest.league_event_dates"),
            json={
                "league_event_id": league_event.id,
                "time": event_time
            },
            follow_redirects=True
        )
        assert response.status_code == 400

        response = client.post(
            url_for("rest.league_event_dates"),
            json={
                "league_event_id": league_event.id,
                "date": event_date,
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
@pytest.mark.usefixtures('league_event_date_factory')
def test_update_league_event_date(
    mlsb_app,
    client,
    auth,
    convenor,
    league_event_factory,
    league_event_date_factory
):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        league_event = league_event_factory()
        league_event_date = league_event_date_factory(league_event=league_event)
        event_date, event_time = split_datetime(datetime.today())
        response = client.put(
            url_for(
                "rest.league_event_date",
                league_event_date_id=league_event_date.id
            ),
            json={
                "date": event_date,
                "time": event_time
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['date'] == event_date
        assert data['time'] == event_time
        assert data['league_event_date_id'] == league_event_date.id


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('league_event_factory')
@pytest.mark.usefixtures('league_event_date_factory')
def test_delete_league_event_date(
    mlsb_app,
    client,
    auth,
    convenor,
    league_event_factory,
    league_event_date_factory
):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        league_event = league_event_factory()
        league_event_date = league_event_date_factory(league_event=league_event)
        response = client.delete(
            url_for(
                "rest.league_event_date",
                league_event_date_id=league_event_date.id
            ),
            follow_redirects=True
        )
        assert response.status_code == 200
        assert LeagueEventDate.query.filter(
            LeagueEventDate.league_event_id == league_event.id
        ).first() is None


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
def test_get_all_league_event_date(mlsb_app, client):
    with mlsb_app.app_context():
        response = client.get(
            url_for("rest.league_event_dates"),
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
@pytest.mark.usefixtures('league_event_date_factory')
def test_get_league_event_date(
    mlsb_app,
    client,
    league_event_factory,
    league_event_date_factory
):
    with mlsb_app.app_context():
        league_event = league_event_factory()
        league_event_date = league_event_date_factory(league_event=league_event)
        response = client.get(
            url_for(
                "rest.league_event_date",
                league_event_date_id=league_event_date.id
            ),
            follow_redirects=True
        )
        assert response.status_code == 200
        data = loads(response.data)
        expected = league_event_date.json()
        assert data['league_event_date_id'] == league_event_date.id
        assert data['league_event_id'] == league_event.id
        assert data['date'] == expected['date']
        assert data['time'] == expected['time']
