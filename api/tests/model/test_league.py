import pytest
from api.errors import InvalidField
from api.model import League


@pytest.mark.parametrize("league_data", [
    ("Some league", ),
])
@pytest.mark.usefixtures('mlsb_app')
def test_create_league(mlsb_app, league_data):
    with mlsb_app.app_context():
        League(name=league_data[0])


@pytest.mark.parametrize("invalid_league_data", [
    (1,),
])
@pytest.mark.usefixtures('mlsb_app')
def test_cannot_create_invalid_league(mlsb_app, invalid_league_data):
    with mlsb_app.app_context():
        with pytest.raises(InvalidField):
            League(name=invalid_league_data[0])


@pytest.mark.parametrize("league_data", [
    ("Some league", ),
])
@pytest.mark.usefixtures('mlsb_app')
def test_update_league(mlsb_app, league_data):
    with mlsb_app.app_context():
        league = League(name="league")
        league.update(league=league_data[0])


@pytest.mark.parametrize("invalid_league_data", [
    (1,),
])
@pytest.mark.usefixtures('mlsb_app')
def test_cannot_update_invalid_league(mlsb_app, invalid_league_data):
    with mlsb_app.app_context():
        with pytest.raises(InvalidField):
            league = League(name="league")
            league.update(league=invalid_league_data[0])
