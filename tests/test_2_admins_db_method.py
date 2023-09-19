from pydantic import ValidationError
import pytest
import os
from sqlalchemy.exc import IntegrityError

from src.db.methods import admin_db_methods


@pytest.fixture(scope="module")
def database_admin():
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


def test_get_all_users(database_admin):
    users = database_admin.get_all_users()
    assert len(users) == 3  # сколько раз добавляем в тестах


def test_get_one_user(database_admin):
    user1 = database_admin.get_one_user(1)
    assert len(user1) == 12


@pytest.mark.parametrize("id_user, kwargs, expected_exception", [
    (1, {"name": "Dima", "last_name": "Ivanov"}, None),
    (2, {"name": "Stas"}, None),
    (3, {"name": ""}, None),
    (1, (123, 234), TypeError),
    (5, {"name": "Test"}, ValueError)
])
def test_update_user(database_admin, id_user, kwargs, expected_exception):
    if expected_exception is None:
        database_admin.update_user(id_user, **kwargs)
        new_user = database_admin.get_one_user(id_user)
        for key, update_value in kwargs.items():
            if update_value != "" and update_value is not None:
                assert update_value == new_user[key]
            else:
                assert new_user[key] is not None and new_user[key] != ''
    else:
        with pytest.raises(expected_exception):
            database_admin.update_user(id_user, **kwargs)


@pytest.mark.parametrize("id_document, kwargs, expected_exception", [
    (1, {"inner_number": "", "output_number": "", "output_date": "", "type_document": "", "name": ""}, None),
    (2, {"inner_number": "", "output_number": "", "output_date": "", "type_document": "", "name": ""}, None),
    # (3, {"inner_number": "", "output_number": "", "output_date": "", "type_document": "", "name": ""}, None),
    (1, (123, 234), TypeError),
    (2, {"linner": "Test"}, ValueError)
])
def test_update_document(database_admin, id_document, kwargs, expected_exception):
    if expected_exception is None:
        database_admin.update_document(id_document, **kwargs)
        # new_document = database_admin.get_one_user(id_user)
        # for key, update_value in kwargs.items():
        #     if update_value != "" and update_value is not None:
        #         assert update_value == new_user[key]
        #     else:
        #         assert new_user[key] is not None and new_user[key] != ''
    else:
        with pytest.raises(expected_exception):
            database_admin.update_document(id_document, **kwargs)
