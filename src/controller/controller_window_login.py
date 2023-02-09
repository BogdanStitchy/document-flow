from src.model import admin
from src.view.window_login import HandlerWindowLogin


def check_login(login, password):
    # this meat create logi
    check_result = admin.check_password(login, password)
    print("check_result in controller = ", check_result)
    if type(check_result) == int:
        print("контроллер Вход выполнен")
        return check_result
    else:
        print("контроллер Вход не выполнен")
        return False
    # else:
    #     return check_result
