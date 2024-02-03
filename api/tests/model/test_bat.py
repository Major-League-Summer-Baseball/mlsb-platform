import pytest
from api.errors import GameDoesNotExist, InvalidField, \
    PlayerDoesNotExist, TeamDoesNotExist
from api.model import Bat

INVALID_ENTITY = -1


@pytest.mark.parametrize("bat_data", [
    ("S", 9, 0),
    ("S", 9, 1),
    ("HR", 1, 4),
    ("HR", 1, 1),
    ("D", 9, 2),
    ("D", 9, 1),
    ("T", 9, 1),
    ("K", 9, 0),
])
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
@pytest.mark.usefixtures('player_factory')
def test_create_bat(
    mlsb_app,
    bat_data,
    league_factory,
    division_factory,
    team_factory,
    game_factory,
    player_factory
):
    with mlsb_app.app_context():
        player = player_factory()
        player_team = team_factory(players=[player])
        game = game_factory(
            home_team=player_team,
            away_team=team_factory(),
            league=league_factory(),
            division=division_factory()
        )
        Bat(
            player_id=player.id,
            team_id=player_team.id,
            game_id=game.id,
            classification=bat_data[0],
            inning=bat_data[1],
            rbi=bat_data[2]
        )


@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
@pytest.mark.usefixtures('player_factory')
def test_nonexistent_player_cannot_bat(
    mlsb_app,
    league_factory,
    division_factory,
    team_factory,
    game_factory,
    player_factory
):
    with mlsb_app.app_context():
        player = player_factory()
        player_team = team_factory(players=[player])
        game = game_factory(
            home_team=player_team,
            away_team=team_factory(),
            league=league_factory(),
            division=division_factory()
        )
        with pytest.raises(PlayerDoesNotExist):
            Bat(
                player_id=INVALID_ENTITY,
                team_id=player_team.id,
                game_id=game.id,
                classification="S",
            )
        bat = Bat(
            player_id=player.id,
            team_id=player_team.id,
            game_id=game.id,
            classification="S",
        )
        with pytest.raises(PlayerDoesNotExist):
            bat.update(player_id=INVALID_ENTITY)


@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
@pytest.mark.usefixtures('player_factory')
def test_nonexistent_team_cannot_have_bats(
    mlsb_app,
    league_factory,
    division_factory,
    team_factory,
    game_factory,
    player_factory
):
    with mlsb_app.app_context():
        player = player_factory()
        player_team = team_factory(players=[player])
        game = game_factory(
            home_team=player_team,
            away_team=team_factory(),
            league=league_factory(),
            division=division_factory()
        )
        with pytest.raises(TeamDoesNotExist):
            Bat(
                player_id=player.id,
                team_id=INVALID_ENTITY,
                game_id=game.id,
                classification="S",
            )
        bat = Bat(
            player_id=player.id,
            team_id=player_team.id,
            game_id=game.id,
            classification="S",
        )
        with pytest.raises(TeamDoesNotExist):
            bat.update(team_id=INVALID_ENTITY)


@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
@pytest.mark.usefixtures('player_factory')
def test_nonexistent_game_cannot_have_bats(
    mlsb_app,
    league_factory,
    division_factory,
    team_factory,
    game_factory,
    player_factory
):
    with mlsb_app.app_context():
        player = player_factory()
        player_team = team_factory(players=[player])
        game = game_factory(
            home_team=player_team,
            away_team=team_factory(),
            league=league_factory(),
            division=division_factory()
        )
        with pytest.raises(GameDoesNotExist):
            Bat(
                player_id=player.id,
                team_id=player_team.id,
                game_id=INVALID_ENTITY,
                classification="S",
            )
        bat = Bat(
            player_id=player.id,
            team_id=player_team.id,
            game_id=game.id,
            classification="S",
        )
        with pytest.raises(GameDoesNotExist):
            bat.update(game_id=INVALID_ENTITY)


@pytest.mark.parametrize("invalid_bat_data", [
    ("X", 9, 0),
    ("S", -1, 1),
    ("HR", 1, -1),
    ("HR", "X", 1),
    ("D", 9, "X")
])
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
@pytest.mark.usefixtures('player_factory')
def test_create_invalid_bat(
    mlsb_app,
    invalid_bat_data,
    league_factory,
    division_factory,
    team_factory,
    game_factory,
    player_factory
):
    with mlsb_app.app_context():
        player = player_factory()
        player_team = team_factory(players=[player])
        game = game_factory(
            home_team=player_team,
            away_team=team_factory(),
            league=league_factory(),
            division=division_factory()
        )
        with pytest.raises(InvalidField):
            Bat(
                player_id=player.id,
                team_id=player_team.id,
                game_id=game.id,
                classification=invalid_bat_data[0],
                inning=invalid_bat_data[1],
                rbi=invalid_bat_data[2]
            )


@pytest.mark.parametrize("bat_data", [
    (None, 9, None),
    (None, None, 4),
])
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
@pytest.mark.usefixtures('player_factory')
def test_update_bat(
    mlsb_app,
    bat_data,
    league_factory,
    division_factory,
    team_factory,
    game_factory,
    player_factory
):
    with mlsb_app.app_context():
        player = player_factory()
        player_team = team_factory(players=[player])
        game = game_factory(
            home_team=player_team,
            away_team=team_factory(),
            league=league_factory(),
            division=division_factory()
        )
        bat = Bat(
            player_id=player.id,
            team_id=player_team.id,
            game_id=game.id,
            classification="FO",
        )
        bat.update(
            inning=bat_data[1],
            rbi=bat_data[2]
        )
        if bat_data[1] is not None:
            assert bat.inning == bat_data[1]
        if bat_data[2] is not None:
            assert bat.rbi == bat_data[2]


@pytest.mark.parametrize("invalid_bat_data", [
    (None, "X", None),
    (None, -1, None),
    (None, None, 100),
    (None, None, "X"),
])
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
@pytest.mark.usefixtures('player_factory')
def test_cannot_update_invalid_bat(
    mlsb_app,
    invalid_bat_data,
    league_factory,
    division_factory,
    team_factory,
    game_factory,
    player_factory
):
    with mlsb_app.app_context():
        player = player_factory()
        player_team = team_factory(players=[player])
        game = game_factory(
            home_team=player_team,
            away_team=team_factory(),
            league=league_factory(),
            division=division_factory()
        )
        bat = Bat(
            player_id=player.id,
            team_id=player_team.id,
            game_id=game.id,
            classification="FO",
        )
        with pytest.raises(InvalidField):
            bat.update(
                inning=invalid_bat_data[1],
                rbi=invalid_bat_data[2]
            )

@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
@pytest.mark.usefixtures('player_factory')
def test_cannot_update_bat_type(
    mlsb_app,
    league_factory,
    division_factory,
    team_factory,
    game_factory,
    player_factory
):
    with mlsb_app.app_context():
        player = player_factory()
        player_team = team_factory(players=[player])
        game = game_factory(
            home_team=player_team,
            away_team=team_factory(),
            league=league_factory(),
            division=division_factory()
        )
        bat = Bat(
            player_id=player.id,
            team_id=player_team.id,
            game_id=game.id,
            classification="FO",
        )
        bat.update(
            hit="S",
        )

@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
@pytest.mark.usefixtures('player_factory')
def test_sum_bats_rbis(
    mlsb_app,
    league_factory,
    division_factory,
    team_factory,
    game_factory,
    player_factory
):
    with mlsb_app.app_context():
        player = player_factory()
        player_team = team_factory(players=[player])
        game = game_factory(
            home_team=player_team,
            away_team=team_factory(),
            league=league_factory(),
            division=division_factory()
        )
        first_bat = Bat(
            player_id=player.id,
            team_id=player_team.id,
            game_id=game.id,
            classification="S",
            rbi=1
        )
        second_bat = Bat(
            player_id=player.id,
            team_id=player_team.id,
            game_id=game.id,
            classification="HR",
            rbi=2
        )
        combined = first_bat + second_bat
        assert combined == 3
