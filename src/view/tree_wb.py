from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QHeaderView

from src.view.widget import my_tree_widget


class TreeHierarchy(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.resize(800, 600)
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

        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        # item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)

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

        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "Номер отдела"))
        self.treeWidget.header().setResizeContentsPrecision(QHeaderView.ResizeToContents)
        # size = QSize()
        # size.setWidth(400)
        # self.treeWidget.headerItem().setSizeHint(1, size)
        self.treeWidget.headerItem().setText(1, _translate("MainWindow", "Название отдела"))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(1, _translate("MainWindow",
                                                              "Заместитель генерального деректора по безопасности"))
        self.treeWidget.topLevelItem(0).setText(0, _translate("MainWindow", "zgdb"))

        self.treeWidget.topLevelItem(0).child(0).setText(0, _translate("MainWindow", "235"))
        self.treeWidget.topLevelItem(0).child(0).setText(1, _translate("MainWindow", "Управление безопасности"))

        self.treeWidget.topLevelItem(0).child(0).child(0).setText(0, _translate("MainWindow", "400"))
        self.treeWidget.topLevelItem(0).child(0).child(0).setText(1, _translate("MainWindow",
                                                                                "Отдел экономической безопасности"))

        self.treeWidget.topLevelItem(0).child(0).child(1).setText(0, _translate("MainWindow", "401"))
        self.treeWidget.topLevelItem(0).child(0).child(1).setText(1, _translate("MainWindow",
                                                                                "Отдел информационной безопасности"))

        self.treeWidget.topLevelItem(0).child(0).child(2).setText(0, _translate("MainWindow", "402"))
        self.treeWidget.topLevelItem(0).child(0).child(2).setText(1, _translate("MainWindow",
                                                                                "Отдел по обеспечению физической и информационной техническиой защиты ЯО"))

        # self.treeWidget.topLevelItem(0).child(0).child(1).setText(0, _translate("MainWindow", "403"))
        self.treeWidget.topLevelItem(0).child(1).setText(0, _translate("MainWindow", "260"))
        self.treeWidget.topLevelItem(0).child(1).setText(1, _translate("MainWindow",
                                                                       "Бюро противодействия иностранным техническим разведкам"))

        self.treeWidget.topLevelItem(0).child(2).setText(0, _translate("MainWindow", "291"))
        self.treeWidget.topLevelItem(0).child(2).setText(1, _translate("MainWindow", "Бюро специальной связи"))

        self.treeWidget.topLevelItem(0).child(3).setText(0, _translate("MainWindow", "236"))
        self.treeWidget.topLevelItem(0).child(3).setText(1, _translate("MainWindow", "Режимно-секретный отдел"))

        self.treeWidget.topLevelItem(0).child(4).setText(0, _translate("MainWindow", "117"))
        self.treeWidget.topLevelItem(0).child(4).setText(1,
                                                         _translate("MainWindow", "Отдел мобилизационной подготовки"))

        self.treeWidget.topLevelItem(0).child(5).setText(0, _translate("MainWindow", "237"))
        self.treeWidget.topLevelItem(0).child(5).setText(1, _translate("MainWindow", "Отдел ГО и ЧС"))

        self.treeWidget.setSortingEnabled(__sortingEnabled)

        self.button_save.setText(_translate("MainWindow", "сохранить изменения"))
        self.button_add_row.setText(_translate("MainWindow", "добавить элемент"))
        self.button_delte_row.setText(_translate("MainWindow", "удалить элемент"))

    def button_save_press(self):
        print(self.treeWidget.topLevelItemCount())
        for i in range(self.treeWidget.topLevelItemCount()):  # количество элементов верхнего уровня
            item = self.treeWidget.topLevelItem(i)  # элемент верхнего уровня, находящийся по индексу
            print(type(item))
            # print(item.text(0))  # текст элемента в указанном столбце
            self.tree(item)

    def button_add_row_press(self):
        print("push button")
        item_for_adedd = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_for_adedd.setFlags(
            QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsDragEnabled)
        item_for_adedd.setText(0, "номер")
        item_for_adedd.setText(1, "новое название")
        self.treeWidget.addTopLevelItem(item_for_adedd)

    def button_delete_row_press(self):
        # index = self.treeWidget.currentIndex().row()
        selected_elements = self.treeWidget.selectedItems()
        print(selected_elements)
        for element in selected_elements:
            self.treeWidget.removeItemWidget(element, 0)
        # self.treeWidget.removeItemWidget()
        # item = model.item(index)
        # print(item.text())

    def tree(self, item):
        text = item.text(0)
        print(f"{text}", end="")
        if item.parent() is not None:
            print(f"\tparent: {item.parent().text(0)}")
        print()
        count_children = item.childCount()
        for index_child in range(count_children):
            self.tree(item.child(index_child))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    ui = TreeHierarchy()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    sys.exit(app.exec_())
