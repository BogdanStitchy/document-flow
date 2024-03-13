import datetime

from pydantic import ValidationError
import pytest
import os

from src.db.methods import user_db_methods


@pytest.fixture(scope="module")
def database_user():
    user_methods = user_db_methods.UserDB()
    yield user_methods


@pytest.mark.parametrize("data, expected_exception", [
    ((1, os.urandom(16), "doc1", "11111", "333333", datetime.datetime(2019, 7, 12), "docx"), None),
    ((1, os.urandom(16), "doc2", "22222", "77777", datetime.datetime(2020, 7, 12), "pdf"), None),
    ((1, os.urandom(16), "doc3", "55555", "99999", datetime.datetime(2023, 7, 12), "rtx"), None),
    ((1, os.urandom(16), "doc3", "55555", 99999, datetime.datetime(2023, 7, 12), "rtx"), ValidationError),
    ((1, os.urandom(16), "doc3", "55555", "99999", datetime.datetime(2023, 7, 12), 15.7), ValidationError)
])
def test_add_document(database_user, clean_documents_table_database, data, expected_exception):
    if expected_exception is None:
        database_user.add_document(*data)
    else:
        with pytest.raises(expected_exception):
            database_user.add_document(*data)


def test_get_document_admin():
    from src.db.methods.admin_db_methods import AdminMethodsDB
    documents = AdminMethodsDB.get_all_documents()
    assert len(documents) == 3


def test_good_find_document_period(database_user):
    start_output_date = datetime.datetime.strptime("01.01.2019", "%d.%m.%Y")
    end_output_date = datetime.datetime.strptime("01.01.2021", "%d.%m.%Y")
    date_creating = datetime.date.today() + datetime.timedelta(days=1)

    res = database_user.find_document_period(start_output_date, end_output_date,
                                             start_output_date, date_creating)
    assert len(res) == 2


def test_broke_find_documents_period(database_user):
    with pytest.raises(ValidationError):
        database_user.find_document_period("01.05.2021", "01.05.2025", "01.05.2021", "01.05.2025")
