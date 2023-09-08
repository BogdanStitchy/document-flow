from pydantic import ValidationError
from sqlalchemy import create_engine
import pytest
import os

from sqlalchemy.exc import IntegrityError

from src.db.models import base
from src.db.methods import super_admin_db_methods as sa_methods
from src.db.database_setup import set_new_engine

data_base_local = "sqlite:///B:/работа/проекты с работы/document_flow/tests/testDB.db"
data_base_memory = "sqlite:///:memory:"


@pytest.fixture(scope="module")
def database():
    print("fixture")
    engine = create_engine(data_base_memory)
    base.Base.metadata.create_all(engine)
    set_new_engine(engine)
    super_admin_methods = sa_methods.SuperAdminDB()
    yield super_admin_methods


@pytest.mark.parametrize("data, expected_exception", [
    (("admin", "adminovich", "adminov", "admin_login", os.urandom(16), os.urandom(16)), None),
    (("admin1", "admh", "adv", "admin_login1", os.urandom(16), os.urandom(16)), None),
    ((1, {}, "adminov", "admin_login", os.urandom(16), os.urandom(16)), ValidationError),
    (("admin1", "adminovich1", (1, 2), "admin_login1", os.urandom(16), os.urandom(16)), ValidationError),
    ((None, "sd", "adminov", "admin_login", os.urandom(16), os.urandom(16)), ValidationError),
    (("None", "sd", None, "admin_login", os.urandom(16), os.urandom(16)), ValidationError)
])
def test_good_add_admin(database, data, expected_exception):
    if expected_exception is None:
        id_added_admin = database.add_admin(*data)
        assert type(id_added_admin) == int
    else:
        with pytest.raises(expected_exception):
            database.add_admin(*data)


def test_remaining_admin(database):
    data = ("rem", "rem", "rem", "rem", os.urandom(16), os.urandom(16))
    database.add_admin(*data)
    with pytest.raises(IntegrityError):
        database.add_admin(*data)
