import pytest
from flask import url_for
from api.tests.fixtures import random_name
from api.model import Division
from api.helper import loads


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_able_create_division(mlsb_app, client, auth, convenor):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        name = random_name("Rest")
        response = client.post(
            url_for("rest.divisions"),
            json={
                "division_name": name,
                "division_shortname": name[0:4]
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['division_name'] == name
        assert data['division_shortname'] in name
        assert isinstance(data['division_id'], int) is True
        assert Division.does_division_exist(data['division_id']) is True


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_required_fields_of_division(mlsb_app, client, auth, convenor):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        name = random_name("Rest")
        response = client.post(
            url_for("rest.divisions"),
            json={
                "division_shortname": name[0:4]
            },
            follow_redirects=True
        )
        assert response.status_code == 400


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('division_factory')
def test_update_division(mlsb_app, client, auth, convenor, division_factory):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        division = division_factory()
        name = random_name("Rest")
        response = client.put(
            url_for("rest.division", division_id=division.id),
            json={
                "division_name": name
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['division_name'] == name
        assert data['division_id'] == division.id
        assert Division.query.filter(Division.name == name).first() is not None


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('division_factory')
def test_delete_division(mlsb_app, client, auth, convenor, division_factory):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        division = division_factory()
        response = client.delete(
            url_for("rest.division", division_id=division.id),
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert Division.does_division_exist(division.id) is False


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
def test_get_all_division(mlsb_app, client):
    with mlsb_app.app_context():
        response = client.get(
            url_for("rest.divisions"),
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
@pytest.mark.usefixtures('division_factory')
def test_get_division(mlsb_app, client, division_factory):
    with mlsb_app.app_context():
        division = division_factory()
        response = client.get(
            url_for("rest.division", division_id=division.id),
            follow_redirects=True,
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['division_id'] == division.id
        assert data['division_name'] == division.name
