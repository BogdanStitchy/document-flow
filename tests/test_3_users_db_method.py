from datetime import datetime

from pydantic import ValidationError
import pytest
import os

from src.db.methods import user_db_methods


@pytest.fixture(scope="module")
def database_user():
    user_methods = user_db_methods.UserDB()
    yield user_methods


@pytest.mark.parametrize("data, expected_exception", [
    ((1, os.urandom(16), "doc1", "11111", "333333", datetime(2023, 7, 12), "docx"), None),
    ((1, os.urandom(16), "doc2", "22222", "77777", datetime(2023, 7, 12), "pdf"), None),
    ((1, os.urandom(16), "doc3", "55555", "99999", datetime(2023, 7, 12), "rtx"), None),
    ((1, os.urandom(16), "doc3", "55555", 99999, datetime(2023, 7, 12), "rtx"), ValidationError),
    ((1, os.urandom(16), "doc3", "55555", "99999", datetime(2023, 7, 12), 15.7), ValidationError)
])
def test_add_document(database_user, data, expected_exception):
    if expected_exception is None:
        database_user.add_document(*data)
    else:
        with pytest.raises(expected_exception):
            database_user.add_document(*data)


def test_get_document():
    from src.db.methods.admin_db_methods import AdminMethodsDB
    documents = AdminMethodsDB.get_all_documents()
    assert len(documents) == 3
