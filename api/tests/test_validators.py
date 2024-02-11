import pytest
from api.validators import gender_validator, boolean_validator, \
    string_validator, year_validator, int_validator, float_validator, \
    date_validator, time_validator, rbi_validator, hit_validator, \
    inning_validator, field_validator
from api.variables import BATS, FIELDS
from datetime import date


@pytest.mark.functional
@pytest.mark.parametrize("valid_boolean", [
    True,
    False,
    "True",
    "False",
])
def test_boolean_validator_valid(valid_boolean):
    assert boolean_validator(valid_boolean) is True


@pytest.mark.functional
@pytest.mark.parametrize("invalid_boolean", [
    "TrueX",
    "FalseX",
    1
])
def test_boolean_validator_invalid(invalid_boolean):
    assert boolean_validator(invalid_boolean) is False


@pytest.mark.functional
@pytest.mark.parametrize("valid_string", [
    "SomeString",
    "one"
])
def test_string_validator_valid(valid_string):
    assert string_validator(valid_string) is True


@pytest.mark.functional
@pytest.mark.parametrize("invalid_string", [
    "1"
])
def test_string_validator_invalid(invalid_string):
    assert string_validator(invalid_string) is False


@pytest.mark.functional
@pytest.mark.parametrize("valid_year", [
    2016,
    date.today().year,
    "2016"
])
def test_year_validator_valid(valid_year):
    assert year_validator(valid_year) is True


@pytest.mark.functional
@pytest.mark.parametrize("invalid_year", [
    1999,
    "1999",
    date.today().year + 1,
    "X",
    str(date.today().year + 1)
])
def test_year_validator_invalid(invalid_year):
    assert year_validator(invalid_year) is False


@pytest.mark.functional
@pytest.mark.parametrize("valid_int", [
    1,
    "2",
])
def test_int_validator_valid(valid_int):
    assert int_validator(valid_int) is True


@pytest.mark.functional
@pytest.mark.parametrize("invalid_int", [
    -1,
    "X"
])
def test_int_validator_invalid(invalid_int):
    assert int_validator(invalid_int) is False


@pytest.mark.functional
@pytest.mark.parametrize("valid_float", [
    1.0,
    "2.0",
])
def test_float_validator_valid(valid_float):
    assert float_validator(valid_float) is True


@pytest.mark.functional
@pytest.mark.parametrize("invalid_float", [
    -1.,
    "X"
])
def test_float_validator_invalid(invalid_float):
    assert float_validator(invalid_float) is False


@pytest.mark.functional
@pytest.mark.parametrize("invalid_gender", [
    "",
    1,
    "X"
])
def test_gender_validator_invalid(invalid_gender):
    assert gender_validator(invalid_gender) is False


@pytest.mark.functional
@pytest.mark.parametrize("valid_gender", [
    "f",
    "F",
    "m",
    "M",
    "t",
    "T"
])
def test_gender_validator(valid_gender):
    assert gender_validator(valid_gender) is True


@pytest.mark.functional
@pytest.mark.parametrize("invalid_date", [
    "X",
    "1",
    "10-01-2023"
])
def test_date_validator_invalid(invalid_date):
    assert date_validator(invalid_date) is False


@pytest.mark.functional
@pytest.mark.parametrize("valid_date", [
    "2023-10-01",
    "2024-01-01"
])
def test_date_validator(valid_date):
    assert date_validator(valid_date) is True


@pytest.mark.functional
@pytest.mark.parametrize("invalid_time", [
    "X",
    "1",
    "25:61"
])
def test_time_validator_invalid(invalid_time):
    assert time_validator(invalid_time) is False


@pytest.mark.functional
@pytest.mark.parametrize("valid_time", [
    "12:01",
    "23:59"
])
def test_time_validator(valid_time):
    assert time_validator(valid_time) is True


@pytest.mark.functional
@pytest.mark.parametrize("invalid_rbi", [
    5,
    "5",
    -1
])
def test_rbi_validator_invalid(invalid_rbi):
    assert rbi_validator(invalid_rbi) is False


@pytest.mark.functional
@pytest.mark.parametrize("valid_rbi", [
    0,
    1,
    2,
    3,
    4,
    "0",
    "1",
    "2",
    "3",
    "4"
])
def test_rbi_validator(valid_rbi):
    assert rbi_validator(valid_rbi) is True


@pytest.mark.functional
@pytest.mark.parametrize("invalid_hit", [
    "X",
    "1",
    "XX",
    "HRX"
])
def test_hit_validator_invalid(invalid_hit):
    assert hit_validator(invalid_hit) is False


@pytest.mark.functional
def test_hit_validator_ss_only_eligble():
    assert hit_validator("SS", gender="m") is False


@pytest.mark.functional
@pytest.mark.parametrize("valid_hit", BATS)
def test_hit_validator(valid_hit):
    assert hit_validator(valid_hit, gender="f") is True


@pytest.mark.functional
@pytest.mark.parametrize("invalid_inning", [
    "X",
    "0",
    "XX"
])
def test_inning_validator_invalid(invalid_inning):
    assert inning_validator(invalid_inning) is False


@pytest.mark.functional
@pytest.mark.parametrize("valid_inning", [
    1,
    "1",
    2,
    "2"
])
def test_inning_validator(valid_inning):
    assert inning_validator(valid_inning) is True


@pytest.mark.functional
@pytest.mark.parametrize("invalid_field", [
    "WP5",
    "1",
    "Hillside Central",
    1
])
def test_field_validator_invalid(invalid_field):
    assert field_validator(invalid_field) is False


@pytest.mark.functional
@pytest.mark.parametrize(
    "valid_field",
    FIELDS + ["wp1", "wp2", "hillside lower"]
)
def test_field_validator(valid_field):
    assert field_validator(valid_field) is True
