import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from window_login import HandlerWindowLogin
from window_sa_test import WindowSuperAdmin

from src.view.dialog_window.dialog_add_user import DialogWidgetAddUser


def main():
    app = QtWidgets.QApplication(sys.argv)
    window_login = HandlerWindowLogin()
    window_login.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()