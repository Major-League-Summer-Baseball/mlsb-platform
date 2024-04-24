import pytest
import random
from datetime import date
from api.model import Fun
from flask import url_for


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('fun_factory')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_convenor_fun_page(
    mlsb_app, client, fun_factory, auth, convenor
):
    """Test able to view/edit league events."""
    with mlsb_app.app_context():
        too_much_fun = random.randint(999999, 9999999)
        fun = fun_factory(count=too_much_fun)
        auth.login(convenor.email)
        response = client.get(
            url_for("convenor.fun_page"),
            follow_redirects=True,
        )
        assert response.status_code == 200
        data = response.data
        assert str(fun.count) in str(data)
        assert not url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_convenor_submit_new_fun(mlsb_app, client, auth, convenor):
    """Test able to view/edit league events."""
    with mlsb_app.app_context():
        count = random.randint(9999, 99999)
        auth.login(convenor.email)
        response = client.post(
            url_for("convenor.submit_fun"),
            follow_redirects=True,
            data={
                "year": date.today().year,
                "count": count
            }
        )
        assert response.status_code == 200
        assert str(count) in str(response.data)
        assert not url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('fun_factory')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_convenor_submit_updated_fun(
    mlsb_app, client, auth, convenor, fun_factory
):
    """Test able to view/edit league events."""
    with mlsb_app.app_context():
        fun = fun_factory()
        count = random.randint(9999, 99999)
        auth.login(convenor.email)
        response = client.post(
            url_for("convenor.submit_fun"),
            follow_redirects=True,
            data={
                "year": fun.year,
                "count": count,
                "fun_id": fun.id
            }
        )
        assert response.status_code == 200
        assert str(count) in str(response.data)
        assert not url_for("website.loginpage").endswith(response.request.path)
        updated_fun = Fun.query.get(fun.id)
        assert updated_fun.count == count


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
def test_only_convenor_fun_page(mlsb_app, client, auth):
    """Test only convenor able to view/edit fun."""
    with mlsb_app.app_context():
        auth.logout()
        response = client.get(
            url_for("convenor.fun_page"),
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
def test_only_convenor_submit_fun(mlsb_app, client, auth):
    """Test only convenor able to view/edit fun."""
    with mlsb_app.app_context():
        auth.logout()
        response = client.post(
            url_for("convenor.submit_fun"),
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert url_for("website.loginpage").endswith(response.request.path)
