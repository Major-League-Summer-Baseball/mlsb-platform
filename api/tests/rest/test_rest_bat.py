import pytest
from flask import url_for
from datetime import datetime
from api.model import Game, split_datetime, Bat
from api.helper import loads


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('admin_header')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('game_factory')
def test_able_create_bat(
    mlsb_app,
    client,
    admin_header,
    sponsor_factory,
    team_factory,
    league_factory,
    division_factory,
    player_factory,
    game_factory
):
    with mlsb_app.app_context():
        player = player_factory()
        division = division_factory()
        league = league_factory()
        sponsor = sponsor_factory()
        home_team = team_factory(
            sponsor=sponsor, league=league, players=[player]
        )
        away_team = team_factory(sponsor=sponsor, league=league)
        game = game_factory(
            home_team=home_team,
            away_team=away_team,
            league=league,
            division=division
        )
        hit = "s"
        rbi = 1

        response = client.post(
            url_for("rest.bats"),
            json={
                "game_id": game.id,
                "player_id": player.id,
                "team_id": home_team.id,
                "hit": hit,
                "rbi": rbi,

            },
            follow_redirects=True,
            headers=admin_header
        )

        print(response.data)
        assert response.status_code == 200
        data = loads(response.data)
        assert data['game_id'] == game.id
        assert data['player_id'] == player.id
        assert data['team_id'] == home_team.id
        assert data['hit'] == hit
        assert data['rbi'] == rbi
        assert isinstance(data['bat_id'], int) is True
        assert Bat.does_bat_exist(data['bat_id'])


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('admin_header')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('game_factory')
def test_required_fields_of_bat(
    mlsb_app,
    client,
    admin_header,
    sponsor_factory,
    team_factory,
    league_factory,
    division_factory,
    player_factory,
    game_factory
):
    with mlsb_app.app_context():
        player = player_factory()
        division = division_factory()
        league = league_factory()
        sponsor = sponsor_factory()
        home_team = team_factory(
            sponsor=sponsor, league=league, players=[player]
        )
        away_team = team_factory(sponsor=sponsor, league=league)
        game = game_factory(
            home_team=home_team,
            away_team=away_team,
            league=league,
            division=division
        )
        hit = "S"
        rbi = 1

        response = client.post(
            url_for("rest.bats"),
            json={
                "player_id": player.id,
                "team_id": home_team.id,
                "hit": hit,
                "rbi": rbi,
            },
            follow_redirects=True,
            headers=admin_header
        )
        assert response.status_code == 400

        response = client.post(
            url_for("rest.games"),
            json={
                "game_id": game.id,
                "team_id": home_team.id,
                "hit": hit,
                "rbi": rbi,
            },
            follow_redirects=True,
            headers=admin_header
        )
        assert response.status_code == 400

        response = client.post(
            url_for("rest.games"),
            json={
                "game_id": game.id,
                "player_id": player.id,
                "hit": hit,
                "rbi": rbi,
            },
            follow_redirects=True,
            headers=admin_header
        )
        assert response.status_code == 400

        response = client.post(
            url_for("rest.games"),
            json={
                "game_id": game.id,
                "player_id": player.id,
                "team_id": home_team.id,
                "rbi": rbi,
            },
            follow_redirects=True,
            headers=admin_header
        )
        assert response.status_code == 400


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('admin_header')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('game_factory')
@pytest.mark.usefixtures('bat_factory')
def test_update_bat(
    mlsb_app,
    client,
    admin_header,
    sponsor_factory,
    team_factory,
    league_factory,
    division_factory,
    player_factory,
    game_factory,
    bat_factory,
):
    with mlsb_app.app_context():
        player = player_factory()
        division = division_factory()
        league = league_factory()
        sponsor = sponsor_factory()
        home_team = team_factory(
            sponsor=sponsor, league=league, players=[player]
        )
        away_team = team_factory(sponsor=sponsor, league=league)
        game = game_factory(
            home_team=home_team,
            away_team=away_team,
            league=league,
            division=division
        )
        hit = "s"
        rbi = 1
        bat = bat_factory(game, player, home_team)

        response = client.put(
            url_for("rest.bat", bat_id=bat.id),
            json={
                "hit": hit,
                "rbi": rbi,
            },
            follow_redirects=True,
            headers=admin_header
        )

        assert response.status_code == 200
        data = loads(response.data)
        assert data['hit'] == hit
        assert data['rbi'] == rbi


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('admin_header')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('game_factory')
@pytest.mark.usefixtures('bat_factory')
def test_delete_bat(
    mlsb_app,
    client,
    admin_header,
    sponsor_factory,
    team_factory,
    league_factory,
    division_factory,
    player_factory,
    game_factory,
    bat_factory,
):
    with mlsb_app.app_context():
        player = player_factory()
        division = division_factory()
        league = league_factory()
        sponsor = sponsor_factory()
        home_team = team_factory(
            sponsor=sponsor, league=league, players=[player]
        )
        away_team = team_factory(sponsor=sponsor, league=league)
        game = game_factory(
            home_team=home_team,
            away_team=away_team,
            league=league,
            division=division
        )
        bat = bat_factory(game, player, home_team)

        response = client.delete(
            url_for("rest.bat", bat_id=bat.id),
            follow_redirects=True,
            headers=admin_header
        )
        assert response.status_code == 200
        assert not Bat.does_bat_exist(bat.id)


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('admin_header')
def test_get_all_bats(
    mlsb_app,
    client,
    admin_header,
):
    with mlsb_app.app_context():
        response = client.get(
            url_for("rest.bats"),
            follow_redirects=True,
            headers=admin_header
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
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('game_factory')
@pytest.mark.usefixtures('bat_factory')
def test_get_bat(
    mlsb_app,
    client,
    admin_header,
    sponsor_factory,
    team_factory,
    league_factory,
    division_factory,
    player_factory,
    game_factory,
    bat_factory
):
    with mlsb_app.app_context():
        player = player_factory()
        division = division_factory()
        league = league_factory()
        sponsor = sponsor_factory()
        home_team = team_factory(
            sponsor=sponsor, league=league, players=[player]
        )
        away_team = team_factory(sponsor=sponsor, league=league)
        game = game_factory(
            home_team=home_team,
            away_team=away_team,
            league=league,
            division=division
        )
        bat = bat_factory(game, player, home_team)

        response = client.get(
            url_for("rest.bat", bat_id=bat.id),
            follow_redirects=True,
            headers=admin_header
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data == bat.json()
