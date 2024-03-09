import pytest

from src.db.methods import admin_db_methods


@pytest.fixture(scope="module")
def database_admin():
    admin_methods = admin_db_methods.AdminMethodsDB()
    yield admin_methods


@pytest.mark.parametrize("id_document, kwargs, expected_exception", [
    (1, {"inner_number": "", "output_number": "", "output_date": "", "type_document": "", "name": ""}, None),
    (2, {"inner_number": "", "output_number": "", "output_date": "", "type_document": "", "name": ""}, None),
    (1, (123, 234), TypeError),
    (4, {"linner": "Test"}, ValueError)
])
def test_update_document(database_admin, id_document, kwargs, expected_exception):
    if expected_exception is None:
        database_admin.edit_document(id_document, **kwargs)
    else:
        with pytest.raises(expected_exception):
            database_admin.edit_document(id_document, **kwargs)
