import pytest
from api.tests.fixtures import random_name
from api.model import League, Division
from flask import url_for


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
def test_convenor_league_page(
    mlsb_app, client, auth, convenor, league_factory, division_factory
):
    """Test convenor can view leagues/divisions."""
    with mlsb_app.app_context():
        league = league_factory()
        division = division_factory()
        auth.login(convenor.email)
        response = client.get(
            url_for("convenor.leagues_page"), follow_redirects=True
        )
        assert response.status_code == 200
        assert league.name in str(response.data)
        assert division.name in str(response.data)
        assert not url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_only_convenor_league_page(
    mlsb_app, client, auth
):
    """Test only convenor can view leagues/divisions."""
    with mlsb_app.app_context():
        auth.logout()
        response = client.get(
            url_for("convenor.leagues_page"), follow_redirects=True
        )
        assert url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_convenor_create_league(mlsb_app, client, auth, convenor):
    """Test convenor can create league."""
    with mlsb_app.app_context():
        name = random_name("League")
        auth.login(convenor.email)
        response = client.post(
            url_for("convenor.submit_league"),
            follow_redirects=True,
            data={
                'league_name': name
            }
        )
        assert response.status_code == 200
        assert name in str(response.data)
        assert not url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('league_factory')
def test_convenor_update_league(
    mlsb_app, client, auth, convenor, league_factory
):
    """Test convenor can update league."""
    with mlsb_app.app_context():
        league = league_factory()
        new_name = random_name("League")
        auth.login(convenor.email)
        response = client.post(
            url_for("convenor.submit_league"),
            follow_redirects=True,
            data={
                'league_name': new_name,
                'league_id': league.id
            }
        )
        assert response.status_code == 200
        assert new_name in str(response.data)
        assert not url_for("website.loginpage").endswith(response.request.path)
        updated_league = League.query.get(league.id)
        assert updated_league.name == new_name


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('league_factory')
def test_only_convenor_submit_league(
    mlsb_app, client, auth, league_factory
):
    """Test convenor can update league."""
    with mlsb_app.app_context():
        league = league_factory()
        new_name = random_name("League")
        auth.logout()
        response = client.post(
            url_for("convenor.submit_league"),
            follow_redirects=True,
            data={
                'league_name': new_name,
                'league_id': league.id
            }
        )
        assert url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_convenor_create_division(mlsb_app, client, auth, convenor):
    """Test convenor can create division."""
    with mlsb_app.app_context():
        name = random_name("Division")
        auth.login(convenor.email)
        response = client.post(
            url_for("convenor.submit_division"),
            follow_redirects=True,
            data={
                'division_name': name,
                'division_shortname': name[0: 1]
            }
        )
        assert response.status_code == 200
        assert name in str(response.data)
        assert not url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('division_factory')
def test_convenor_update_division(
    mlsb_app, client, auth, convenor, division_factory
):
    """Test convenor can update league."""
    with mlsb_app.app_context():
        division = division_factory()
        new_name = random_name("Division")
        auth.login(convenor.email)
        response = client.post(
            url_for("convenor.submit_division"),
            follow_redirects=True,
            data={
                'division_name': new_name,
                'division_shortname': new_name[0: 1],
                'division_id': division.id
            }
        )
        assert response.status_code == 200
        assert new_name in str(response.data)
        assert not url_for("website.loginpage").endswith(response.request.path)
        updated_division = Division.query.get(division.id)
        assert updated_division.name == new_name


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('division_factory')
def test_only_convenor_submit_division(
    mlsb_app, client, auth, division_factory
):
    """Test convenor can update league."""
    with mlsb_app.app_context():
        division = division_factory()
        new_name = random_name("League")
        auth.logout()
        response = client.post(
            url_for("convenor.submit_division"),
            follow_redirects=True,
            data={
                'division_name': new_name,
                'division_shortname': new_name[0: 1],
                'division_id': division.id
            }
        )
        assert url_for("website.loginpage").endswith(response.request.path)
