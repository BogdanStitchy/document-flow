from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QButtonGroup
from src.model.for_data_base.db_helper_for_hierarchy_derartments import get_all_departments
from src.controller import controller_main_window as controller


class DialogWidgetEditUser(QDialog):
    def __init__(self, main_window, last_name: str, name: str, patronymic: str, number_department: int, login: str,
                 id_user: int):
        QDialog.__init__(self)
        self.dialog_window = None
        self.last_name = last_name
        self.name = name
        self.patronymic = patronymic
        self.number_department = number_department
        self.login = login
        self.id_user = id_user

        self.setModal(True)
        self.main_window = main_window
        self.show()
        self.setupUi()

    def setupUi(self):
        self.show()
        # self.setWindowTitle("Добавление пользователя")
        self.setObjectName("Dialog_add_user")
        self.resize(580, 500)
        self.setMinimumSize(QtCore.QSize(320, 340))
        # self.setMaximumSize(QtCore.QSize(400, 380))
        self.setStyleSheet("background-color: rgb(146, 180, 236);")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.main_frame = QtWidgets.QFrame(self)
        self.main_frame.setStyleSheet("")
        self.main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_frame.setObjectName("main_frame")
        self.formLayout = QtWidgets.QFormLayout(self.main_frame)
        self.formLayout.setObjectName("formLayout")
        self.label_last_name = QtWidgets.QLabel(self.main_frame)

        font = QtGui.QFont()
        font.setFamily("Monospac821 BT")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)

        style_for_line_edit = "border: 2px solid;\n" \
                              "border-color: rgb(255, 230, 154);\n" \
                              "border-radius: 5px;\n" \
                              "\n"

        self.label_last_name.setFont(font)
        self.label_last_name.setObjectName("label_last_name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_last_name)

        self.lineEdit_last_name = QtWidgets.QLineEdit(self.main_frame)
        self.lineEdit_last_name.setText(self.last_name)
        self.lineEdit_last_name.setMinimumSize(QtCore.QSize(0, 23))
        self.lineEdit_last_name.setFont(font)
        self.lineEdit_last_name.setStyleSheet(style_for_line_edit)
        self.lineEdit_last_name.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_last_name.setObjectName("lineEdit_last_name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_last_name)

        self.lineEdit_name = QtWidgets.QLineEdit(self.main_frame)
        self.lineEdit_name.setText(self.name)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.lineEdit_name.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_name.setMinimumSize(QtCore.QSize(0, 23))
        self.lineEdit_name.setFont(font)
        self.lineEdit_name.setStyleSheet(style_for_line_edit)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_name)

        self.label_patronymic = QtWidgets.QLabel(self.main_frame)
        self.label_patronymic.setFont(font)
        self.label_patronymic.setObjectName("label_patronymic")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_patronymic)

        self.lineEdit_patronymic = QtWidgets.QLineEdit(self.main_frame)
        self.lineEdit_patronymic.setText(self.patronymic)
        self.lineEdit_patronymic.setObjectName("lineEdit_patronymic")
        self.lineEdit_patronymic.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_patronymic.setMinimumSize(QtCore.QSize(0, 23))
        self.lineEdit_patronymic.setFont(font)
        self.lineEdit_patronymic.setStyleSheet(style_for_line_edit)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_patronymic)

        self.scrollArea = QtWidgets.QScrollArea(self.main_frame)
        self.scrollArea.setStyleSheet("border-radius: 1px;")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 315, 145))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.group = QtWidgets.QButtonGroup(self.scrollAreaWidgetContents)
        self.add_radiobutton()
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.scrollArea)

        self.label_login = QtWidgets.QLabel(self.main_frame)
        self.label_login.setFont(font)
        self.label_login.setObjectName("label_login")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_login)

        self.lineEdit_login = QtWidgets.QLineEdit(self.main_frame)
        self.lineEdit_login.setText(self.login)
        # self.lineEdit_login.setPlaceholderText("Логин вводить только при необходимости замены")
        self.lineEdit_login.setObjectName("lineEdit_login")
        self.lineEdit_login.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_login.setMinimumSize(QtCore.QSize(0, 23))
        self.lineEdit_login.setFont(font)
        self.lineEdit_login.setStyleSheet(style_for_line_edit)
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.lineEdit_login)

        self.label_departments = QtWidgets.QLabel(self.main_frame)
        self.label_departments.setFont(font)
        self.label_departments.setObjectName("label_departments")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_departments)

        self.label_password = QtWidgets.QLabel(self.main_frame)
        self.label_password.setFont(font)
        self.label_password.setObjectName("label_password")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_password)

        self.lineEdit_password = QtWidgets.QLineEdit(self.main_frame)
        self.lineEdit_password.setPlaceholderText("Пароль вводить только при необходимости замены")
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.lineEdit_password.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_password.setMinimumSize(QtCore.QSize(0, 23))
        self.lineEdit_password.setFont(font)
        self.lineEdit_password.setStyleSheet(style_for_line_edit)
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.lineEdit_password)

        self.label_name = QtWidgets.QLabel(self.main_frame)
        self.label_name.setFont(font)
        self.label_name.setObjectName("label_name")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_name)
        self.verticalLayout.addWidget(self.main_frame)

        self.pushButton_save = QtWidgets.QPushButton(self)
        self.pushButton_save.pressed.connect(self.push_save)
        self.pushButton_save.setMinimumSize(QtCore.QSize(0, 23))
        self.pushButton_save.setFont(font)
        self.pushButton_save.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_save.setStyleSheet("background-color: rgb(255, 210, 76);\n"
                                           "border-radius: 5px;\n"
                                           "\n"
                                           "")
        self.pushButton_save.setObjectName("pushButton_save")
        self.verticalLayout.addWidget(self.pushButton_save)

        self.pushButton_cancel = QtWidgets.QPushButton(self)
        self.pushButton_cancel.pressed.connect(self.push_cancel)
        self.pushButton_cancel.setMinimumSize(QtCore.QSize(0, 23))
        self.pushButton_cancel.setFont(font)
        self.pushButton_cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_cancel.setStyleSheet("background-color: rgb(255, 210, 76);\n"
                                             "border-radius: 5px;\n"
                                             "\n"
                                             "")
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.verticalLayout.addWidget(self.pushButton_cancel)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle("Редактирование пользователя")
        self.label_last_name.setText(_translate("Dialog_add_user", "Фамилия:"))
        self.label_patronymic.setText(_translate("Dialog_add_user", "Отчество:"))
        self.label_login.setText(_translate("Dialog_add_user", "Логин:"))
        self.label_departments.setText(_translate("Dialog_add_user", "Отдел:"))
        self.label_password.setText(_translate("Dialog_add_user", "Пароль:"))
        self.label_name.setText(_translate("Dialog_add_user", "Имя:"))
        self.pushButton_save.setText(_translate("Dialog_add_user", "Сохранить"))
        self.pushButton_cancel.setText(_translate("Dialog_add_user", "Отмена"))

    def add_radiobutton(self):
        departments = get_all_departments()
        for department in departments:
            radio_button = QtWidgets.QRadioButton(f"{department[2]} - {department[1]}")
            if self.number_department == department[2]:
                print("TRUE")
                radio_button.click()
            self.verticalLayout_2.addWidget(radio_button)
            self.group.addButton(radio_button)

    def push_save(self):
        new_last_name = self.lineEdit_last_name.text()
        new_name = self.lineEdit_name.text()
        new_patronymic = self.lineEdit_patronymic.text()
        new_login = self.lineEdit_login.text()
        new_password = self.lineEdit_password.text()
        if new_login != self.login:
            flag_edit_login = True
        else:
            flag_edit_login = False
        print("password = ", new_password)
        try:
            department = self.group.checkedButton().text()  # получаем выбранную радиобаттон
            department = department[:3]  # получаем только номер отдела, без его названия
            print(department)
            controller.edit_user_data(new_last_name, new_name, new_patronymic, department, new_login, new_password,
                                      self.id_user, flag_edit_login)
            self.main_window.press_button_refresh()
            self.dialog_window = QtWidgets.QMessageBox().information(self, "Редактирование пользователя",
                                                                     f'Данные пользователя '
                                                                     f'"{new_last_name} {new_name} {new_patronymic}" '
                                                                     f'успешно отредактированы.')
            self.close()
        except Exception as ex:
            self.dialog_window = QtWidgets.QMessageBox().warning(self, "Редактирование пользователя",
                                                                 "Для редактирования пользователя заполните все поля! ")
            print("[ERROR] Не выбран ни один радиобаттон\t", ex)

    def push_cancel(self):
        self.close()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog_add_user = QtWidgets.QWidget()
    Dialog_add_user.show()

    Dialog_add_user.setWindowTitle("TRGGFFG")
    # print(Dialog_add_user.windowTitle())

    ui = DialogWidgetEditUser(Dialog_add_user, "last_name", "name", "patronymic", 401, "Ivan@mail.ru", 1)

    sys.exit(app.exec_())
