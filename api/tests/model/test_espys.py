import pytest
from api.errors import InvalidField, SponsorDoesNotExist, TeamDoesNotExist
from api.model import Espys, convert_date


@pytest.mark.parametrize("espy_data", [
    ("Some Description", 1.0, 'Receipt Number', '10:00', '2022-10-01'),
])
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('mlsb_app')
def test_create_espy(
    mlsb_app,
    team_factory,
    sponsor_factory,
    espy_data
):
    with mlsb_app.app_context():
        team = team_factory()
        sponsor = sponsor_factory()
        Espys(
            team.id,
            sponsor_id=sponsor.id,
            description=espy_data[0],
            points=espy_data[1],
            receipt=espy_data[2],
            time=espy_data[3],
            date=espy_data[4]
        )


@pytest.mark.parametrize("invalid_espy_data", [
    (1, 1.0, 'Receipt Number', '10:00', '2022-10-01'),
    ("Some description", "bad", 'Receipt Number', '10:00', '2022-10-01'),
    ("Some description", 1.0, 1.0, '10:00', '2022-10-01'),
    ("Some description", 1.0, 'Receipt Number', '99:00', '2022-10-01'),
    ("Some description", 1.0, 'Receipt Number', '10:00', '2022-30-01'),
])
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('mlsb_app')
def test_create_invalid_espy(
    mlsb_app,
    team_factory,
    sponsor_factory,
    invalid_espy_data
):
    with mlsb_app.app_context():
        team = team_factory()
        sponsor = sponsor_factory()
        with pytest.raises(InvalidField):
            Espys(
                team.id,
                sponsor_id=sponsor.id,
                description=invalid_espy_data[0],
                points=invalid_espy_data[1],
                receipt=invalid_espy_data[2],
                time=invalid_espy_data[3],
                date=invalid_espy_data[4]
            )


@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('mlsb_app')
def test_espy_cannot_nonexistent_sponsor(
    mlsb_app,
    team_factory,
):
    with mlsb_app.app_context():
        team = team_factory()
        with pytest.raises(SponsorDoesNotExist):
            Espys(
                team.id,
                sponsor_id=-1
            )


@pytest.mark.usefixtures('mlsb_app')
def test_espy_cannot_nonexistent_team(mlsb_app):
    with mlsb_app.app_context():
        with pytest.raises(TeamDoesNotExist):
            Espys(-1)


@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
def test_add_espys(mlsb_app, team_factory):
    with mlsb_app.app_context():
        team = team_factory()
        espy_one = Espys(team.id, points=1.0)
        espy_two = Espys(team.id, points=2.0)
        assert espy_one + espy_two == 3.0, "Adding two espys"


@pytest.mark.parametrize("espy_data", [
    ("Some Description", None, None, None, None, None),
    (None, 1.0, None, None, None),
    (None, None, 'Receipt Number', None, None),
    (None, None, None, '10:00', '2022-10-01'),
    ("Some Description", 1.0, 'Receipt Number', '10:00', '2022-10-01'),
])
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('sponsor_factory')
def test_update_espy(mlsb_app, team_factory, sponsor_factory, espy_data):
    with mlsb_app.app_context():
        team = team_factory()
        team_two = team_factory()
        sponsor = sponsor_factory()
        espy = Espys(team.id)
        espy.update(
            team_id=team_two.id,
            sponsor_id=sponsor.id,
            description=espy_data[0],
            points=espy_data[1],
            receipt=espy_data[2],
            time=espy_data[3],
            date=espy_data[4]
        )
        assert espy.team_id == team_two.id
        assert espy.sponsor_id == sponsor.id
        if espy_data[0] is not None:
            assert espy.description == espy_data[0]
        if espy_data[1] is not None:
            assert espy.points == espy_data[1]
        if espy_data[2] is not None:
            assert espy.receipt == espy_data[2]
        if espy_data[3] is not None and espy_data[4] is not None:
            assert espy.date == convert_date(espy_data[4], espy_data[3])


@pytest.mark.parametrize("invalid_espy_data", [
    (1, None, None, None, None),
    (None, "bad", None, None, None),
    (None, None, 1.0, None, None),
    (None, None, None, '99:00', None),
    (None, None, None, None, '2022-30-01'),
])
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('sponsor_factory')
def test_update_invalid_espy(
    mlsb_app,
    team_factory,
    sponsor_factory,
    invalid_espy_data
):
    with mlsb_app.app_context():
        team = team_factory()
        team_two = team_factory()
        sponsor = sponsor_factory()
        espy = Espys(team.id)
        with pytest.raises(InvalidField):
            espy.update(
                team_id=team_two.id,
                sponsor_id=sponsor.id,
                description=invalid_espy_data[0],
                points=invalid_espy_data[1],
                receipt=invalid_espy_data[2],
                time=invalid_espy_data[3],
                date=invalid_espy_data[4]
            )


@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
def test_espy_update_cannot_nonexistent_sponsor(mlsb_app, team_factory):
    with mlsb_app.app_context():
        team = team_factory()
        espy = Espys(team.id)
        with pytest.raises(SponsorDoesNotExist):
            espy.update(sponsor_id=-1)


@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
def test_espy_update_cannot_nonexistent_team(mlsb_app, team_factory):
    with mlsb_app.app_context():
        team = team_factory()
        espy = Espys(team.id)
        with pytest.raises(TeamDoesNotExist):
            espy.update(team_id=-1)
