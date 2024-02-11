import pytest
from flask import url_for
from datetime import datetime


@pytest.mark.routes
@pytest.mark.parametrize("route", [
    "component_fun_meter",
    "component_score_banner",
    "component_sponsor_banner"
])
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_various_components(mlsb_app, client, route):
    """Test any components properly respond 200."""
    with mlsb_app.app_context():
        url = url_for(f"website.{route}", year=datetime.now().year)
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200
