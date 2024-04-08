from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog

from src.controller import controller_main_window as controller


class DialogEditDocument(QDialog):
    def __init__(self, main_window, id_document: int, name_document: str, inner_number: str, output_number: str,
                 type_document: str,
                 date: QtCore.QDate):
        super().__init__()
        self.dialog_window = None
        self.id_document = id_document
        self.name_file = name_document
        self.inner_number = inner_number
        self.output_number = output_number
        self.type_document = type_document
        self.date = QtCore.QDate(date)
        self.setModal(True)
        self.main_window = main_window
        self.show()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Dialog_add_user")
        self.resize(500, 250)
        self.setMinimumSize(QtCore.QSize(320, 200))
        self.setMaximumSize(QtCore.QSize(1100, 1000))
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

        font = QtGui.QFont()
        font.setFamily("Monospac821 BT")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)

        self.label_name_document = QtWidgets.QLabel(self.main_frame)
        self.label_name_document.setText(self.name_file)
        self.label_name_document.setFont(font)
        self.label_name_document.setStyleSheet("")
        self.label_name_document.setObjectName("label_date")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_name_document)

        self.label_inner_number = QtWidgets.QLabel(self.main_frame)
        self.label_inner_number.setFont(font)
        self.label_inner_number.setObjectName("label_inner_number")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_inner_number)

        style_for_line_edit = "border: 2px solid;\n" \
                              "border-color: rgb(255, 230, 154);\n" \
                              "border-radius: 5px;\n" \
                              "\n" \
                              ""

        self.lineEdit_inner_number = QtWidgets.QLineEdit(self.main_frame)
        self.lineEdit_inner_number.setText(self.inner_number)
        self.lineEdit_inner_number.setMinimumSize(QtCore.QSize(0, 23))
        self.lineEdit_inner_number.setFont(font)
        self.lineEdit_inner_number.setStyleSheet(style_for_line_edit)
        self.lineEdit_inner_number.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_inner_number.setObjectName("lineEdit_inner_number")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_inner_number)

        self.label_output_date = QtWidgets.QLabel(self.main_frame)
        font = QtGui.QFont()
        font.setFamily("Monospac821 BT")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_output_date.setFont(font)
        self.label_output_date.setObjectName("label_output_date")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_output_date)

        self.lineEdit_output_number = QtWidgets.QLineEdit(self.main_frame)
        self.lineEdit_output_number.setText(self.output_number)
        self.lineEdit_output_number.setObjectName("lineEdit_output_number")
        self.lineEdit_output_number.setStyleSheet(style_for_line_edit)
        self.lineEdit_output_number.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_output_number.setMinimumSize(QtCore.QSize(0, 23))
        self.lineEdit_output_number.setFont(font)

        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_output_number)

        self.label_type_document = QtWidgets.QLabel(self.main_frame)
        self.label_type_document.setFont(font)
        self.label_type_document.setObjectName("label_type_document")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_type_document)

        self.lineEdit_type_document = QtWidgets.QLineEdit(self.main_frame)
        self.lineEdit_type_document.setText(self.type_document)
        self.lineEdit_type_document.setObjectName("lineEdit_type_document")
        self.lineEdit_type_document.setStyleSheet(style_for_line_edit)
        self.lineEdit_type_document.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_type_document.setMinimumSize(QtCore.QSize(0, 23))
        self.lineEdit_type_document.setFont(font)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_type_document)

        self.label_date = QtWidgets.QLabel(self.main_frame)
        self.label_date.setFont(font)
        self.label_date.setStyleSheet("")
        self.label_date.setObjectName("label_date")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_date)

        self.dateEdit = QtWidgets.QDateEdit(self.main_frame)
        self.dateEdit.setDate(self.date)
        self.dateEdit.setStyleSheet(style_for_line_edit)
        self.dateEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.dateEdit.setMinimumSize(QtCore.QSize(0, 23))
        self.dateEdit.setFont(font)
        self.dateEdit.setObjectName("dateEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.dateEdit)
        self.verticalLayout.addWidget(self.main_frame)

        self.pushButton_save = QtWidgets.QPushButton(self)
        self.pushButton_save.clicked.connect(self.push_save_file)
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
        self.pushButton_cancel.clicked.connect(self.push_cancel)
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
        self.setWindowTitle("Редактирование документа")
        self.label_inner_number.setText(_translate("Dialog_add_user", "Входящий номер:"))
        self.label_output_date.setText(_translate("Dialog_add_user", "Исходящий номер:"))
        self.label_type_document.setText(_translate("Dialog_add_user", "Тип документа:"))
        self.label_date.setText(_translate("Dialog_add_user", "Исходящая дата:"))
        self.pushButton_save.setText(_translate("Dialog_add_user", "Сохранить"))
        self.pushButton_cancel.setText(_translate("Dialog_add_user", "Отмена"))

    def push_save_file(self):
        inner_number = self.lineEdit_inner_number.text()
        output_number = self.lineEdit_output_number.text()
        output_date = self.dateEdit.text()
        type_document = self.lineEdit_type_document.text()

        controller.edit_document(self.id_document, self.name_file, inner_number, output_number, output_date,
                                 type_document)
        self.main_window.press_button_refresh()
        self.dialog_window = QtWidgets.QMessageBox.information(self, "редактирование документа",
                                                               f'Документ "{self.name_file}" успешно отредактирован.\n'
                                                               f'Список документов обновлен')

        self.close()

    def push_cancel(self):
        self.close()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QWidget()
    main_window.show()

    ui = DialogEditDocument(main_window)

    sys.exit(app.exec_())
