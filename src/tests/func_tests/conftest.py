import pytest
from src.model.super_admin import SuperAdmin


@pytest.fixture(scope="module")
def fill_db_admins(create_database):
    added_admins = [("Иванов", "Иван", "Иванович", "ivanadmin", "password1"),
                    ("Петров", "Петр", "Петрович", "petradmin", "password2"),
                    ("Сергеев", "Сергей", "Сергеевич", "sergeyadmin", "password3")]

    for admin in added_admins:
        SuperAdmin.add_admin(*admin)
