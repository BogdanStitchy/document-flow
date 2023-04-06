import datetime
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets

from src.view import window_login
from widget import widget_setting_documents
from src.controller import controller_main_window as controller
from src.view.dialog_window.dialog_password_change import DialogWidgetChangePassword


class WindowUser(QtWidgets.QMainWindow):
    def __init__(self):
        super(WindowUser, self).__init__()
        self.setObjectName("MainWindow")
        self.resize(1110, 706)
        self.setMinimumSize(900, 706)
        path_to_images = Path(Path().cwd().parent.parent, "pictures")
        print("path in user = ", (str(Path(path_to_images, "logo.png"))))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(str(Path(path_to_images, "logo.png"))), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setupUi()
        self.show()
        self.check_needs_password_change()

    def setupUi(self):
        self.centralwidget = QtWidgets.QWidget(self)

        font = QtGui.QFont()
        font.setFamily("Monospac821 BT")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)

        self.centralwidget.setFont(font)
        self.centralwidget.setStyleSheet("background-color: rgb(146, 180, 236);")
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.frame_data = QtWidgets.QFrame(self.centralwidget)
        self.frame_data.setFont(font)
        self.frame_data.setStyleSheet("")
        self.frame_data.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_data.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_data.setObjectName("frame_data")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_data)
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(520, 18, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        self.label_name = QtWidgets.QLabel(self.frame_data)
        self.label_name.setFont(font)
        self.label_name.setObjectName("label_name")
        self.horizontalLayout.addWidget(self.label_name)

        spacerItem1 = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        self.label_departament = QtWidgets.QLabel(self.frame_data)
        self.label_departament.setFont(font)
        self.label_departament.setObjectName("label_departament")
        self.horizontalLayout.addWidget(self.label_departament)

        self.pushButton_logout = QtWidgets.QPushButton(self.frame_data)
        self.pushButton_logout.clicked.connect(self.logout)
        self.pushButton_logout.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_logout.setFont(font)
        self.pushButton_logout.setStyleSheet("padding: 5;\n"
                                             "border-radius:5px;\n"
                                             "border: 1 solid black;\n"
                                             "")
        self.pushButton_logout.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton_logout)

        self.verticalLayout.addWidget(self.frame_data)
        self.verticalLayout.addWidget(widget_setting_documents.WidgetDocuments())

        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, ):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "BZ document flow"))
        self.label_name.setText(_translate("MainWindow", controller.get_full_name()))
        self.label_departament.setText(_translate("MainWindow", f"отдел {controller.get_number_department()}"))
        self.pushButton_logout.setText(_translate("MainWindow", "выйти"))

    def logout(self):
        self.login = window_login.HandlerWindowLogin()
        self.login.show()
        self.close()

    def check_needs_password_change(self):
        change = controller.get_last_password_change()
        # print(change)
        # print(type(change))
        if change is None:
            self.dialog = DialogWidgetChangePassword(self)
            result = self.dialog.exec()
            print("result exit: ", result)
        else:
            delta_date = datetime.datetime.now() - change
            # print("days:", delta_date.days)
            if delta_date.days > 180:
                self.dialog = DialogWidgetChangePassword(self)
                result = self.dialog.exec()
                # print("result exit: ", result)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = WindowUser()
    ui.check_needs_password_change()
    sys.exit(app.exec_())
