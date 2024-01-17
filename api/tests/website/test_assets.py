import pytest
from datetime import datetime
from flask import url_for
from api.helper import loads



@pytest.mark.routes
@pytest.mark.parametrize("route", [
    "mlsb_favicon",
    "mlsb_logo",
    "mlsb_colors"
])
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_static_assets(mlsb_app, client, route):
    """Test any static asset route  - does not change year over year."""
    with mlsb_app.app_context():
        url = url_for(f"website.{route}")
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200


@pytest.mark.routes
@pytest.mark.parametrize("year", [
    2016,
    datetime.now().year
])
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_promos_page_different_years(mlsb_app, client, year):
    with mlsb_app.app_context():
        url = url_for('website.promos_page', year=year)
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200

@pytest.mark.routes
@pytest.mark.parametrize("year", [
    2016,
    2017,
    2018
])
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_mlsb_colors_year_different_years(mlsb_app, client, year):
    with mlsb_app.app_context():
        url = url_for('website.mlsb_colors_year', year=year)
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200


@pytest.mark.routes
@pytest.mark.parametrize("year", [
    datetime.now().year + 1
])
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_mlsb_colors_year_future_years(mlsb_app, client, year):
    with mlsb_app.app_context():
        url = url_for('website.mlsb_colors_year', year=year)
        response = client.get(url, follow_redirects=True)
        # still get the base colors until defined
        assert response.status_code == 200


@pytest.mark.routes
@pytest.mark.parametrize("year", [
    2016,
    2017,
    2018
])
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_mlsb_logo_year_different_years(mlsb_app, client, year):
    with mlsb_app.app_context():
        url = url_for('website.mlsb_logo_year', year=year)
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200


@pytest.mark.routes
@pytest.mark.parametrize("year", [
    datetime.now().year + 1
])
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_mlsb_logo_year_future_years(mlsb_app, client, year):
    with mlsb_app.app_context():
        url = url_for('website.mlsb_logo_year', year=year)
        response = client.get(url, follow_redirects=True)
        # still get the base colors until defined
        assert response.status_code == 200


@pytest.mark.routes
@pytest.mark.parametrize("year", [
    2016,
    2017,
    2018
])
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_mlsb_favicon_year_different_years(mlsb_app, client, year):
    with mlsb_app.app_context():
        url = url_for('website.mlsb_favicon_year', year=year)
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200


@pytest.mark.routes
@pytest.mark.parametrize("year", [
    datetime.now().year + 1
])
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_mlsb_favicon_year_future_years(mlsb_app, client, year):
    with mlsb_app.app_context():
        url = url_for('website.mlsb_favicon_year', year=year)
        response = client.get(url, follow_redirects=True)
        # still get the base colors until defined
        assert response.status_code == 200