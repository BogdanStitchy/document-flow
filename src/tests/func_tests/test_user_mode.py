from pathlib import Path
import pytest

from src.model.custom_exceptions import FileNotWrittenError
from src.model.user import User


def test_user_add_get_document():
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


@pytest.mark.parametrize("path_source_file, path_saved_file, id_document, expected_exception", [
    (Path(Path.cwd(), "src", "tests", "func_tests", "file for testing", "test.txt"),
     Path(Path.cwd(), "src", "tests", "func_tests", "file for testing", "saved files",
          "saved_test.txt"),
     1, None),  # ok

    (Path(Path.cwd(), "src", "tests", "func_tests", "file for testing", "test.txt"),
     Path(Path.cwd(), "src", "tests", "func_tests", "file for testing", "saved files",
          "saved_test.txt"),
     11, FileNotWrittenError),

    (Path(Path.cwd(), "src", "tests", "func_tests", "file for testing", "test.txt"),
     Path(Path.cwd(), "src", "tests", "func_tests", "saved files", "saved_test.txt"),
     1, FileNotFoundError)

])
def test_get_document(path_source_file, path_saved_file, id_document, expected_exception, clean_test_files_directory):
    def _read_file(path_to_read: str or Path):
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
        return

    content_source, content_saved_file = _make_test()
    assert content_source == content_saved_file
