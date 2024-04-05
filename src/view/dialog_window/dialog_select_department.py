from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog
from src.controller import controller_main_window as controller


class DialogWidgetSelectDepartment(QDialog):
    def __init__(self, main_window, id_department_delete):
        QDialog.__init__(self)
        self.dialog_window = None
        self.setModal(True)
        self.main_window = main_window
        self.selected_department = None
        self.id_department_delete = id_department_delete

        self.show()
        self.__setupUi()

    def __setupUi(self):
        self.show()
        self.setWindowTitle("Выбор отдела для перемещения пользователей")

        font = QtGui.QFont()
        font.setFamily("Monospac821 BT")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)

        self.setObjectName("Dialog_add_user")
        self.resize(550, 330)
        self.setMinimumSize(QtCore.QSize(320, 250))
        self.setStyleSheet("background-color: rgb(146, 180, 236);")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.setFont(font)

        self.label_instruction = QtWidgets.QLabel(self)
        self.label_instruction.setAlignment(QtCore.Qt.AlignCenter)
        self.label_instruction.setText("Выберите, к какому отделу необходимо прикрепить людей из удаляемого отдела:")
        self.verticalLayout.addWidget(self.label_instruction)

        self.__add_radiobutton()

        self.button_save = QtWidgets.QPushButton(self)
        self.verticalLayout.addWidget(self.button_save)
        self.button_save.setText("Сохранить")
        self.button_save.pressed.connect(self.__save_answer)
        self.button_save.setMinimumSize(QtCore.QSize(0, 23))
        self.button_save.setFont(font)
        self.button_save.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_save.setStyleSheet("background-color: rgb(255, 210, 76);\n"
                                       "border-radius: 5px;\n"
                                       "")

    def __add_radiobutton(self):
        departments = controller.get_all_departments_without_one(self.id_department_delete)
        self.group = QtWidgets.QButtonGroup(self)
        for department in departments:
            radio_button = QtWidgets.QRadioButton(f"{department.number_department} - {department.name_department}")
            radio_button.setObjectName(f"{department.id}")
            self.verticalLayout.addWidget(radio_button)
            self.group.addButton(radio_button)

    def __save_answer(self):
        try:
            department = self.group.checkedButton().objectName()  # получаем выбранную радиобаттон
            self.selected_department = department
            self.close()
        except Exception as ex:
            self.dialog_window = QtWidgets.QMessageBox().warning(self, "Выбор отдела",
                                                                 "Выберите отдел!")

    def get_selected_answer(self):
        return self.selected_department


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog_add_user = QtWidgets.QWidget()
    Dialog_add_user.show()

    ui = DialogWidgetSelectDepartment(Dialog_add_user)

    sys.exit(app.exec_())
