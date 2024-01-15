import pytest
from datetime import datetime
from flask import url_for
from api.helper import loads


@pytest.mark.routes
@pytest.mark.parametrize("year", [
    2016,
    datetime.now().year
])
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_homepage_different_years(mlsb_app, client, year):
    with mlsb_app.app_context():
        url = url_for('website.index', year=year)
        response = client.get(url, follow_redirects=True)        
        assert response.status_code == 200


@pytest.mark.routes
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_homepage_article(mlsb_app, client):
    with mlsb_app.app_context():
        url = url_for('website.index', year=2016)
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200
        data = response.data
        assert "MLSB Player Feature Week 2" in str(data)


@pytest.mark.routes
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_posts_json(mlsb_app, client):
    with mlsb_app.app_context():
        url = url_for('website.posts_json', year=2016)
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200
        response_json = loads(response.data)
        expected_json = [
            {'date': '20160713', 'description': 'Ladies.html'},
            {'date': '20160609', 'description': 'VinceJP.html'},
            {'date': '20160422', 'description': 'Launch.html'},
            {'date': '20160713', 'description': 'SeasonRoundUp.html'},
            {'date': '20160507', 'description': 'Kik.html'},
            {'date': '20160629', 'description': 'Rory.html'}
        ]
        assert response_json == expected_json, "Static 2016 posts"


@pytest.mark.routes
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_checkout_post(mlsb_app, client):
    with mlsb_app.app_context():
        url = url_for(
            'website.checkout_post',
            year=2016,
            date='20160713',
            file_name='Ladies.html'
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200
        data = response.data
        assert "Posts not Found" not in str(data)


@pytest.mark.routes
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_checkout_nonexistent_post(mlsb_app, client):
    with mlsb_app.app_context():
        url = url_for(
            'website.checkout_post',
            year=2016,
            date='20160713',
            file_name='LadiesMissing'
        )
        response = client.get(url, follow_redirects=True)
        # still 200 since send not found
        assert response.status_code == 200
        data = response.data
        assert "Posts not Found" in str(data)

@pytest.mark.routes
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_checkout_post_json(mlsb_app, client):
    with mlsb_app.app_context():
        url = url_for(
            'website.checkout_post_json',
            year=2016,
            date='20160713',
            file_name='Ladies.html'
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200
        data = response.data
        assert loads(data) != {}
        assert len(loads(data)) == 2


@pytest.mark.routes
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_checkout_nonexistent_post_json(mlsb_app, client):
    with mlsb_app.app_context():
        url = url_for(
            'website.checkout_post_json',
            year=2016,
            date='20160713',
            file_name='LadiesMissing'
        )
        response = client.get(url, follow_redirects=True)
        # still 200 since send not found
        assert response.status_code == 200
        data = response.data
        assert loads(data) == {}, "Empty data for non-existent post"


@pytest.mark.routes
@pytest.mark.parametrize("picture_name", [
    "bot.png",
    "ladies.jpg",
    "crank.png"
])
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_get_posts_pictures(mlsb_app, client, picture_name):
    with mlsb_app.app_context():
        url = url_for('website.post_picture', name=picture_name)
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200


@pytest.mark.routes
@pytest.mark.parametrize("picture_name", [
    "WTF.png"
])
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_get_nonexistent_posts_pictures(mlsb_app, client, picture_name):
    with mlsb_app.app_context():
        url = url_for('website.post_picture', name=picture_name)
        response = client.get(url, follow_redirects=True)
        # sends a not found picture
        assert response.status_code == 200