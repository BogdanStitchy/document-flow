import pytest


@pytest.fixture(scope="module")
def setup_test_1_super_admins_db_method(clean_all_database):
    pass


@pytest.fixture(scope="module")
def setup_test_2_admins_db_method(clean_all_database, fill_db_admins,
                                  fill_db_departments_and_departments_hierarchy):
    pass


@pytest.fixture(scope="module")
def setup_test_3_users_db_method(clean_all_database, fill_db_admins, fill_db_users):
    pass


@pytest.fixture(scope="module")
def setup_test_4_update_documents(clean_all_database, fill_db_admins, fill_db_documents):
    pass
