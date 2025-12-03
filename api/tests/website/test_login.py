import pytest
from flask import url_for
from datetime import datetime


@pytest.mark.routes
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_join_league_requires_an_email(mlsb_app, client):
    """Test unable to send join league request with no email."""
    with mlsb_app.app_context():
        with client.session_transaction() as session:
            session["oauth_email"] = None
        url = url_for("website.join_league", year=datetime.now().year)
        response = client.post(url, follow_redirects=True)
        assert response.status_code == 400
        assert "did not give an email" in str(response.data)


@pytest.mark.routes
@pytest.mark.parametrize("invalid_email", [
    "@@dallas",
    "Drop table",
    "-1 SELECT"
])
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_join_league_requires_valid_email(mlsb_app, client, invalid_email):
    """Test unable to create join league request with invalid email."""
    with mlsb_app.app_context():
        invalid_email = ''
        with client.session_transaction() as session:
            session["oauth_email"] = invalid_email
        url = url_for("website.join_league", year=datetime.now().year)
        response = client.post(url, follow_redirects=True)
        assert response.status_code == 400
        assert invalid_email in str(response.data)
