import pytest
from flask import url_for
from api.tests.fixtures import random_name
from api.model import Sponsor
from api.helper import loads


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_able_create_sponsor(mlsb_app, client, auth, convenor):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        name = random_name("Rest")
        response = client.post(
            url_for("rest.sponsors"),
            json={
                "sponsor_name": name,
                "link": None,
                "description": None,
                'active': True
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['sponsor_name'] == name
        assert data['link'] is None
        assert data['description'] is None
        assert data['active'] is True
        assert isinstance(data['sponsor_id'], int) is True
        assert Sponsor.does_sponsor_exist(data['sponsor_id']) is True


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_required_fields_of_sponsor(mlsb_app, client, auth, convenor):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        response = client.post(
            url_for("rest.sponsors"),
            json={
                "link": None,
                "description": None,
                'active': True
            },
            follow_redirects=True,
        )
        assert response.status_code == 400


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('sponsor_factory')
def test_update_sponsor(mlsb_app, client, auth, convenor, sponsor_factory):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        sponsor = sponsor_factory()
        name = random_name("Rest")
        response = client.put(
            url_for("rest.sponsor", sponsor_id=sponsor.id),
            json={
                "sponsor_name": name
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['sponsor_name'] == name
        assert data['sponsor_id'] == sponsor.id
        assert Sponsor.query.filter(Sponsor.name == name).first() is not None


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('sponsor_factory')
def test_delete_sponsor(mlsb_app, client, auth, convenor, sponsor_factory):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        sponsor = sponsor_factory()
        response = client.delete(
            url_for("rest.sponsor", sponsor_id=sponsor.id),
            follow_redirects=True
        )
        assert response.status_code == 200
        assert Sponsor.does_sponsor_exist(sponsor.id) is False


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
def test_get_all_sponsor(mlsb_app, client):
    with mlsb_app.app_context():
        response = client.get(
            url_for("rest.sponsors"),
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
@pytest.mark.usefixtures('sponsor_factory')
def test_get_sponsor(mlsb_app, client, sponsor_factory):
    with mlsb_app.app_context():
        sponsor = sponsor_factory()
        response = client.get(
            url_for("rest.sponsor", sponsor_id=sponsor.id),
            follow_redirects=True
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['sponsor_id'] == sponsor.id
        assert data['sponsor_name'] == sponsor.name
