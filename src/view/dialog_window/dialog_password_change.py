from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QDialog
from src.controller import controller_main_window as controller


class DialogWidgetChangePassword(QDialog):
    def __init__(self, main_window):
        QDialog.__init__(self)
        self.setModal(True)
        self.main_window = main_window
        self.flag_success_exit = False
        self.setWindowTitle("Смена пароля")
        self.show()
        self.setupUi()

    def setupUi(self):
        font = QtGui.QFont()
        font.setFamily("Monospac821 BT")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)

        self.setObjectName("Dialog")
        self.resize(400, 300)
        self.setStyleSheet("background-color: rgb(146, 180, 236);")
        # self.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self)
        self.frame.setMinimumSize(QtCore.QSize(0, 100))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout.addWidget(self.frame)

        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")

        self.label_user = QtWidgets.QLabel(self)
        self.label_user.setObjectName("label_user")
        self.label_user.setFont(font)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_user)

        self.label_password = QtWidgets.QLabel(self)
        self.label_password.setObjectName("label_password")
        self.label_password.setFont(font)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_password)

        self.label_password_repeat = QtWidgets.QLabel(self)
        self.label_password_repeat.setObjectName("label_password_repeat")
        self.label_password_repeat.setFont(font)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_password_repeat)

        style_for_line_edit = "border: 2px solid;\n" \
                              "border-color: rgb(255, 230, 154);\n" \
                              "border-radius: 5px;\n" \
                              "\n" \
                              ""

        self.lineEdit_password = QtWidgets.QLineEdit(self)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.lineEdit_password.setFont(font)
        self.lineEdit_password.setStyleSheet(style_for_line_edit)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_password)

        self.lineEdit_password_repeat = QtWidgets.QLineEdit(self)
        self.lineEdit_password_repeat.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password_repeat.setObjectName("lineEdit_password_repeat")
        self.lineEdit_password_repeat.setFont(font)
        self.lineEdit_password_repeat.setStyleSheet(style_for_line_edit)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_password_repeat)

        self.label_name = QtWidgets.QLabel(self)
        self.label_name.setObjectName("label_name")
        self.label_name.setFont(font)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_name)

        self.pushButton_save = QtWidgets.QPushButton(self)
        self.pushButton_save.setObjectName("pushButton_save")
        self.pushButton_save.clicked.connect(self.save_password)
        self.pushButton_save.setFont(font)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.pushButton_save)
        self.verticalLayout.addLayout(self.formLayout)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label_user.setText(_translate("Dialog", "Пользователь: "))
        self.label_password.setText(_translate("Dialog", "Введите пароль:"))
        self.label_password_repeat.setText(_translate("Dialog", "Подтвердите пароль:"))
        self.label_name.setText(_translate("Dialog", controller.get_login()))
        self.pushButton_save.setText(_translate("Dialog", "Сохранить"))

    def save_password(self):
        password = self.lineEdit_password.text()
        password_repeat = self.lineEdit_password_repeat.text()
        if password != password_repeat:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Введеные пароли не сходятся!")
        if password == "":
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Введите пароль!")
        else:
            if controller.change_password(password):
                self.flag_success_exit = True
                self.close()
            else:
                QtWidgets.QMessageBox.warning(self, "Предупреждение", "Старый и новый пароли должны отличаться!")

    def closeEvent(self, event):
        if not self.flag_success_exit:
            reply = QtWidgets.QMessageBox.information(self, 'Выход',
                                                      'Вы точно хотите выйти? Без смены пароля не возможно '
                                                      'дальнейшее использование программы!',
                                                      QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                      QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                event.accept()
                self.main_window.close()
                self.close()
            else:
                event.ignore()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog_add_user = QtWidgets.QWidget()
    Dialog_add_user.show()

    ui = DialogWidgetChangePassword(Dialog_add_user, "login")

    sys.exit(app.exec_())
