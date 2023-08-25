from PyQt5 import QtWidgets
from src.view.window_login import HandlerWindowLogin
import sys


def main():
    app = QtWidgets.QApplication([])
    application = HandlerWindowLogin()
    application.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
