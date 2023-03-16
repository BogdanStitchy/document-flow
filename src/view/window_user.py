from PyQt5 import QtCore, QtGui, QtWidgets

from src.view import window_login
from widget import widget_setting_documents


class WindowUser(QtWidgets.QMainWindow):
    def __init__(self):
        super(WindowUser, self).__init__()
        self.setObjectName("MainWindow")
        self.resize(1110, 706)
        self.setMinimumSize(900, 706)
        self.setupUi()
        self.show()

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
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_name.setText(_translate("MainWindow", "Иван Иванович Иванов"))
        self.label_departament.setText(_translate("MainWindow", "отдел 235"))
        self.pushButton_logout.setText(_translate("MainWindow", "выйти"))

    def logout(self):
        self.login = window_login.HandlerWindowLogin()
        self.login.show()
        self.close()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = WindowUser()
    sys.exit(app.exec_())
