import pytest
from src.model.user import User


@pytest.fixture(scope="module")
def get_user():
    user = User()
    user.set_self_data({'id': 1, 'name': 'Ivan', 'patronymic': "Ivanovich", 'last_name': "Ivanov",
                        'date_last_changes_password': "10.10.2023", 'id_department': 1, 'number_department': 100},
                       "Login_Ivan")
    return user


@pytest.fixture(scope="function")
def get_temp_file(tmp_path):
    file_name = "source_test.txt"
    temp_file_path = tmp_path / file_name

    # проверка, существует ли файл, и создание его, если он не существует
    if not temp_file_path.exists():
        temp_file_path.write_text("_____test file_____")

    return temp_file_path
