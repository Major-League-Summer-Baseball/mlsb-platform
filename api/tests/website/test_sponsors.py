import pytest
from datetime import date
from flask import url_for
from api.helper import loads

THIS_YEAR = date.today().year
INVALID_ENTITY = 100000000


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_get_sponsor_breakdown(mlsb_app, client):
    with mlsb_app.app_context():
        url = url_for(
            "website.get_sponsor_breakdown",
            year=THIS_YEAR,
            garbage=INVALID_ENTITY
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200
        response_data = loads(response.data)
        assert response_data['name'] == "Sponsor Breakdown by ESPYS"
        assert isinstance(response_data['children'], list) is True


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_sponsor_breakdown_page(mlsb_app, client):
    with mlsb_app.app_context():
        url = url_for("website.sponsor_breakdown", year=THIS_YEAR)
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('sponsor_factory')
def test_sponsor_page(mlsb_app, client, sponsor_factory):
    with mlsb_app.app_context():
        sponsor = sponsor_factory()
        url = url_for(
            "website.sponsor_page",
            year=THIS_YEAR,
            sponsor_id=sponsor.id
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_nonexistent_sponsor_page(mlsb_app, client):
    with mlsb_app.app_context():
        url = url_for(
            "website.sponsor_page",
            year=THIS_YEAR,
            sponsor_id=INVALID_ENTITY
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200
        assert "<title>Not Found</title>" in response.data.decode("utf-8")


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_sponsors_page(mlsb_app, client):
    with mlsb_app.app_context():
        url = url_for(
            "website.sponsors_page",
            year=THIS_YEAR,
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200
