import pytest
from sqlalchemy import and_
from datetime import date
from flask import url_for
from random import randint
from api.model import Fun
from api.helper import loads


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_able_create_fun(mlsb_app, client, auth, convenor):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        count = randint(100, 300)
        year = date.today().year + 1
        response = client.post(
            url_for("rest.funs"),
            json={
                "year": year,
                "count": count
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['year'] == year
        assert data['count'] == count
        fun_exist = Fun.query.filter(and_(
            Fun.year == year, Fun.count == count
        )).first()
        assert fun_exist is not None


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_required_fields_of_fun(mlsb_app, client, auth, convenor):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        count = randint(100, 300)
        year = randint(2016, date.today().year)
        response = client.post(
            url_for("rest.funs"),
            json={
                "year": year,
            },
            follow_redirects=True
        )
        assert response.status_code == 400
        response = client.post(
            url_for("rest.funs"),
            json={
                "count": count,
            },
            follow_redirects=True
        )
        assert response.status_code == 400


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_update_fun(mlsb_app, client, auth, convenor):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        count = randint(100, 300)
        fun = Fun.query.filter(Fun.year == 2016).first()
        response = client.put(
            url_for("rest.fun", year=fun.year),
            json={
                "count": count
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['year'] == fun.year
        assert data['count'] == count
        fun_exist = Fun.query.filter(and_(
            Fun.year == 2016, Fun.count == count
        )).first()
        assert fun_exist is not None


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_delete_fun(mlsb_app, client, auth, convenor):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        fun = Fun.query.filter(Fun.year == 2016).first()
        response = client.delete(
            url_for("rest.fun", year=fun.year),
            follow_redirects=True,
        )
        assert response.status_code == 200
        fun_exist = Fun.query.filter(and_(
            Fun.year == fun.year, Fun.count == fun.count
        )).first()
        assert fun_exist is None


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
def test_get_all_fun(mlsb_app, client):
    with mlsb_app.app_context():
        response = client.get(
            url_for("rest.funs"),
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
def test_get_fun(mlsb_app, client):
    with mlsb_app.app_context():
        fun = Fun.query.filter(Fun.year == 2017).first()
        response = client.get(
            url_for("rest.fun", year=fun.year),
            follow_redirects=True
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['year'] == fun.year
        assert data['count'] == fun.count
