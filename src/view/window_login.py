import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from src.view.design_login_window import WindowLogin
from src.controller import controller_window_login as controller
from src.model import admin


class HandlerWindowLogin(QtWidgets.QMainWindow):
    def __init__(self):
        super(HandlerWindowLogin, self).__init__()
        self.windows_login = WindowLogin()
        self.windows_login.setup_ui(self)
        self.init_window_login()

    def init_window_login(self):
        self.windows_login.button_login.clicked.connect(self.button_press)
        self.windows_login.button_login.setShortcut(QtGui.QKeySequence("Return"))  # нажата клавиша enter

    def button_press(self):
        input_login = self.windows_login.line_login.text()
        input_password = self.windows_login.line_password.text()
        print(f"login = {input_login}\tpassword = {input_password}")
        login_flag = controller.check_login(input_login, input_password)
        if not login_flag:
            self.clear_password_line()

    def clear_password_line(self):
        self.windows_login.line_password.setText('')
        self.repaint()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = HandlerWindowLogin()
    application.show()

    sys.exit(app.exec())
