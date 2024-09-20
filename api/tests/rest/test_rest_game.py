import pytest
from flask import url_for
from datetime import datetime
from api.model import Game, split_datetime
from api.helper import loads


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
def test_able_create_game(
    mlsb_app,
    client,
    auth,
    convenor,
    sponsor_factory,
    team_factory,
    league_factory,
    division_factory
):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        division = division_factory()
        league = league_factory()
        sponsor = sponsor_factory()
        home_team = team_factory(sponsor=sponsor, league=league)
        away_team = team_factory(sponsor=sponsor, league=league)
        field = "WP1"
        game_date, game_time = split_datetime(datetime.today())

        response = client.post(
            url_for("rest.games"),
            json={
                "home_team_id": home_team.id,
                "away_team_id": away_team.id,
                "league_id": league.id,
                "division_id": division.id,
                "date": game_date,
                "time": game_time,
                "field": field
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['home_team_id'] == home_team.id
        assert data['away_team_id'] == away_team.id
        assert data['league_id'] == league.id
        assert data['division_id'] == division.id
        assert data['field'] == field
        assert data['date'] == game_date
        assert data['time'] == game_time
        assert isinstance(data['game_id'], int) is True
        assert Game.does_game_exist(data['game_id'])


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
def test_required_fields_of_game(
    mlsb_app,
    client,
    auth,
    convenor,
    sponsor_factory,
    team_factory,
    league_factory,
    division_factory
):
    with mlsb_app.app_context():
        division = division_factory()
        league = league_factory()
        sponsor = sponsor_factory()
        home_team = team_factory(sponsor=sponsor, league=league)
        away_team = team_factory(sponsor=sponsor, league=league)
        field = "WP1"
        game_date, game_time = split_datetime(datetime.today())

        response = client.post(
            url_for("rest.games"),
            json={
                "home_team_id": home_team.id,
                "league_id": league.id,
                "division_id": division.id,
                "date": game_date,
                "time": game_time,
                "field": field
            },
            follow_redirects=True
        )
        assert response.status_code == 400

        response = client.post(
            url_for("rest.games"),
            json={
                "away_team_id": away_team.id,
                "league_id": league.id,
                "division_id": division.id,
                "date": game_date,
                "time": game_time,
                "field": field
            },
            follow_redirects=True
        )
        assert response.status_code == 400

        response = client.post(
            url_for("rest.games"),
            json={
                "home_team_id": home_team.id,
                "away_team_id": away_team.id,
                "league_id": league.id,
                "date": game_date,
                "time": game_time,
                "field": field
            },
            follow_redirects=True
        )
        assert response.status_code == 400

        response = client.post(
            url_for("rest.games"),
            json={
                "home_team_id": home_team.id,
                "away_team_id": away_team.id,
                "division_id": division.id,
                "date": game_date,
                "time": game_time,
                "field": field
            },
            follow_redirects=True
        )
        assert response.status_code == 400


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('game_factory')
def test_update_game(
    mlsb_app,
    client,
    auth,
    convenor,
    sponsor_factory,
    team_factory,
    league_factory,
    division_factory,
    game_factory
):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        division = division_factory()
        league = league_factory()
        sponsor = sponsor_factory()
        home_team = team_factory(sponsor=sponsor, league=league)
        away_team = team_factory(sponsor=sponsor, league=league)
        field = "WP2"
        game_date, game_time = split_datetime(datetime.today())
        game = game_factory(
            home_team=home_team,
            away_team=away_team,
            league=league,
            division=division,
        )

        response = client.put(
            url_for("rest.game", game_id=game.id),
            json={
                "date": game_date,
                "time": game_time,
                "field": field
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        data = loads(response.data)
        assert data['date'] == game_date
        assert data['time'] == game_time
        assert data['field'] == field


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('game_factory')
def test_delete_game(
    mlsb_app,
    client,
    auth,
    convenor,
    sponsor_factory,
    team_factory,
    league_factory,
    division_factory,
    game_factory
):
    with mlsb_app.app_context():
        auth.login(convenor.email)
        division = division_factory()
        league = league_factory()
        sponsor = sponsor_factory()
        home_team = team_factory(sponsor=sponsor, league=league)
        away_team = team_factory(sponsor=sponsor, league=league)
        game = game_factory(
            home_team=home_team,
            away_team=away_team,
            league=league,
            division=division,
        )

        response = client.delete(
            url_for("rest.game", game_id=game.id),
            follow_redirects=True
        )
        assert response.status_code == 200
        assert not Game.does_game_exist(game.id)


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
def test_get_all_games(mlsb_app, client):
    with mlsb_app.app_context():
        response = client.get(
            url_for("rest.games"),
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
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('game_factory')
def test_get_game(
    mlsb_app,
    client,
    sponsor_factory,
    team_factory,
    league_factory,
    division_factory,
    game_factory
):
    with mlsb_app.app_context():
        division = division_factory()
        league = league_factory()
        sponsor = sponsor_factory()
        home_team = team_factory(sponsor=sponsor, league=league)
        away_team = team_factory(sponsor=sponsor, league=league)
        game = game_factory(
            home_team=home_team,
            away_team=away_team,
            league=league,
            division=division,
        )

        response = client.get(
            url_for("rest.game", game_id=game.id),
            follow_redirects=True
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['home_team'] == str(home_team)
        assert data['away_team'] == str(away_team)
