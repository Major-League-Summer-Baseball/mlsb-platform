import pytest
from api.tests.fixtures import random_name
from api.model import Sponsor
from api.extensions import DB
from flask import url_for


NONEXISTENT = -1


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_sponsor_page_only_convenors(mlsb_app, client):
    """Test only convenors can edit/add sponsors"""
    with mlsb_app.app_context():
        url = url_for("convenor.sponsors_page")
        response = client.get(url, follow_redirects=True)
        assert url_for("website.loginpage").endswith(response.request.path)
        assert response.status_code == 200


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('sponsor_factory')
def test_convenor_sponsor_page(
    mlsb_app, client, auth, convenor, sponsor_factory
):
    """Test convenor can view sponsors"""
    with mlsb_app.app_context():
        sponsor = sponsor_factory()
        auth.login(convenor.email)
        response = client.get(
            url_for("convenor.sponsors_page"), follow_redirects=True
        )
        assert response.status_code == 200
        assert sponsor.name in str(response.data)
        assert not url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_convenor_create_sponsor(
    mlsb_app, client, auth, convenor
):
    with mlsb_app.app_context():
        name = random_name('sponsor')
        description = "some description"
        link = "https://github.com"
        auth.login(convenor.email)
        response = client.post(
            url_for("convenor.submit_sponsor"),
            follow_redirects=True,
            data={
                "sponsor_name": name,
                "link": link,
                "description": description
            }
        )
        assert response.status_code == 200
        assert name in str(response.data)
        assert link in str(response.data)
        assert description in str(response.data)
        assert not url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('sponsor_factory')
def test_convenor_edit_sponsor(
    mlsb_app, client, auth, convenor, sponsor_factory
):
    with mlsb_app.app_context():
        sponsor = sponsor_factory()
        name = random_name('sponsor')
        description = "some description"
        link = "https://github.com"
        auth.login(convenor.email)
        response = client.post(
            url_for("convenor.submit_sponsor"),
            follow_redirects=True,
            data={
                "sponsor_name": name,
                "link": link,
                "description": description,
                "sponsor_id": sponsor.id
            }
        )
        assert response.status_code == 200
        assert name in str(response.data)
        assert link in str(response.data)
        assert description in str(response.data)
        assert not url_for("website.loginpage").endswith(response.request.path)
        updated_sponsor = Sponsor.query.get(sponsor.id)
        assert updated_sponsor.name == name


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('sponsor_factory')
def test_only_convenor_edit_sponsor(
    mlsb_app, client, sponsor_factory
):
    """Test only convenors can update/create sponsors"""
    with mlsb_app.app_context():
        sponsor = sponsor_factory()
        name = random_name('sponsor')
        description = "some description"
        link = "https://github.com"
        response = client.post(
            url_for("convenor.submit_sponsor"),
            follow_redirects=True,
            data={
                "sponsor_name": name,
                "link": link,
                "description": description,
                "sponsor_id": sponsor.id
            }
        )
        assert url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('sponsor_factory')
def test_convenor_make_sponsor_visible(
    mlsb_app, client, auth, convenor, sponsor_factory
):
    """Test convenors can make a sponsor visible."""
    with mlsb_app.app_context():
        sponsor = sponsor_factory()
        sponsor.deactivate()
        DB.session.commit()
        auth.login(convenor.email)
        response = client.post(
            url_for(
                "convenor.change_visibility", sponsor_id=sponsor.id, visible=1
            ),
            follow_redirects=True,
        )
        assert response.status_code == 200
        updated_sponsor = Sponsor.query.get(sponsor.id)
        assert updated_sponsor.active is True


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('sponsor_factory')
def test_convenor_make_sponsor_not_visible(
    mlsb_app, client, auth, convenor, sponsor_factory
):
    """Test convenors can make a sponsor visible."""
    with mlsb_app.app_context():
        sponsor = sponsor_factory()
        auth.login(convenor.email)
        response = client.post(
            url_for(
                "convenor.change_visibility", sponsor_id=sponsor.id, visible=0
            ),
            follow_redirects=True,
        )
        assert response.status_code == 200
        updated_sponsor = Sponsor.query.get(sponsor.id)
        assert updated_sponsor.active is False


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('sponsor_factory')
def test_only_convenor_change_sponsor_visibility(
    mlsb_app, client, auth, convenor, sponsor_factory
):
    """Test only convenors can change a sponsor visibility."""
    with mlsb_app.app_context():
        sponsor = sponsor_factory()
        response = client.post(
            url_for(
                "convenor.change_visibility", sponsor_id=sponsor.id, visible=0
            ),
            follow_redirects=True,
        )
        assert url_for("website.loginpage").endswith(response.request.path)
