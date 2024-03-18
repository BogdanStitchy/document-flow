from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog

from src.controller import controller_main_window as controller


class DialogSelectPeriodRegistration(QDialog):

    def __init__(self, main_window, param_searching: str):
        QDialog.__init__(self)
        self.setModal(True)
        self.main_window = main_window
        self.param_searching = param_searching
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

        self.frame_date_download = QtWidgets.QFrame(self)
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

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle("Выбор периода поиска")
        self.label_date_download.setText(_translate("Dialog", "Дата регистрации (д.м.г):"))
        self.label_dash_download.setText(_translate("Dialog", "-"))
        self.pushButton_apply.setText(_translate("Dialog", "Применить"))

    def apply_params_period(self):
        if self.param_searching == "admin":
            res = controller.apply_period_registration_admins(self.dateEdit_start_date_download.text(),
                                                              self.dateEdit_end_date_download.text())
        else:
            res = controller.apply_period_searching_registration_users(self.dateEdit_start_date_download.text(),
                                                                       self.dateEdit_end_date_download.text())
        self.close()

        if len(res) < 1:
            QtWidgets.QMessageBox.warning(self, "Ошибка периода", "Данные в заданном периоде не найдены")

        self.set_new_name_main_window_button()
        self.main_window.fill_in_table(res)

    def set_new_name_main_window_button(self):
        new_name_button_period = f"период:{self.dateEdit_start_date_download.text()}-" \
                                 f"{self.dateEdit_end_date_download.text()}"
        self.main_window.pushButton_period_search.setText(new_name_button_period)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog_add_user = QtWidgets.QWidget()
    Dialog_add_user.show()

    ui = DialogSelectPeriodRegistration(Dialog_add_user, "admin")

    sys.exit(app.exec_())
