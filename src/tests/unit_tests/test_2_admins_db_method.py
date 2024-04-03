from pydantic import ValidationError
import pytest
import os
import datetime
from sqlalchemy.exc import IntegrityError


@pytest.mark.parametrize("data, expected_exception", [
    (("userov", "user", "userovich", "user_login", os.urandom(16), os.urandom(16), 1, 1), None),
    (("usr", "user1", "usr", "usr_log", os.urandom(16), os.urandom(16), 3, 3), None),
    ((1, {}, "asdf", "asdf", os.urandom(16), os.urandom(16), 1, 6), ValidationError),
    (("asdf", "sdf", (1, 2), "sdfg", os.urandom(16), os.urandom(16), 7, 9), ValidationError),
    ((None, "sd", "hhgfgh", "dfgh", os.urandom(16), os.urandom(16), 1), ValidationError),
    (("None", "sdaf", None, "asdf", os.urandom(16), os.urandom(16), 1), ValidationError)
])
def test_add_user(setup_test_2_admins_db_method, database_admin, data, expected_exception):
    if expected_exception is None:
        id_added_user = database_admin.add_user_db(*data)
        assert type(id_added_user) == int
    else:
        with pytest.raises(expected_exception):
            database_admin.add_user_db(*data)


def test_remaining_user(database_admin):
    data = ("uniq", "uniq", "uniq", "uniq_usr_log", os.urandom(16), os.urandom(16), 1, 1)
    database_admin.add_user_db(*data)
    with pytest.raises(IntegrityError):
        database_admin.add_user_db(*data)


def test_get_all_users(database_admin):
    users = database_admin.get_all_users()
    assert len(users) == 3  # сколько раз добавляем в тестах


def test_get_one_user(database_admin):
    user1 = database_admin.get_one_user(1)
    assert len(user1) == 12


def test_find_admins_word(database_admin):
    find_string = "userov"
    res = database_admin.find_users_words(find_string)
    assert len(res) == 1


def test_good_find_admins_period(database_admin):
    start_date = datetime.datetime.strptime("01.01.2021", "%d.%m.%Y")
    end_date = datetime.datetime.strptime("01.01.2022", "%d.%m.%Y")
    new_date = datetime.datetime.strptime("01.05.2021", "%d.%m.%Y")

    database_admin.edit_user(1, date_creating=new_date)
    res = database_admin.find_users_period(start_date, end_date)
    assert len(res) == 1


def test_broke_find_admins_period(database_admin):
    new_date = datetime.datetime.strptime("01.05.2021", "%d.%m.%Y")
    database_admin.edit_user(1, date_creating=new_date)
    with pytest.raises(ValidationError):
        database_admin.find_users_period("01.05.2021", "01.05.2025")


@pytest.mark.parametrize("id_user, kwargs, expected_exception", [
    (1, {"name": "Dima", "last_name": "Ivanov"}, None),
    (2, {"name": "Stas"}, None),
    (3, {"name": ""}, None),
    (1, (123, 234), TypeError),
    (5, {"name": "Test"}, ValueError)
])
def test_update_user(database_admin, id_user, kwargs, expected_exception):
    if expected_exception is None:
        database_admin.edit_user(id_user, **kwargs)
        new_user = database_admin.get_one_user(id_user)
        for key, update_value in kwargs.items():
            if update_value != "" and update_value is not None:
                assert update_value == new_user[key]
            else:
                assert new_user[key] is not None and new_user[key] != ''
    else:
        with pytest.raises(expected_exception):
            database_admin.edit_user(id_user, **kwargs)


@pytest.mark.parametrize("data, expected_exception", [
    (1, None),
    (2, None),
    ("string", ValidationError),
    ((1, 2, 3), ValidationError),
    (5, ValueError)
])
def test_change_active_status_user(database_admin, data, expected_exception):
    if expected_exception is None:
        user_before_change = database_admin.get_one_user(data)
        database_admin.change_user_activity_status(data)
        user_after_change = database_admin.get_one_user(data)
        assert user_before_change.active != user_after_change.active
    else:
        with pytest.raises(expected_exception):
            database_admin.change_user_activity_status(data)
