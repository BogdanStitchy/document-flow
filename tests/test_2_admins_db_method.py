from pydantic import ValidationError
from sqlalchemy import create_engine
import pytest
import os

from sqlalchemy.exc import IntegrityError

from src.db.models import base
from src.db.methods import admin_db_methods
from src.db.database_setup import set_new_engine

data_base_local = "sqlite:///B:/работа/проекты с работы/document_flow/tests/testDB.db"
data_base_memory = "sqlite:///:memory:"


@pytest.fixture(scope="module")
def database_admin():
    # engine = create_engine(data_base_memory)
    # set_new_engine(engine)
    admin_methods = admin_db_methods.AdminDB()
    yield admin_methods


@pytest.mark.parametrize("data, expected_exception", [
    (("userov", "user", "userovich", "user_login", os.urandom(16), os.urandom(16), 1, 1), None),
    (("usr", "user1", "usr", "usr_log", os.urandom(16), os.urandom(16), 3, 3), None),
    ((1, {}, "asdf", "asdf", os.urandom(16), os.urandom(16), 1, 6), ValidationError),
    (("asdf", "sdf", (1, 2), "sdfg", os.urandom(16), os.urandom(16), 7, 9), ValidationError),
    ((None, "sd", "hhgfgh", "dfgh", os.urandom(16), os.urandom(16), 1), ValidationError),
    (("None", "sdaf", None, "asdf", os.urandom(16), os.urandom(16), 1), ValidationError)
])
def test_add_user(database_admin, data, expected_exception):
    if expected_exception is None:
        id_added_user = database_admin.add_user(*data)
        assert type(id_added_user) == int
    else:
        with pytest.raises(expected_exception):
            database_admin.add_user(*data)


def test_remaining_user(database_admin):
    data = ("uniq", "uniq", "uniq", "uniq_usr_log", os.urandom(16), os.urandom(16), 1, 1)
    database_admin.add_user(*data)
    with pytest.raises(IntegrityError):
        database_admin.add_user(*data)
