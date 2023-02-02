from src.model import admin
from src.view.window_login import HandlerWindowLogin


def check_login(login, password):
    # this meat create logi
    check_result = admin.check_password(login, password)
    if check_result:
        print("controller", check_result)
        return True
    else:
        print("Вход не выполнен")
        return False
