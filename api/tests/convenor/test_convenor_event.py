import pytest
from datetime import datetime
from api.tests.fixtures import random_name
from api.model import LeagueEvent, LeagueEventDate, split_datetime
from flask import url_for


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('league_event_factory')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_convenor_league_events_page(
    mlsb_app, client, league_event_factory, auth, convenor
):
    """Test able to view/edit league events."""
    with mlsb_app.app_context():
        league_event = league_event_factory()
        auth.login(convenor.email)
        response = client.get(
            url_for("convenor.events_page"),
            follow_redirects=True,
        )
        assert response.status_code == 200
        data = response.data
        assert league_event.name in str(data)
        assert not url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('league_event_factory')
def test_league_events_only_convenors_page(mlsb_app, client, auth):
    """Test only convenors able to edit/view league events."""
    with mlsb_app.app_context():
        auth.logout()
        response = client.get(
            url_for("convenor.events_page"),
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('league_event_factory')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_convenor_league_event_page(
    mlsb_app, client, league_event_factory, auth, convenor
):
    """Test able to view/edit specific league event."""
    with mlsb_app.app_context():
        league_event = league_event_factory()
        auth.login(convenor.email)
        response = client.get(
            url_for("convenor.event_page", league_event_id=league_event.id),
            follow_redirects=True,
        )
        assert response.status_code == 200
        data = response.data
        assert league_event.name in str(data)
        assert not url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('league_event_factory')
def test_league_event_only_convenor_page(
    mlsb_app, client, league_event_factory, auth
):
    """Test able to view/edit specific league event."""
    with mlsb_app.app_context():
        league_event = league_event_factory()
        auth.logout()
        response = client.get(
            url_for("convenor.event_page", league_event_id=league_event.id),
            follow_redirects=True,
        )
        assert url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('league_event_factory')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_convenor_update_league_event(
    mlsb_app, client, league_event_factory, auth, convenor
):
    """Test convenor able to update league event."""
    with mlsb_app.app_context():
        league_event = league_event_factory()
        name = random_name("League Event")
        description = random_name("Description")
        auth.login(convenor.email)
        response = client.post(
            url_for("convenor.submit_event"),
            follow_redirects=True,
            data={
                "name": name,
                "description": description,
                "league_event_id": league_event.id
            }
        )
        data = response.data
        assert not url_for("website.loginpage").endswith(response.request.path)
        assert name in str(data)
        assert description in str(data)
        updated_event = LeagueEvent.query.get(league_event.id)
        assert updated_event.name == name


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_convenor_create_league_event(mlsb_app, client, auth, convenor):
    """Test convenor able to update league event."""
    with mlsb_app.app_context():
        name = random_name("League Event")
        description = random_name("Description")
        auth.login(convenor.email)
        response = client.post(
            url_for("convenor.submit_event"),
            follow_redirects=True,
            data={
                "name": name,
                "description": description,
            }
        )
        data = response.data
        assert not url_for("website.loginpage").endswith(response.request.path)
        assert name in str(data)
        assert description in str(data)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
def test_only_convenor_submit_league_event(mlsb_app, client, auth):
    """Test only convenor able to submit league event."""
    with mlsb_app.app_context():
        name = random_name("League Event")
        description = random_name("Description")
        auth.logout()
        response = client.post(
            url_for("convenor.submit_event"),
            follow_redirects=True,
            data={
                "name": name,
                "description": description,
            }
        )
        assert url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('league_event_factory')
def test_convenor_make_league_event_visible(
    mlsb_app, client, auth, convenor, league_event_factory
):
    """Test convenor about to make league event visible."""
    with mlsb_app.app_context():
        league_event = league_event_factory(active=False)
        auth.login(convenor.email)
        response = client.get(
            url_for(
                "convenor.change_event_visibility",
                league_event_id=league_event.id,
                visible=1
            ),
            follow_redirects=True
        )
        assert not url_for("website.loginpage").endswith(response.request.path)
        updated_event = LeagueEvent.query.get(league_event.id)
        assert updated_event.active is True


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('league_event_factory')
def test_convenor_make_league_event_not_visible(
    mlsb_app, client, auth, convenor, league_event_factory
):
    """Test convenor about to make league event not visible."""
    with mlsb_app.app_context():
        league_event = league_event_factory(active=True)
        auth.login(convenor.email)
        response = client.get(
            url_for(
                "convenor.change_event_visibility",
                league_event_id=league_event.id,
                visible=0
            ),
            follow_redirects=True
        )
        assert not url_for("website.loginpage").endswith(response.request.path)
        updated_event = LeagueEvent.query.get(league_event.id)
        assert updated_event.active is False


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('league_event_factory')
def test_only_convenor_change_league_event_not_visibility(
    mlsb_app, client, auth, league_event_factory
):
    """Test only convenor can change league event visibility."""
    with mlsb_app.app_context():
        league_event = league_event_factory(active=True)
        auth.logout()
        response = client.get(
            url_for(
                "convenor.change_event_visibility",
                league_event_id=league_event.id,
                visible=0
            ),
            follow_redirects=True
        )
        assert url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('league_event_factory')
@pytest.mark.usefixtures('league_event_date_factory')
def test_convenor_update_league_event_date(
    mlsb_app,
    client,
    auth,
    convenor,
    league_event_factory,
    league_event_date_factory
):
    """Test convenor able to update league event."""
    with mlsb_app.app_context():
        league_event = league_event_factory()
        league_event_date = league_event_date_factory(league_event)
        event_date, event_time = split_datetime(datetime.today())
        auth.login(convenor.email)
        response = client.post(
            url_for(
                "convenor.submit_event_date", league_event_id=league_event.id
            ),
            follow_redirects=True,
            data={
                "time": event_time,
                "date": event_date,
                "league_event_date_id": league_event_date.id
            }
        )
        assert not url_for("website.loginpage").endswith(response.request.path)
        updated_event_date = LeagueEventDate.query.get(league_event_date.id)
        data = updated_event_date.json()
        assert data['time'] == event_time
        assert data['date'] == event_date


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('league_event_factory')
def test_convenor_create_league_event_date(
    mlsb_app,
    client,
    auth,
    convenor,
    league_event_factory
):
    """Test convenor able to update league event."""
    with mlsb_app.app_context():
        league_event = league_event_factory()
        event_date, event_time = split_datetime(datetime.today())
        auth.login(convenor.email)
        response = client.post(
            url_for(
                "convenor.submit_event_date", league_event_id=league_event.id
            ),
            follow_redirects=True,
            data={
                "time": event_time,
                "date": event_date,
            }
        )
        assert not url_for("website.loginpage").endswith(response.request.path)
        updated_event_date = LeagueEventDate.query.filter(
            LeagueEventDate.league_event_id == league_event.id
        ).first()
        assert updated_event_date is not None
        data = updated_event_date.json()
        assert data['time'] == event_time
        assert data['date'] == event_date


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('league_event_factory')
def test_only_convenor_submit_league_event_date(
    mlsb_app,
    client,
    auth,
    league_event_factory
):
    """Test convenor able to update league event."""
    with mlsb_app.app_context():
        league_event = league_event_factory()
        event_date, event_time = split_datetime(datetime.today())
        auth.logout()
        response = client.post(
            url_for(
                "convenor.submit_event_date", league_event_id=league_event.id
            ),
            follow_redirects=True,
            data={
                "time": event_time,
                "date": event_date,
            }
        )
        assert url_for("website.loginpage").endswith(response.request.path)
        updated_event_date = LeagueEventDate.query.filter(
            LeagueEventDate.league_event_id == league_event.id
        ).first()
        assert updated_event_date is None
