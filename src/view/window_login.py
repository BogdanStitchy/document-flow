import sys

from PyQt5 import QtGui, QtWidgets
from src.view.design_login_window import WindowLogin
from src.controller import controller_window_login as controller

import window_sa_test
import window_user
import window_admin


class HandlerWindowLogin(QtWidgets.QMainWindow):
    def __init__(self):
        super(HandlerWindowLogin, self).__init__()
        self.windows_login = WindowLogin()
        self.windows_login.setup_ui(self)
        self.init_window_login()

    def init_window_login(self):

        self.windows_login.button_login.clicked.connect(self.button_login_press)
        self.windows_login.button_login.setShortcut(QtGui.QKeySequence("Return"))  # нажата клавиша enter

    def button_login_press(self):
        input_login = self.windows_login.line_login.text()
        input_password = self.windows_login.line_password.text()
        print(f"login = {input_login}\tpassword = {input_password}")
        login_flag = controller.check_login(input_login, input_password)
        print("login_flag in view = ", login_flag)
        if type(login_flag) != int:
            print(" self.clear_password_line()")
            self.clear_password_line()
        elif login_flag == 0:
            print("current = super admin")
            self.admin = window_sa_test.WindowSuperAdmin()
            self.admin.show()
            self.close()
        elif login_flag == 1:
            print("current = admin")
            self.window_admin = window_admin.WindowAdmin()
            self.close()
        elif login_flag == 2:
            print("current = user")
            self.window_user = window_user.WindowUser()
            self.close()

    def clear_password_line(self):
        self.windows_login.line_password.setText('')
        self.repaint()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = HandlerWindowLogin()
    application.show()

    sys.exit(app.exec())
