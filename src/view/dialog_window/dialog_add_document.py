from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QDialog

from src.controller import controller_main_window as controller


class DialogAddDocument(QDialog):
    def __init__(self, main_window):
        QFileDialog.__init__(self)
        self.name_file = ''
        self.path_to_file = ''
        self.setModal(True)
        self.main_window = main_window
        self.setWindowTitle("добавление документа")
        self.show()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Dialog_add_user")
        self.resize(400, 380)
        self.setMinimumSize(QtCore.QSize(320, 340))
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

        self.label_inner_number = QtWidgets.QLabel(self.main_frame)
        font = QtGui.QFont()
        font.setFamily("Monospac821 BT")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_inner_number.setFont(font)
        self.label_inner_number.setObjectName("label_inner_number")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_inner_number)

        style_for_line_edit = "border: 2px solid;\n" \
                              "border-color: rgb(255, 230, 154);\n" \
                              "border-radius: 5px;\n" \
                              "\n" \
                              ""

        self.lineEdit_inner_number = QtWidgets.QLineEdit(self.main_frame)
        self.lineEdit_inner_number.setMinimumSize(QtCore.QSize(0, 23))
        self.lineEdit_inner_number.setFont(font)
        self.lineEdit_inner_number.setStyleSheet(style_for_line_edit)
        self.lineEdit_inner_number.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_inner_number.setObjectName("lineEdit_inner_number")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_inner_number)

        self.label_output_date = QtWidgets.QLabel(self.main_frame)
        font = QtGui.QFont()
        font.setFamily("Monospac821 BT")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_output_date.setFont(font)
        self.label_output_date.setObjectName("label_output_date")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_output_date)

        self.lineEdit_output_number = QtWidgets.QLineEdit(self.main_frame)
        self.lineEdit_output_number.setObjectName("lineEdit_output_number")
        self.lineEdit_output_number.setStyleSheet(style_for_line_edit)
        self.lineEdit_output_number.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_output_number.setMinimumSize(QtCore.QSize(0, 23))
        self.lineEdit_output_number.setFont(font)

        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_output_number)

        self.label_type_document = QtWidgets.QLabel(self.main_frame)
        self.label_type_document.setFont(font)
        self.label_type_document.setObjectName("label_type_document")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_type_document)

        self.lineEdit_type_document = QtWidgets.QLineEdit(self.main_frame)
        self.lineEdit_type_document.setObjectName("lineEdit_type_document")
        self.lineEdit_type_document.setStyleSheet(style_for_line_edit)
        self.lineEdit_type_document.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_type_document.setMinimumSize(QtCore.QSize(0, 23))
        self.lineEdit_type_document.setFont(font)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_type_document)

        self.label_date = QtWidgets.QLabel(self.main_frame)
        self.label_date.setFont(font)
        self.label_date.setStyleSheet("")
        self.label_date.setObjectName("label_date")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_date)

        self.frame_for_drop = QtWidgets.QFrame(self.main_frame)
        self.frame_for_drop.setAcceptDrops(False)
        self.frame_for_drop.setStyleSheet("background-color: rgb(255, 230, 154);\n"
                                          "border-radius: 5px;\n"
                                          "")
        self.frame_for_drop.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_for_drop.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_for_drop.setObjectName("frame_for_drop")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_for_drop)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.label_name_selected_file = QtWidgets.QLabel(self.frame_for_drop)
        font.setPointSize(9)
        self.label_name_selected_file.setFont(font)
        self.label_name_selected_file.setAlignment(QtCore.Qt.AlignCenter)
        self.label_name_selected_file.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label_name_selected_file)
        font.setPointSize(11)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)

        self.label_plus = QtWidgets.QLabel(self.frame_for_drop)
        font_plus = QtGui.QFont()
        font_plus.setPointSize(40)
        font_plus.setBold(False)
        font_plus.setItalic(False)
        font_plus.setUnderline(False)
        font_plus.setWeight(50)
        font_plus.setStrikeOut(False)
        font_plus.setKerning(True)
        self.label_plus.setFont(font_plus)
        self.label_plus.setAlignment(QtCore.Qt.AlignCenter)
        self.label_plus.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_plus)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)

        self.pushButton_select_file = QtWidgets.QPushButton(self.frame_for_drop)
        self.pushButton_select_file.clicked.connect(self.add_file)
        style_for_button_select_file = "background-color: rgb(255, 210, 76);" \
                                       "border-radius: 5px;\n" \
                                       "padding: 2px;" \
                                       "font-size: 10" \
                                       "\n"
        self.pushButton_select_file.setStyleSheet(style_for_button_select_file)
        self.pushButton_select_file.setFont(font)
        self.pushButton_select_file.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_select_file.setObjectName("pushButton_select_file")
        self.verticalLayout_2.addWidget(self.pushButton_select_file)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.frame_for_drop)

        self.dateEdit = QtWidgets.QDateEdit(self.main_frame)
        self.dateEdit.setStyleSheet(style_for_line_edit)
        self.dateEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.dateEdit.setMinimumSize(QtCore.QSize(0, 23))
        self.dateEdit.setFont(font)
        self.dateEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2020, 1, 1), QtCore.QTime(0, 0, 0)))
        self.dateEdit.setObjectName("dateEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.dateEdit)
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
        self.setWindowTitle(_translate("Dialog_add_user", "Dialog"))
        self.label_inner_number.setText(_translate("Dialog_add_user", "Входящий номер:"))
        self.label_output_date.setText(_translate("Dialog_add_user", "Исходящий номер:"))
        self.label_type_document.setText(_translate("Dialog_add_user", "Тип документа:"))
        self.label_date.setText(_translate("Dialog_add_user", "Исходящая дата:"))
        self.label_name_selected_file.setText(
            _translate("Dialog_add_user", "Выберите файл или перетащите его в эту область"))
        self.label_plus.setText(_translate("Dialog_add_user", "+"))
        self.pushButton_select_file.setText(_translate("Dialog_add_user", "Выбрать файл"))
        self.pushButton_save.setText(_translate("Dialog_add_user", "Сохранить"))
        self.pushButton_cancel.setText(_translate("Dialog_add_user", "Отмена"))

    def add_file(self):
        print("button_click")
        self.path_to_file = QtWidgets.QFileDialog.getOpenFileName()[0]
        self.name_file = self.path_to_file[self.path_to_file.rfind("/") + 1:]
        print(self.path_to_file.rfind("/"))
        self.label_name_selected_file.setText(self.name_file)
        # print(self.path_to_file)

    def push_save_file(self):
        inner_number = self.lineEdit_inner_number.text()
        output_number = self.lineEdit_output_number.text()
        output_date = self.dateEdit.text()
        type_document = self.lineEdit_type_document.text()
        print(inner_number)
        print(output_number)
        print(output_date)
        print(type_document)
        print(self.path_to_file)
        controller.add_document_in_database(self.path_to_file, self.name_file, inner_number, output_number, output_date,
                                            type_document)
        self.close()

    def push_cancel(self):
        self.close()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QWidget()
    main_window.show()

    ui = DialogAddDocument(main_window)

    sys.exit(app.exec_())
