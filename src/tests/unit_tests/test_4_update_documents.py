import pytest


@pytest.mark.parametrize("id_document, kwargs, expected_exception", [
    (1, {"inner_number": "", "output_number": "", "output_date": "", "type_document": "", "name": ""}, None),
    (2, {"inner_number": "", "output_number": "", "output_date": "", "type_document": "", "name": ""}, None),
    (1, (123, 234), TypeError),
    (4, {"linner": "Test"}, ValueError)
])
def test_update_document(setup_test_4_update_documents, database_admin, id_document, kwargs, expected_exception):
    if expected_exception is None:
        database_admin.edit_document(id_document, **kwargs)
    else:
        with pytest.raises(expected_exception):
            database_admin.edit_document(id_document, **kwargs)


def test_delete_document(database_admin):
    count_documents_before_delete = len(database_admin.get_all_documents())
    database_admin.delete_document(1)
    count_documents_after_delete = len(database_admin.get_all_documents())
    assert count_documents_after_delete == count_documents_before_delete - 1
