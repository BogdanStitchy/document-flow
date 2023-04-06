from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog

from src.controller import controller_main_window as controller


class DialogSelectDate(QDialog):

    def __init__(self, main_window):
        QDialog.__init__(self)
        self.setModal(True)
        self.main_window = main_window
        self.flag_success_exit = False
        self.show()
        self.setupUi()

    def setupUi(self):
        font = QtGui.QFont()
        font.setFamily("Monospac821 BT")
        font.setPointSize(9)
        # font.setBold(True)
        font.setWeight(75)

        font_dash = QtGui.QFont()
        font_dash.setPointSize(15)

        style_for_date_edit = "border: 2px solid;\n" \
                              "border-color: rgb(255, 230, 154);\n" \
                              "border-radius: 2px;\n" \
                              "\n"

        self.setObjectName("Dialog")
        self.resize(454, 225)
        self.setStyleSheet("background-color: rgb(146, 180, 236);")
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        self.frame_date_output = QtWidgets.QFrame(self)
        self.frame_date_output.setEnabled(False)
        self.frame_date_output.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_date_output.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_date_output.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_date_output.setObjectName("frame_date_output")

        self.gridLayout_date_output = QtWidgets.QGridLayout(self.frame_date_output)
        self.gridLayout_date_output.setObjectName("gridLayout_2")

        self.label_date_output = QtWidgets.QLabel(self.frame_date_output)
        self.label_date_output.setFont(font)
        self.label_date_output.setMinimumSize(QtCore.QSize(220, 0))
        self.label_date_output.setObjectName("label_date_output")
        self.gridLayout_date_output.addWidget(self.label_date_output, 0, 0, 1, 1)

        self.dateEdit_start_date_output = QtWidgets.QDateEdit(self.frame_date_output)
        self.dateEdit_start_date_output.setFont(font)
        self.dateEdit_start_date_output.setStyleSheet(style_for_date_edit)
        self.dateEdit_start_date_output.setToolTip("день.месяц.год")
        self.dateEdit_start_date_output.setMinimumSize(QtCore.QSize(125, 0))
        self.dateEdit_start_date_output.setDateTime(QtCore.QDateTime(QtCore.QDate(2010, 1, 1), QtCore.QTime(0, 0, 0)))
        self.dateEdit_start_date_output.setObjectName("dateEdit_start_date_output")
        self.gridLayout_date_output.addWidget(self.dateEdit_start_date_output, 0, 1, 1, 1)

        self.label_dash_output = QtWidgets.QLabel(self.frame_date_output)
        self.label_dash_output.setMaximumSize(QtCore.QSize(20, 16777215))
        self.label_dash_output.setFont(font_dash)
        self.label_dash_output.setAlignment(QtCore.Qt.AlignCenter)
        self.label_dash_output.setObjectName("label_dash_output")
        self.gridLayout_date_output.addWidget(self.label_dash_output, 0, 2, 1, 1)

        self.dateEdit_end_date_output = QtWidgets.QDateEdit(self.frame_date_output)
        self.dateEdit_end_date_output.setFont(font)
        self.dateEdit_end_date_output.setStyleSheet(style_for_date_edit)
        self.dateEdit_end_date_output.setToolTip("день.месяц.год")
        self.dateEdit_end_date_output.setMinimumSize(QtCore.QSize(125, 0))
        self.dateEdit_end_date_output.setDateTime(QtCore.QDateTime(QtCore.QDate(2030, 1, 1), QtCore.QTime(0, 0, 0)))
        self.dateEdit_end_date_output.setObjectName("dateEdit_end_date_output")
        self.gridLayout_date_output.addWidget(self.dateEdit_end_date_output, 0, 3, 1, 1)

        self.gridLayout.addWidget(self.frame_date_output, 1, 2, 1, 3)

        self.frame_date_download = QtWidgets.QFrame(self)
        self.frame_date_download.setEnabled(False)
        self.frame_date_download.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_date_download.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_date_download.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_date_download.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_date_download.setObjectName("frame_date_download")

        self.gridLayout_date_download = QtWidgets.QGridLayout(self.frame_date_download)
        self.gridLayout_date_download.setObjectName("gridLayout_3")

        self.label_date_download = QtWidgets.QLabel(self.frame_date_download)
        self.label_date_download.setFont(font)
        self.label_date_download.setMinimumSize(QtCore.QSize(220, 0))
        self.label_date_download.setObjectName("label_date_download")
        self.gridLayout_date_download.addWidget(self.label_date_download, 0, 0, 1, 1)

        self.dateEdit_start_date_download = QtWidgets.QDateEdit(self.frame_date_download)
        self.dateEdit_start_date_download.setFont(font)
        self.dateEdit_start_date_download.setStyleSheet(style_for_date_edit)
        self.dateEdit_start_date_download.setToolTip("день.месяц.год")
        self.dateEdit_start_date_download.setMinimumSize(QtCore.QSize(125, 0))
        self.dateEdit_start_date_download.setDateTime(QtCore.QDateTime(QtCore.QDate(2022, 1, 1), QtCore.QTime(0, 0, 0)))
        self.dateEdit_start_date_download.setObjectName("dateEdit_start_date_download")
        self.gridLayout_date_download.addWidget(self.dateEdit_start_date_download, 0, 1, 1, 1)

        self.label_dash_download = QtWidgets.QLabel(self.frame_date_download)
        self.label_dash_download.setMaximumSize(QtCore.QSize(20, 16777215))
        self.label_dash_download.setFont(font_dash)
        self.label_dash_download.setAlignment(QtCore.Qt.AlignCenter)
        self.label_dash_download.setObjectName("label_dash_download")
        self.gridLayout_date_download.addWidget(self.label_dash_download, 0, 2, 1, 1)

        self.dateEdit_end_date_download = QtWidgets.QDateEdit(self.frame_date_download)
        self.dateEdit_end_date_download.setFont(font)
        self.dateEdit_end_date_download.setStyleSheet(style_for_date_edit)
        self.dateEdit_end_date_download.setToolTip("день.месяц.год")
        self.dateEdit_end_date_download.setMinimumSize(QtCore.QSize(125, 0))
        self.dateEdit_end_date_download.setDateTime(QtCore.QDateTime(QtCore.QDate(2030, 1, 1), QtCore.QTime(0, 0, 0)))
        self.dateEdit_end_date_download.setObjectName("dateEdit_end_date_download")
        self.gridLayout_date_download.addWidget(self.dateEdit_end_date_download, 0, 3, 1, 1)
        self.gridLayout.addWidget(self.frame_date_download, 2, 2, 1, 3)

        self.label_select_param = QtWidgets.QLabel(self)
        self.label_select_param.setFont(font)
        self.label_select_param.setMinimumSize(QtCore.QSize(145, 0))
        self.label_select_param.setObjectName("label_select_param")
        self.gridLayout.addWidget(self.label_select_param, 0, 2, 1, 1)

        self.pushButton_apply = QtWidgets.QPushButton(self)
        self.pushButton_apply.clicked.connect(self.apply_params_period)
        self.pushButton_apply.setFont(font)
        self.pushButton_apply.setStyleSheet("background-color: rgb(255, 210, 76);\n"
                                            "border-radius: 5px;\n"
                                            "\n"
                                            "")
        self.pushButton_apply.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_apply.setObjectName("pushButton_apply")
        self.gridLayout.addWidget(self.pushButton_apply, 3, 4, 1, 1)

        self.checkBox_date_output = QtWidgets.QCheckBox(self)
        self.checkBox_date_output.stateChanged.connect(self.click_date_output)
        self.checkBox_date_output.setFont(font)
        self.checkBox_date_output.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.checkBox_date_output.setChecked(True)
        self.checkBox_date_output.setObjectName("checkBox_2_date_output")
        self.gridLayout.addWidget(self.checkBox_date_output, 0, 3, 1, 1)

        self.checkBox_date_download = QtWidgets.QCheckBox(self)
        self.checkBox_date_download.stateChanged.connect(self.click_date_download)
        self.checkBox_date_download.setFont(font)
        self.checkBox_date_download.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.checkBox_date_download.setObjectName("checkBox_date_download")
        self.gridLayout.addWidget(self.checkBox_date_download, 0, 4, 1, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle("Выбор периода поиска")
        self.checkBox_date_output.setText(_translate("Dialog", "Исходящая дата"))
        self.label_date_output.setText(_translate("Dialog", "Исходящая дата (д.м.г):"))
        self.label_dash_output.setText(_translate("Dialog", "-"))
        self.label_date_download.setText(_translate("Dialog", "Дата загрузки в систему (д.м.г):"))
        self.label_dash_download.setText(_translate("Dialog", "-"))
        self.label_select_param.setText(_translate("Dialog", "Параметры периода:"))
        self.checkBox_date_download.setText(_translate("Dialog", "Дата загрузки в систему"))
        self.pushButton_apply.setText(_translate("Dialog", "Применить"))

    def click_date_output(self):
        if self.checkBox_date_output.isChecked():
            self.frame_date_output.setEnabled(True)
        else:
            self.frame_date_output.setEnabled(False)

    def click_date_download(self):
        if self.checkBox_date_download.isChecked():
            self.frame_date_download.setEnabled(True)
        else:
            self.frame_date_download.setEnabled(False)

    def apply_params_period(self):
        if not self.checkBox_date_output.isChecked() and not self.checkBox_date_download.isChecked():
            QtWidgets.QMessageBox.critical(self, "Ошибка периода", "Необходимо выбрать параметры париода!")
            return
        res = controller.apply_period_searching_documents(flag_date_output=self.checkBox_date_output.isChecked(),
                                                          flag_date_download=self.checkBox_date_download.isChecked(),
                                                          start_date_output=self.dateEdit_start_date_output.text(),
                                                          end_date_output=self.dateEdit_end_date_output.text(),
                                                          start_date_download=self.dateEdit_start_date_download.text(),
                                                          end_date_download=self.dateEdit_end_date_download.text())
        self.set_new_name_main_window_button()
        self.close()
        if len(res) > 0:
            self.main_window.fill_in_table(res)
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка периода", "Данные в заданном периоде не найдены")

    def set_new_name_main_window_button(self):
        new_name_button_period = ""
        if self.checkBox_date_output.isChecked() & self.checkBox_date_download.isChecked():
            new_name_button_period = f"исходящая:{self.dateEdit_start_date_output.text()}-" \
                                     f"{self.dateEdit_end_date_output.text()}\n" \
                                     f"загрузки:{self.dateEdit_start_date_download.text()}-" \
                                     f"{self.dateEdit_end_date_download.text()}"
        elif self.checkBox_date_output.isChecked():
            new_name_button_period = f"исходящая:{self.dateEdit_start_date_output.text()}-" \
                                     f"{self.dateEdit_end_date_output.text()}"
        elif self.checkBox_date_download.isChecked():
            new_name_button_period = f"загрузки:{self.dateEdit_start_date_download.text()}-" \
                                     f"{self.dateEdit_end_date_download.text()}"
        self.main_window.pushButton_period_search.setText(new_name_button_period)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog_add_user = QtWidgets.QWidget()
    Dialog_add_user.show()

    ui = DialogSelectDate(Dialog_add_user)

    sys.exit(app.exec_())
