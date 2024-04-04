import pytest
import src.controller.controller_main_window as controller
from src.model.utils.custom_exceptions.client_custom_exceptions import ClientNotFoundError, ClientPasswordError
from src.config.types_role import Role


@pytest.mark.parametrize("login, password, role, expected_exception",
                         [
                             # admins
                             ("ivanadmin", "password1", Role.ADMIN, None),  # успешный вход
                             ("ivanadmin", "password1", Role.USER, ClientNotFoundError),  # не найден в базе админ
                             ("ivan", "password1", Role.ADMIN, ClientNotFoundError),  # не найден в базе админ
                             ("petradmin", "password", Role.ADMIN, ClientPasswordError),  # неверный пароль
                             # users
                             ("ivanovii", "pass123", Role.USER, None),  # успешный вход
                             ("ivanovii", "pass123", Role.ADMIN, ClientNotFoundError),  # не найден в базе пользователей
                             ("ivanovii", "pass", Role.USER, ClientPasswordError),  # неверный пароль
                         ])
def test_login(setup_test_login, login, password, role, expected_exception):
    if expected_exception is not None:
        with pytest.raises(expected_exception):
            controller.__check_login(login, password, role)
        return
    assert role == controller.__check_login(login, password, role)
