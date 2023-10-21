import pytest

from src.db.methods import admin_db_methods


@pytest.fixture(scope="module")
def database_admin():
    admin_methods = admin_db_methods.AdminMethodsDB()
    yield admin_methods


@pytest.mark.parametrize("id_document, kwargs, expected_exception", [
    (1, {"inner_number": "", "output_number": "", "output_date": "", "type_document": "", "name": ""}, None),
    (2, {"inner_number": "", "output_number": "", "output_date": "", "type_document": "", "name": ""}, None),
    # (3, {"inner_number": "", "output_number": "", "output_date": "", "type_document": "", "name": ""}, None),
    (1, (123, 234), TypeError),
    (4, {"linner": "Test"}, ValueError)
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
