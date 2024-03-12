from pathlib import Path

import pytest

from src.model.user import User


def test_add_document(get_user):
    user = get_user
    path_to_file = Path(Path.cwd(), "src", "tests", "func_tests", "file for testing", "test.txt")
    user.add_document(path_to_file, "test.txt", "12345", "54531", "10.10.2023", "txt")             #B:\работа\проекты с работы\document_flow\src\tests\func_tests\file for testing\test.txt
    documents = user.get_data_about_documents()
    assert 3 == 3
