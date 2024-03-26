from pathlib import Path

import pytest
from src.model.super_admin import SuperAdmin
from src.model.administrator import Administrator
from src.model.user import User


@pytest.fixture(scope="module")
def fill_db_admins(create_database):
    added_admins = [("Иванов", "Иван", "Иванович", "ivanadmin", "password1"),
                    ("Петров", "Петр", "Петрович", "petradmin", "password2"),
                    ("Сергеев", "Сергей", "Сергеевич", "sergeyadmin", "password3")]

    for admin in added_admins:
        SuperAdmin.add_admin(*admin)


@pytest.fixture(scope="module")
def fill_db_departments_and_departments_hierarchy():
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
def fill_db_users(create_database, fill_db_departments_and_departments_hierarchy):
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
        # last_name=user[0], name=user[1], patronymic=user[2], login=user[3], password=user[4], id_department=user[5]


@pytest.fixture(scope="module")
def get_user():
    user = User()
    user.set_self_data({'id': 1, 'name': 'Ivan', 'patronymic': "Ivanovich", 'last_name': "Ivanov",
                        'date_last_changes_password': "10.10.2023", 'id_department': 1, 'number_department': 100},
                       "Login_Ivan")
    return user


@pytest.fixture(scope="function")
def clean_test_files_directory():
    directory_path = Path(Path.cwd(), "src", "tests", "func_tests", "file for testing", "saved files")

    
    # Создаем каталог, если он не существует
    directory_path.mkdir(parents=True, exist_ok=True)
    
    # Перебор всех файлов в директории и их удаление
    for file_path in directory_path.iterdir():
        if file_path.is_file() or file_path.is_symlink():
            file_path.unlink()
