from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QHeaderView, QMessageBox

from src.view.widget import my_tree_widget
from src.view.dialog_window.dialog_select_department import DialogWidgetSelectDepartment

import src.controller.controller_main_window as controller


class TreeHierarchy(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(800, 600)

        self.id_departments_for_delete = []
        self.departments_for_added = []
        self.list_hierarchy = []
        self.list_departments = []
        self.list_replacement_departments = []
        self.dialog_window = None

        self.setupUi()
        self.show()

    def setupUi(self):
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        font = QtGui.QFont()
        font.setFamily("Monospac821 BT")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")

        self.treeWidget = my_tree_widget.MyTreeWidget()  # QtWidgets.QTreeWidget(self.frame)
        self.treeWidget.setFont(font)
        self.treeWidget.setObjectName("treeWidget")
        self.init_tree_widget()

        self.gridLayout.addWidget(self.treeWidget, 0, 0, 1, 1)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.button_save = QtWidgets.QPushButton(self.frame_3)
        self.button_save.setFont(font)
        self.button_save.pressed.connect(self.button_save_press)
        self.button_save.setObjectName("button_save")

        self.button_add_row = QtWidgets.QPushButton(self.frame_3)
        self.button_add_row.setFont(font)
        self.button_add_row.pressed.connect(self.button_add_row_press)
        self.button_add_row.setObjectName("button_add_row")

        self.button_delte_row = QtWidgets.QPushButton(self.frame_3)
        self.button_delte_row.setFont(font)
        self.button_delte_row.pressed.connect(self.button_delete_row_press)
        self.button_delte_row.setObjectName("button_delete_row")

        self.horizontalLayout.addWidget(self.button_save)
        self.horizontalLayout.addWidget(self.button_add_row)
        self.horizontalLayout.addWidget(self.button_delte_row)

        self.gridLayout.addWidget(self.frame_3, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.frame)
        self.setCentralWidget(self.centralwidget)

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslate_ui(self, ):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "Номер подразделения"))
        self.treeWidget.header().setResizeContentsPrecision(QHeaderView.ResizeToContents)
        self.treeWidget.headerItem().setText(1, _translate("MainWindow", "Название подразделения"))

        self.button_save.setText(_translate("MainWindow", "сохранить изменения"))
        self.button_add_row.setText(_translate("MainWindow", "добавить элемент"))
        self.button_delte_row.setText(_translate("MainWindow", "удалить элемент"))

    def button_save_press(self):
        def _save_all_data_in_db(main_item):
            self.__add_new_departments()
            controller.change_people_departments(self.list_replacement_departments)
            controller.delete_departments(self.id_departments_for_delete)

            self.make_tree_hierarchy(main_item)
            controller.save_hierarchy(self.list_hierarchy)
            controller.update_data_departments(self.list_departments)

        count_top_lvl = self.treeWidget.topLevelItemCount()
        if count_top_lvl > 1:
            QMessageBox.critical(self, "Ошибка сохранения", "Невозможно сохранить матрицу доступа с несколькими "
                                                            "возглавляющими отделами.\nДолжен быть только один "
                                                            "главный отдел. Составьте матрицу доступа, исходя из этого "
                                                            "правила.")
            return

        main_item = self.treeWidget.topLevelItem(0)
        _save_all_data_in_db(main_item)
        self.__clear_all_lists()
        self.dialog_window = QtWidgets.QMessageBox().information(self, "Сохранение изменений",
                                                                 "Изменеиня успешно сохранены в базе")
        self.init_tree_widget()

    def button_add_row_press(self):
        item_for_added = QtWidgets.QTreeWidgetItem(self.treeWidget.topLevelItem(0))  # добавляется в главный отдел
        item_for_added.setFlags(
            QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsDragEnabled)
        item_for_added.setText(0, "0")
        item_for_added.setText(1, "новое название")
        item_for_added.setText(2, "111")
        self.departments_for_added.append(item_for_added)

    def button_delete_row_press(self):
        def __check_abort_delete(count_selected_items: int):
            if count_selected_items < 1:
                self.dialog_window = QtWidgets.QMessageBox().warning(self, "Удаление информации об отделе",
                                                                     "Для удаления информации об отделе, выделите "
                                                                     "нужный отдел щелчком мыши")
                return True
            if count_selected_items > 1:
                self.dialog_window = QtWidgets.QMessageBox().warning(self, "Удаление информации об отделе",
                                                                     "Для удаления выберите один отдел.")
                return True
            reply = QMessageBox.question(self, 'Подтверждение', 'Вы уверены, что хотите удалить выбранный отдел? '
                                                                'Помимо выбранного отдела, удаляются все подчиняющиеся'
                                                                ' отделы. \n\nДля сохранения изменений после удаления '
                                                                'не забудьте нажать кнопку "сохранить"',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return True

        selected_elements = self.treeWidget.selectedItems()
        if __check_abort_delete(len(selected_elements)):
            return

        self.dialog_window = DialogWidgetSelectDepartment(self)
        self.dialog_window.exec()  # ожидание закрытия диалогового окна
        id_department_for_replace = self.dialog_window.get_selected_answer()

        for element in selected_elements:
            self.__create_deletion_queues(id_department_for_replace, element)
        self.init_tree_widget()

    def __clear_all_lists(self):
        self.list_departments.clear()
        self.list_hierarchy.clear()
        self.list_replacement_departments.clear()
        self.departments_for_added.clear()
        self.id_departments_for_delete.clear()

    def __add_new_departments(self):  # добавляем только новые департаменты. Заменить на массив не получится
        for item in self.departments_for_added:
            try:
                parent_id = int(item.parent().text(2))
            except AttributeError as ex:
                QtWidgets.QMessageBox.critical(self, "Ошибка добавления отдела",
                                               "Невозможно добавить еще один главный отдел. Главный отдел должен быть только один!")
                continue
            id_added_department = controller.add_department(name_department=item.text(1),
                                                            number_department=int(item.text(0)),
                                                            parent_id=parent_id)
            item.setText(2, str(id_added_department))

    def __create_deletion_queues(self, id_department_for_replace, element_for_delete):
        # лист для перевода людей с удаляемого отдела в другой отдел 1 - то, на что меняем; 2 - то, что заменяем
        self.list_replacement_departments.append(
            (id_department_for_replace, int(element_for_delete.text(2))))
        self.id_departments_for_delete.append(int(element_for_delete.text(2)))
        for number_child in range(element_for_delete.childCount()):
            child = element_for_delete.child(number_child)
            self.__create_deletion_queues(id_department_for_replace, child)  # Рекурсия. Подаем потомка итема
        element_for_delete.removeChild(element_for_delete)

    def make_tree_hierarchy(self, item, level_parentage=0):
        def add_all_parents_to_department(current_item, current_level):
            """
            Adds all ancestors for the transferred department to the hierarchy list
            :param current_item:
            :param current_level: nesting level of the transferred item
            :return: None
            """
            while current_item.parent() is not None:
                current_level += 1
                current_item = current_item.parent()
                self.list_hierarchy.append({
                    "department_id": department_id,
                    "parent_id": current_item.text(2),
                    "level": current_level
                })

        department_id = item.text(2)
        self.list_departments.append({
            "number_department": item.text(0),
            "name_department": item.text(1),
            "id": department_id
        })

        parent_id = item.parent().text(2) if item.parent() is not None else None

        if item.parent() is None:  # для самого главного отдела
            self.list_hierarchy.append({
                "department_id": department_id,
                "parent_id": parent_id,
                "level": level_parentage
            })

        add_all_parents_to_department(item, level_parentage)  # добавляем всех предков до самого верхнего уровня

        # рекурсивный вызов для дочерних элементов
        count_children = item.childCount()
        for index_child in range(count_children):
            self.make_tree_hierarchy(item.child(index_child), level_parentage=level_parentage)

    def init_tree_widget(self):
        hierarchy = controller.get_hierarchy()
        self.treeWidget.clear()
        self.treeWidget.addTopLevelItem(
            hierarchy[1]["item"])  # элемент под 1-ым индексом всегда будет главным (так сохраняется в базе данных)
        self.treeWidget.expandAll()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = TreeHierarchy()
    sys.exit(app.exec_())
