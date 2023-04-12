from PyQt5 import QtCore, QtGui, QtWidgets

from src.view.widget.my_table_widget_item import MyTableWidgetItem
from src.view.dialog_window import dialog_edit_user
from src.view.dialog_window import dialog_add_user
from src.view.dialog_window import dialog_select_period_registration
from src.controller import controller_main_window as controller


class WidgetSettingUser(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.dialog_window = None
        self.data_about_users = None
        self.setObjectName("MainWindow")
        self.resize(895, 605)
        self.setupUi()
        self.show()

    def setupUi(self):
        self.centralwidget = QtWidgets.QWidget(self)
        font = QtGui.QFont()
        font.setFamily("Monospac821 BT")
        self.centralwidget.setFont(font)
        self.centralwidget.setStyleSheet("background-color: rgb(146, 180, 236);")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_body = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.frame_body.sizePolicy().hasHeightForWidth())
        self.frame_body.setSizePolicy(sizePolicy)
        self.frame_body.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_body.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_body.setObjectName("frame_body")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_body)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_function = QtWidgets.QFrame(self.frame_body)
        self.frame_function.setStyleSheet("")
        self.frame_function.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_function.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_function.setObjectName("frame_function")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_function)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 9)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.pushButton_home = QtWidgets.QPushButton(self.frame_function)
        self.pushButton_home.clicked.connect(self.press_button_home)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_home.sizePolicy().hasHeightForWidth())
        self.pushButton_home.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Monospac821 BT")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)

        self.pushButton_home.setFont(font)
        self.pushButton_home.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_home.setStyleSheet("background-color: rgb(255, 210, 76);\n"
                                           "padding: 5;\n"
                                           "border-radius:5px;\n"
                                           "border: 1 solid black;\n"
                                           "")
        self.pushButton_home.setObjectName("pushButton_home")
        self.horizontalLayout.addWidget(self.pushButton_home)

        self.pushButton_refresh = QtWidgets.QPushButton(self.frame_function)
        self.pushButton_refresh.clicked.connect(self.press_button_refresh)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_refresh.sizePolicy().hasHeightForWidth())
        self.pushButton_refresh.setSizePolicy(sizePolicy)
        self.pushButton_refresh.setFont(font)
        self.pushButton_refresh.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_refresh.setStyleSheet("background-color: rgb(255, 210, 76);\n"
                                              "padding: 5;\n"
                                              "border-radius:5px;\n"
                                              "border: 1 solid black;\n"
                                              "")
        self.pushButton_refresh.setObjectName("pushButton_refresh")
        self.horizontalLayout.addWidget(self.pushButton_refresh)

        self.line_edit_search = QtWidgets.QLineEdit(self.frame_function)
        self.line_edit_search.setPlaceholderText("введите запрос")
        self.line_edit_search.setToolTip("поле для поиска по таблице. По умолчанию поиск производится по всем полям")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_edit_search.sizePolicy().hasHeightForWidth())
        self.line_edit_search.setSizePolicy(sizePolicy)
        self.line_edit_search.setMinimumSize(QtCore.QSize(150, 27))
        self.line_edit_search.setStyleSheet("background-color: rgb(255, 255, 255);"
                                            "border-radius:5px;")
        self.line_edit_search.setObjectName("lineEdit_search")
        self.horizontalLayout.addWidget(self.line_edit_search)

        self.pushButton_find = QtWidgets.QPushButton(self.frame_function)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_find.sizePolicy().hasHeightForWidth())
        self.pushButton_find.clicked.connect(self.press_button_search_users)
        self.pushButton_find.setSizePolicy(sizePolicy)
        self.pushButton_find.setFont(font)
        self.pushButton_find.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_find.setStyleSheet("background-color: rgb(255, 210, 76);\n"
                                           "padding: 5;\n"
                                           "border-radius:5px;\n"
                                           "border: 1 solid black;\n"
                                           "")
        self.pushButton_find.setObjectName("pushButton_find")
        self.horizontalLayout.addWidget(self.pushButton_find)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        self.pushButton_period_search = QtWidgets.QPushButton(self.frame_function)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_period_search.sizePolicy().hasHeightForWidth())
        self.pushButton_period_search.clicked.connect(self.press_button_period)
        self.pushButton_period_search.setSizePolicy(sizePolicy)
        self.pushButton_period_search.setFont(font)
        self.pushButton_period_search.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_period_search.setStyleSheet("background-color: rgb(255, 210, 76);\n"
                                                    "padding: 5;\n"
                                                    "border-radius:5px;\n"
                                                    "border: 1 solid black;\n"
                                                    "")
        self.pushButton_period_search.setObjectName("pushButton_period_search")
        self.horizontalLayout.addWidget(self.pushButton_period_search, 0, QtCore.Qt.AlignVCenter)

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        self.pushButton_add = QtWidgets.QPushButton(self.frame_function)
        self.pushButton_add.clicked.connect(self.press_button_add_user)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_add.sizePolicy().hasHeightForWidth())
        self.pushButton_add.setSizePolicy(sizePolicy)
        self.pushButton_add.setFont(font)
        self.pushButton_add.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_add.setStyleSheet("background-color: rgb(255, 210, 76);\n"
                                          "padding: 5;\n"
                                          "border-radius:5px;\n"
                                          "border: 1 solid black;\n"
                                          "")
        self.pushButton_add.setObjectName("pushButton_add")
        self.horizontalLayout.addWidget(self.pushButton_add)

        self.pushButton_edit = QtWidgets.QPushButton(self.frame_function)
        self.pushButton_edit.clicked.connect(self.press_button_edit_user)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_edit.sizePolicy().hasHeightForWidth())
        self.pushButton_edit.setSizePolicy(sizePolicy)
        self.pushButton_edit.setFont(font)
        self.pushButton_edit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_edit.setStyleSheet("background-color: rgb(255, 210, 76);\n"
                                           "padding: 5;\n"
                                           "border-radius:5px;\n"
                                           "border: 1 solid black;\n"
                                           "")
        self.pushButton_edit.setObjectName("pushButton_edit")
        self.horizontalLayout.addWidget(self.pushButton_edit)

        self.pushButton_delete = QtWidgets.QPushButton(self.frame_function)
        self.pushButton_delete.clicked.connect(self.press_button_delete)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.pushButton_delete.sizePolicy().hasHeightForWidth())
        self.pushButton_delete.setSizePolicy(sizePolicy)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.pushButton_delete.setFont(font)
        self.pushButton_delete.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_delete.setStyleSheet("background-color: rgb(255, 210, 76);\n"
                                             "padding: 5;\n"
                                             "border-radius:5px;\n"
                                             "border: 1 solid black;\n"
                                             "")
        self.pushButton_delete.setObjectName("pushButton_delete")
        self.horizontalLayout.addWidget(self.pushButton_delete)

        self.verticalLayout_2.addWidget(self.frame_function)

        self.tableWidget = QtWidgets.QTableWidget(self.frame_body)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setMinimumSize(QtCore.QSize(877, 498))
        self.tableWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setFont(font)
        self.tableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidget.verticalScrollBar().setSingleStep(3)
        self.tableWidget.horizontalScrollBar().setSingleStep(3)
        self.tableWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tableWidget.setStyleSheet("background-color: rgb(255, 230, 154);\n"
                                       "border-radius: 10;")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(8)
        # self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.verticalLayout_2.addWidget(self.tableWidget)
        self.gridLayout.addWidget(self.frame_body, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        self.press_button_refresh()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_home.setText(_translate("MainWindow", "главная"))
        self.pushButton_refresh.setText(_translate("MainWindow", "обновить"))
        self.pushButton_find.setText(_translate("MainWindow", "искать"))
        self.pushButton_period_search.setText(_translate("MainWindow", "период"))
        self.pushButton_add.setText(_translate("MainWindow", "добавить"))
        self.pushButton_edit.setText(_translate("MainWindow", "редактировать"))
        self.pushButton_delete.setText(_translate("MainWindow", "актив/деактив"))

        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Фамилия"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Имя"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Отчество"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Логин"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Дата регистрации"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Номер отдела"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Добавил в базу"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Деактивирован"))

    def press_button_add_user(self):
        print("pushed_button_add_document")
        self.dialog_window = dialog_add_user.DialogWidgetAddUser(self)

    def press_button_refresh(self):
        self.pushButton_period_search.setText("период")
        self.data_about_users = controller.get_data_about_users()
        # print(self.data_about_users)
        self.fill_in_table(self.data_about_users)

    def press_button_home(self):
        self.pushButton_period_search.setText("период")
        self.fill_in_table(self.data_about_users)

    def fill_in_table(self, data_about_users):
        if data_about_users is None:
            self.dialog_window = QtWidgets.QMessageBox().critical(self, "Ошибка", "Данные отсутствуют.")
            return False
        self.tableWidget.setRowCount(len(data_about_users))
        number_row = 0
        for row in data_about_users:
            # print(row)
            name_item = MyTableWidgetItem(row[1])
            name_item.set_additional_data(int(row[0]))  # Установка id

            self.tableWidget.setItem(number_row, 0, name_item)  # Установка фамилии
            self.tableWidget.setItem(number_row, 1, QtWidgets.QTableWidgetItem(row[2]))  # Установка имени
            self.tableWidget.setItem(number_row, 2, QtWidgets.QTableWidgetItem(row[3]))  # Установка отчества
            self.tableWidget.setItem(number_row, 3, QtWidgets.QTableWidgetItem(row[4]))  # Установка логина
            self.tableWidget.setItem(number_row, 4,
                                     QtWidgets.QTableWidgetItem(str(row[5])))  # Установка даты регистрации
            self.tableWidget.setItem(number_row, 5, QtWidgets.QTableWidgetItem(str(row[6])))  # Установка номера отдела
            creator = f"{row[7]} {row[8]} {row[9]}"
            self.tableWidget.setItem(number_row, 6, QtWidgets.QTableWidgetItem(creator))  # Установка создателя
            status_active = "" if row[10] else "Деактивирован"
            self.tableWidget.setItem(number_row, 7, QtWidgets.QTableWidgetItem(status_active))  # Уст. статуса деакитива

            number_row += 1
        print("init table users finished")
        return True

    def press_button_delete(self):
        items = self.tableWidget.selectedItems()
        if len(items) == 8:
            controller.change_activation_status(items[0].get_additional_data())
            self.dialog_window = QtWidgets.QMessageBox()
            if items[7].text() == "":
                title = "Деактивация пользователя"
                message = "успешно деактивирован"
            else:
                title = "Активация пользователя"
                message = "успешно активирован"
            self.dialog_window.information(self, title,
                                           f'Пользователь "{items[0].text()} {items[1].text()} {items[2].text()}" '
                                           f'{message}.')
            self.press_button_refresh()

        else:
            self.dialog_window = QtWidgets.QMessageBox().warning(self, "Изменение статуса активности пользователя",
                                                                 "Для изменения статуса активности пользователя "
                                                                 "выделите всю строку (строка станет белой), щелкнув "
                                                                 "по номеру строки (крайний левый стоблец).")

    def press_button_edit_user(self):
        items = self.tableWidget.selectedItems()
        if len(items) == 8:
            id_user = items[0].get_additional_data()
            self.dialog_window = dialog_edit_user.DialogWidgetEditUser(self, items[0].text(), items[1].text(),
                                                                       items[2].text(), int(items[5].text()),
                                                                       items[3].text(), id_user)
        else:
            self.dialog_window = QtWidgets.QMessageBox().warning(self, "Редактирование пользователя",
                                                                 "Для редактирования пользователя выделите всю строку "
                                                                 "(строка станет белой), щелкнув по номеру строки "
                                                                 "(крайний левый стоблец).")

    def press_button_search_users(self):
        self.pushButton_period_search.setText("период")
        self.result_searching = controller.search_users(self.line_edit_search.text())
        flag_result = self.fill_in_table(self.result_searching)
        if not flag_result:
            QtWidgets.QMessageBox().information(self, "Результат поиска", f'По запросу "{self.line_edit_search.text()}"'
                                                                          f' не найдено результатов')

    def press_button_period(self):
        self.dialog_window = dialog_select_period_registration.DialogSelectPeriodRegistration(self, "user")


if __name__ == "__main__":
    import sys

    # app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    # ui = WidgetDocuments()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    # sys.exit(app.exec_()

    app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    ui = WidgetSettingUser()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    sys.exit(app.exec_())
