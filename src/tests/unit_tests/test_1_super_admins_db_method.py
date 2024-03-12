from pydantic import ValidationError
import pytest
import os
import datetime
from sqlalchemy.exc import IntegrityError

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
def test_good_add_admin(db_methods_super_admin, data, expected_exception, create_database, clean_admins_table_database):
    if expected_exception is None:
        id_added_admin = db_methods_super_admin.add_admin(*data)
        assert type(id_added_admin) == int
    else:
        with pytest.raises(expected_exception):
            db_methods_super_admin.add_admin(*data)


def test_re_add_admin(db_methods_super_admin):
    db_methods_super_admin.add_admin(*__data_successfully_added_admins_for_tests[2])
    with pytest.raises(IntegrityError):
        db_methods_super_admin.add_admin(*__data_successfully_added_admins_for_tests[2])


@pytest.mark.parametrize("data, expected_exception", [
    (1, None),
    (2, None),
    ("string", ValidationError),
    ((1, 2, 3), ValidationError),
    (15, ValueError)
])
def test_change_active_status_admin(db_methods_super_admin, data, expected_exception):
    if expected_exception is None:
        admin_before_change = db_methods_super_admin.get_one_admin(data)
        db_methods_super_admin.change_admin_activity_status(data)
        admin_after_change = db_methods_super_admin.get_one_admin(data)
        assert admin_before_change.active != admin_after_change.active
    else:
        with pytest.raises(expected_exception):
            db_methods_super_admin.change_admin_activity_status(data)


@pytest.mark.parametrize("id_admin, kwargs_new_data, expected_exception", [
    (1, {"name": "new_admin_name", "last_name": "new_last_name"}, None),
    (2, {"name": "new_admin_name_1", "login": "new_login", "password": os.urandom(16)}, None),
    (3, {"name": "", "salt": os.urandom(16)}, None),
    (3, {"name": "New_new", "login": "new_login"}, IntegrityError),
])
def test_edit_admin(db_methods_super_admin, id_admin, kwargs_new_data, expected_exception):
    if expected_exception is not None:
        with pytest.raises(expected_exception):
            db_methods_super_admin.edit_admin(id_admin, **kwargs_new_data)
        return

    db_methods_super_admin.edit_admin(id_admin, **kwargs_new_data)
    new_user = db_methods_super_admin.get_one_admin(id_admin)
    for key, update_value in kwargs_new_data.items():
        if update_value != "" and update_value is not None:
            assert update_value == new_user[key]
        else:
            assert new_user[key] is not None and new_user[key] != ''


def test_get_all_admins(db_methods_super_admin):
    admins = db_methods_super_admin.get_all_admins()
    print(f"\n\n{admins}\n\n")
    assert len(admins) == len(__data_successfully_added_admins_for_tests) #+ 3 # +3 потому что фикстурой еще три добавляется


def test_good_find_admins_period(db_methods_super_admin):
    start_date = datetime.datetime.strptime("01.01.2021", "%d.%m.%Y")
    end_date = datetime.datetime.strptime("01.01.2022", "%d.%m.%Y")
    new_date = datetime.datetime.strptime("01.05.2021", "%d.%m.%Y")

    db_methods_super_admin.edit_admin(1, date_creating=new_date)
    res = db_methods_super_admin.find_admins_period(start_date, end_date)
    assert len(res) == 1


def test_broke_find_admins_period(db_methods_super_admin):
    new_date = datetime.datetime.strptime("01.05.2021", "%d.%m.%Y")
    db_methods_super_admin.edit_admin(1, date_creating=new_date)
    with pytest.raises(ValidationError):
        db_methods_super_admin.find_admins_period("01.05.2021", "01.05.2025")


def test_find_admins_word(db_methods_super_admin):
    find_string = "new_admin_name_1"
    res = db_methods_super_admin.find_admins_words(find_string)
    assert len(res) == 1


@pytest.mark.parametrize("data, expected_exception", [
    (("", ""), ValidationError),
    ((1, 1), ValidationError),
])
def test_add_department_broke(db_methods_super_admin, data, expected_exception):
    with pytest.raises(expected_exception):
        db_methods_super_admin.add_admin(*data)


def test_add_department_good(clean_departments_table_database, db_methods_super_admin):
    data = [("dep1", 100), ("dep2", 200), ("dep3", 300), ("dep4", 400), ]
    for dt in data:
        db_methods_super_admin.add_department(*dt)
    departments = db_methods_super_admin.get_all_departments()
    assert len(departments) == 4


@pytest.mark.parametrize("data, expected_exception", [
    (("", ""), ValidationError),
    ((1, 1), ValueError),
])
def test_add_hierarchy_department_broke(db_methods_super_admin, data, expected_exception):
    with pytest.raises(expected_exception):
        db_methods_super_admin.add_one_hierarchy_department(*data)


def test_add_hierarchy_department_good(db_methods_super_admin):
    data = [(2, 1), (3, 1), (4, 3)]
    for dt in data:
        db_methods_super_admin.add_one_hierarchy_department(*dt)
    hierarchy_departments = db_methods_super_admin.get_full_hierarchy_departments()
    assert len(hierarchy_departments) == 3


def test_delete_department(db_methods_super_admin):
    id_departments_for_delete = [2, 4]
    db_methods_super_admin.delete_departments(id_departments_for_delete)
    departments_after_delete = db_methods_super_admin.get_all_departments()
    assert len(departments_after_delete) == 2
