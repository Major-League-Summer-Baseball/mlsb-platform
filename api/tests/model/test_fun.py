import pytest
from api.model import Fun
from datetime import date


@pytest.mark.usefixtures('mlsb_app')
def test_created_fun_this_year(mlsb_app):
    with mlsb_app.app_context():
        fun = Fun()
        assert fun.count == 0, "Fun count defaults zero"
        assert fun.year == date.today().year, "Fun defaults to this year"


@pytest.mark.usefixtures('mlsb_app')
def test_update_fun_count(mlsb_app):
    with mlsb_app.app_context():
        fun = Fun()
        fun.update(10)
        assert fun.count == 10, "Able to update fun count"


@pytest.mark.usefixtures('mlsb_app')
def test_increment_fun_count(mlsb_app):
    with mlsb_app.app_context():
        fun = Fun()
        fun.increment(10)
        fun.increment(10)
        assert fun.count == 20, "Able to increment fun count"
