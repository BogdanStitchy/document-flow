from pathlib import Path
import pytest

from src.model.utils.custom_exceptions import FileNotWrittenError
from src.model.user import User


def test_user_add_get_document(setup_test_user_mode, get_temp_file):
    # всего 5 отделов. иерархия следующая:
    # 2 -> 1    2 подчиняется 1
    # 3 -> 1
    # 4 -> 2
    # 5 -> 3

    user = User()
    all_user_documents = [[], [], [], [], [], []]
    for id_department in range(5, 0, -1):
        user.set_self_data({'id': id_department, 'name': 'Ivan', 'patronymic': "Ivanovich", 'last_name': "Ivanov",
                            'date_last_changes_password': "10.10.2023", 'id_department': id_department,
                            'number_department': id_department * 100}, "Login_Ivan")
        user.add_document(get_temp_file, "test.txt", f"{id_department * 100 + id_department}",
                          f"{id_department * 100 - id_department}", "10.10.2023", "txt", "note")
        all_user_documents[id_department] = user.get_data_about_documents()

    # проверяем количество документов, доступное каждому из людей из разных отеделов
    assert len(all_user_documents[1]) == 3
    assert len(all_user_documents[2]) == 2
    assert len(all_user_documents[3]) == 2
    assert len(all_user_documents[4]) == 1
    assert len(all_user_documents[5]) == 1


@pytest.mark.parametrize("file_name, id_document, expected_exception", [
    ("test.txt", 1, None),  # ok
    ("test.txt", 11, FileNotWrittenError),
    ("src/nonexistent.txt", 1, FileNotFoundError)
])
def test_get_document(file_name, id_document, expected_exception, get_temp_file, tmp_path):
    path_source_file = get_temp_file
    path_saved_file = tmp_path / f"saved_{file_name}"

    def _read_file(path_to_read: Path):
        with open(path_to_read, "rb") as file:
            return file.read()

    def _make_test():
        content_source = _read_file(path_source_file)
        User.download_document(id_document, path_saved_file)
        content_saved_file = _read_file(path_saved_file)
        return content_source, content_saved_file

    if expected_exception is not None:
        with pytest.raises(expected_exception):
            _make_test()
    else:
        content_source, content_saved_file = _make_test()
        assert content_source == content_saved_file
