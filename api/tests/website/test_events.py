import pytest
from datetime import date
from flask import url_for
from api.helper import loads
from api.model import LeagueEvent
from api.tests.fixtures import random_email

THIS_YEAR = date.today().year
INVALID_ENTITY = 100000000


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_events_page_json(mlsb_app, client):
    with mlsb_app.app_context():
        url = url_for(
            "website.events_page_json",
            year=THIS_YEAR,
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200
        data = loads(response.data)
        assert isinstance(data, list) is True


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('league_event_factory')
@pytest.mark.usefixtures('league_event_date_factory')
def test_signup_event(
    mlsb_app,
    client,
    auth,
    league_event_factory,
    league_event_date_factory
):
    with mlsb_app.app_context():
        auth.login(random_email())
        league_event_date = league_event_date_factory(
            league_event=league_event_factory()
        )
        url = url_for(
            "website.signup_event",
            league_event_date_id=league_event_date.id,
        )
        response = client.post(url, follow_redirects=True)
        assert response.status_code == 200


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('league_event_factory')
@pytest.mark.usefixtures('league_event_date_factory')
def test_signup_twice_for_event(
    mlsb_app,
    client,
    auth,
    league_event_factory,
    league_event_date_factory
):
    with mlsb_app.app_context():
        auth.login(random_email())
        league_event_date = league_event_date_factory(
            league_event=league_event_factory()
        )
        url = url_for(
            "website.signup_event",
            league_event_date_id=league_event_date.id,
        )
        client.post(url, follow_redirects=True)
        response = client.post(url, follow_redirects=True)
        assert response.status_code == 200


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
def test_signup_nonexistent_event(mlsb_app, client, auth):
    with mlsb_app.app_context():
        auth.login(random_email())
        url = url_for(
            "website.signup_event",
            league_event_date_id=INVALID_ENTITY,
        )
        response = client.post(url, follow_redirects=True)
        assert response.status_code == 404


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_events_page(mlsb_app, client):
    with mlsb_app.app_context():
        url = url_for(
            "website.events_page",
            year=THIS_YEAR,
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
def test_logged_in_events_page(mlsb_app, client, auth):
    with mlsb_app.app_context():
        # logged in still gets year events
        # will test underlying method later
        auth.login(random_email())
        url = url_for(
            "website.events_page",
            year=THIS_YEAR,
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200
