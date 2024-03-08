from pydantic import ValidationError
import pytest
import os
from sqlalchemy.exc import IntegrityError

from src.db.methods import super_admin_db_methods as sa_methods


@pytest.fixture(scope="module")
def database_sa():
    super_admin_methods = sa_methods.SuperAdminMethodsDB()
    yield super_admin_methods


# Успешно добавленных админов нужно вносить в эту переменную
__data_successfully_added_admins_for_tests = (
    ("admin", "adminovich", "adminov", "admin_login", os.urandom(16), os.urandom(16)),
    ("admin1", "admh", "adv", "admin_login1", os.urandom(16), os.urandom(16)),
    ("rem", "rem", "rem", "rem", os.urandom(16), os.urandom(16))
)


@pytest.mark.parametrize("data, expected_exception", [
    (__data_successfully_added_admins_for_tests[0], None),
    (__data_successfully_added_admins_for_tests[1], None),
    ((1, {}, "adminov", "admin_login", os.urandom(16), os.urandom(16)), ValidationError),
    (("admin1", "adminovich1", (1, 2), "admin_login1", os.urandom(16), os.urandom(16)), ValidationError),
    ((None, "sd", "adminov", "admin_login", os.urandom(16), os.urandom(16)), ValidationError),
    (("None", "sd", None, "admin_login", os.urandom(16), os.urandom(16)), ValidationError)
])
def test_good_add_admin(database_sa, data, expected_exception, create_database):
    if expected_exception is None:
        id_added_admin = database_sa.add_admin(*data)
        assert type(id_added_admin) == int
    else:
        with pytest.raises(expected_exception):
            database_sa.add_admin(*data)


def test_re_add_admin(database_sa):
    database_sa.add_admin(*__data_successfully_added_admins_for_tests[2])
    with pytest.raises(IntegrityError):
        database_sa.add_admin(*__data_successfully_added_admins_for_tests[2])


@pytest.mark.parametrize("data, expected_exception", [
    (("dep1", 1), None),
    (("dep2", 2), None),
    (("dep3", 3), None),
    (("dep4", 4), None),
    (("", ""), ValidationError),
    ((1, 1), ValidationError),
])
def test_add_department(database_sa, data, expected_exception):
    if expected_exception is None:
        database_sa.add_department(*data)
    else:
        with pytest.raises(expected_exception):
            database_sa.add_admin(*data)


@pytest.mark.parametrize("data, expected_exception", [
    (1, None),
    (2, None),
    ("string", ValidationError),
    ((1, 2, 3), ValidationError),
    (5, ValueError)
])
def test_change_active_status_admin(database_sa, data, expected_exception):
    if expected_exception is None:
        admin_before_change = database_sa.get_one_admin(data)
        database_sa.change_admin_activity_status(data)
        admin_after_change = database_sa.get_one_admin(data)
        assert admin_before_change.active != admin_after_change.active
    else:
        with pytest.raises(expected_exception):
            database_sa.change_admin_activity_status(data)


@pytest.mark.parametrize(
    "id_admin, kwargs_new_data, expected_exception",
    [
        (1, {"name": "new_admin_name", "last_name": "new_last_name"}, None),
        (2, {"name": "new_admin_name_1", "login": "new_login", "password": os.urandom(16)}, None),
        (3, {"name": "", "salt": os.urandom(16)}, None),
        (3, {"name": "New_new", "login": "new_login"}, IntegrityError),
    ])
def test_edit_admin(database_sa, id_admin, kwargs_new_data, expected_exception):
    if expected_exception is not None:
        with pytest.raises(expected_exception):
            database_sa.edit_admin(id_admin, **kwargs_new_data)
        return

    database_sa.edit_admin(id_admin, **kwargs_new_data)
    new_user = database_sa.get_one_admin(id_admin)
    for key, update_value in kwargs_new_data.items():
        if update_value != "" and update_value is not None:
            assert update_value == new_user[key]
        else:
            assert new_user[key] is not None and new_user[key] != ''


def test_get_all_admins(database_sa):
    admins = database_sa.get_all_admins()
    assert len(admins) == len(__data_successfully_added_admins_for_tests)
