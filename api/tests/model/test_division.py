import pytest
from api.errors import InvalidField
from api.model import Division


@pytest.mark.parametrize("division_data", [
    ("Some Division", "SD"),
    ("No shortname", None),
])
@pytest.mark.usefixtures('mlsb_app')
def test_create_division(mlsb_app, division_data):
    with mlsb_app.app_context():
        Division(
            name=division_data[0],
            shortname=division_data[1]
        )


@pytest.mark.parametrize("invalid_division_data", [
    (1, "Invalid division name"),
    ("Invalid shortname", 1),
])
@pytest.mark.usefixtures('mlsb_app')
def test_cannot_create_invalid_division(mlsb_app, invalid_division_data):
    with mlsb_app.app_context():
        with pytest.raises(InvalidField):
            Division(
                name=invalid_division_data[0],
                shortname=invalid_division_data[1]
            )


@pytest.mark.parametrize("division_data", [
    ("Some Division", "SD"),
    ("No shortname", None),
    (None, "SD"),
])
@pytest.mark.usefixtures('mlsb_app')
def test_update_division(mlsb_app, division_data):
    with mlsb_app.app_context():
        division = Division(name='Division')
        division.update(
            name=division_data[0],
            shortname=division_data[1]
        )


@pytest.mark.parametrize("invalid_division_data", [
    (1, None),
    (None, 1),
])
@pytest.mark.usefixtures('mlsb_app')
def test_cannot_update_invalid_division(mlsb_app, invalid_division_data):
    with mlsb_app.app_context():
        with pytest.raises(InvalidField):
            Division(
                name=invalid_division_data[0],
                shortname=invalid_division_data[1]
            )


@pytest.mark.parametrize("division_data", [
    ("Division", "SD"),
    ("Division", None),
])
@pytest.mark.usefixtures('mlsb_app')
def test_get_division_shortname(mlsb_app, division_data):
    with mlsb_app.app_context():
        division = Division(
            name=division_data[0],
            shortname=division_data[1]
        )
        shortname = division.get_shortname()
        expect = division_data[1] if division_data[1] else division_data[0]
        assert shortname == expect, "Short name did not match"
