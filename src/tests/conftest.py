import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.models import base
from src.db.database_setup import set_new_engine
from src.model.super_admin import SuperAdmin
from src.model.administrator import Administrator
from src.db.methods import super_admin_db_methods as sa_methods

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
def db_methods_super_admin():
    super_admin_methods = sa_methods.SuperAdminMethodsDB()
    yield super_admin_methods


# ------------------------------------for clean table DB---------------------------------------------------------------
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


# ------------------------------------for fill table DB---------------------------------------------------------------
@pytest.fixture(scope="module")
def fill_db_admins(db_methods_super_admin):
    existing_admins = db_methods_super_admin.get_all_admins()
    if len(existing_admins) != 0:
        print(f"Table admins not empty. existing_admins:\n{existing_admins}\n")
        return

    added_admins = [("Иванов", "Иван", "Иванович", "ivanadmin", "password1"),
                    ("Петров", "Петр", "Петрович", "petradmin", "password2"),
                    ("Сергеев", "Сергей", "Сергеевич", "sergeyadmin", "password3")]

    for admin in added_admins:
        SuperAdmin.add_admin(*admin)


@pytest.fixture(scope="module")
def fill_db_departments_and_departments_hierarchy(db_methods_super_admin):
    existing_departments = db_methods_super_admin.get_all_departments()
    if len(existing_departments) != 0:
        print(f"Table departments not empty. existing_departments:\n{existing_departments}\n")
        return

    added_department = [
        ("Финансовый", 101, None),  # id = 1
        ("Кадровый", 102, 1),  # id = 2
        ("Информационные Технологии", 103, 1),  # id = 3
        ("Маркетинг", 104, 2),  # id = 4
        ("Продажи", 105, 3)  # id = 5
    ]
    for department in added_department:
        SuperAdmin.add_department(*department)


@pytest.fixture(scope="module")
def fill_db_users(create_database, fill_db_departments_and_departments_hierarchy, db_methods_super_admin):
    existing_users = db_methods_super_admin.get_all_users()
    if len(existing_users) != 0:
        print(f"Table users not empty. existing_users:\n{existing_users}\n")
        return

    added_users = [("Иванов", "Иван", "Иванович", "ivanovii", "pass123", 1),
                   ("Петрова", "Мария", "Алексеевна", "petrovama", "pass234", 2),
                   ("Сидоров", "Николай", "Петрович", "sidorovnp", "pass345", 3),
                   ("Кузнецов", "Алексей", "Дмитриевич", "kuznetsovad", "pass456", 4),
                   ("Смирнова", "Екатерина", "Васильевна", "smirnovaev", "pass567", 5),
                   ("Волков", "Дмитрий", "Анатольевич", "volkovda", "pass678", 4),
                   ("Зайцева", "Ольга", "Геннадьевна", "zaytsevog", "pass789", 5)]
    admin = Administrator()
    admin.set_self_data({"id": 1, 'name': 'test', 'patronymic': 'test', 'last_name': 'test',
                         'date_last_changes_password': "10.10.2023"},
                        "login")  # потому что при добавлении пользователя, используется атрибут id админа
    for user in added_users:
        admin.add_user(*user)
