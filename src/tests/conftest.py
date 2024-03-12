import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.models import base
from src.db.database_setup import set_new_engine

from src.db.methods import super_admin_db_methods as sa_methods

# data_base_local = "sqlite:///B:/работа/проекты с работы/document_flow/tests/testDB.db"
data_base_memory = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def create_database():
    engine = create_engine(data_base_memory)
    base.Base.metadata.create_all(engine)
    set_new_engine(engine)
    return engine


@pytest.fixture(scope="session")
def get_session(create_database):
    engine = create_database
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


@pytest.fixture(scope="module")
def clean_all_database(create_database, get_session):
    session = get_session
    try:
        for table in base.Base.metadata.sorted_tables:
            session.execute(table.delete())
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


@pytest.fixture(scope="module")
def clean_admins_table_database(create_database, get_session):
    session = get_session
    try:
        admin_table = base.Base.metadata.tables['admins']
        session.execute(admin_table.delete())
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


@pytest.fixture(scope="module")
def clean_users_table_database(create_database, get_session):
    session = get_session
    try:
        user_table = base.Base.metadata.tables['users']
        session.execute(user_table.delete())
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


@pytest.fixture(scope="module")
def clean_departments_table_database(create_database, get_session):
    session = get_session
    try:
        departments_table = base.Base.metadata.tables['departments']
        departments_hierarchy_table = base.Base.metadata.tables['departments_hierarchy']
        session.execute(departments_table.delete())
        session.execute(departments_hierarchy_table.delete())
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


@pytest.fixture(scope="module")
def clean_documents_table_database(create_database, get_session):
    session = get_session
    try:
        data_document_table = base.Base.metadata.tables['data_about_documents']
        file_document_table = base.Base.metadata.tables['files_documents']
        session.execute(data_document_table.delete())
        session.execute(file_document_table.delete())
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


@pytest.fixture(scope="module")
def db_methods_super_admin():
    super_admin_methods = sa_methods.SuperAdminMethodsDB()
    yield super_admin_methods
