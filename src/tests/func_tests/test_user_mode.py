from pathlib import Path
import pytest

from src.model.user import User


def test_user_add__get_document(get_user):
    # всего 5 отделов. иерархия следующая:
    # 2 -> 1    2 подчиняется 1
    # 3 -> 1
    # 4 -> 2
    # 5 -> 3

    user = User()
    path_to_file = Path(Path.cwd(), "src", "tests", "func_tests", "file for testing", "test.txt")
    all_user_documents = [[], [], [], [], [], []]
    for id_department in range(5, 0, -1):
        user.set_self_data({'id': id_department, 'name': 'Ivan', 'patronymic': "Ivanovich", 'last_name': "Ivanov",
                            'date_last_changes_password': "10.10.2023", 'id_department': id_department,
                            'number_department': id_department * 100}, "Login_Ivan")
        user.add_document(path_to_file, "test.txt", f"{id_department * 100 + id_department}",
                          f"{id_department * 100 - id_department}", "10.10.2023", "txt")
        all_user_documents[id_department] = user.get_data_about_documents()

    # проверяем количество документов, доступное каждому из людей из разных отеделов
    assert len(all_user_documents[1]) == 3
    assert len(all_user_documents[2]) == 2
    assert len(all_user_documents[3]) == 2
    assert len(all_user_documents[4]) == 1
    assert len(all_user_documents[5]) == 1
