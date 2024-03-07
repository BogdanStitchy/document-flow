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
    "id_admin, old_data_admin, new_name, new_login, new_password, new_salt",
    [
        (1, __data_successfully_added_admins_for_tests[0], "new_name", "new_login", os.urandom(16), os.urandom(16)),
        (2, __data_successfully_added_admins_for_tests[1], "new_name1", "new_login1", None, None),
    ])
def test_edit_admin(id_admin, database_sa, old_data_admin, new_name, new_login, new_password, new_salt):
    if new_password:
        database_sa.edit_admin_data(id_admin=id_admin, name=new_name, login=new_login, patronymic=old_data_admin[1],
                                    last_name=old_data_admin[2], password=new_password, salt=new_salt)
    else:
        database_sa.edit_admin_data(id_admin=id_admin, name=new_name, login=new_login, patronymic=old_data_admin[1],
                                    last_name=old_data_admin[2])

    edited_admin = database_sa.get_one_admin(id_admin)

    assert (edited_admin.login == new_login and
            edited_admin.name == new_name and
            edited_admin.last_name == old_data_admin[2] and
            edited_admin.patronymic == old_data_admin[1]
            )
    if new_password is None:
        assert (edited_admin.password == old_data_admin[4] and
                edited_admin.salt == old_data_admin[5])


def test_get_all_admins(database_sa):
    admins = database_sa.get_all_admins()
    assert len(admins) == len(__data_successfully_added_admins_for_tests)
