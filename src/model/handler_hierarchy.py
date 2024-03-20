from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5 import QtCore


class Hierarchy:
    """
    Class needs to get and preparation data about hierarchy from a database.
    """

    def __init__(self, departments: [{}, {}], hierarchy: [{}, {}]):
        self.__departments_returning = {}
        self.__departments_received = departments
        self.__hierarchy = hierarchy

    def get_data_about_departments(self):
        """
        Get preparation data about hierarchy for QTreeWidget.

        :return: {id(int): {"item": value(QTreeWidgetItem), "name": value(str), "number_department": value(int)}}
        """
        self.__set_naming_all_departments()
        self.__set_hierarchy_departments()
        return self.__departments_returning

    def __set_naming_all_departments(self):
        for row in self.__departments_received:
            self.__departments_returning[row.id] = {"item": QTreeWidgetItem(), "name": row.name_department,
                                                    "number_department": row.number_department}
            self.__departments_returning[row.id]["item"].setFlags(
                QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsDragEnabled)
            self.__departments_returning[row.id]["item"].setText(0,
                                                                 str(row.number_department))  # установка номера отдела на итем
            self.__departments_returning[row.id]["item"].setText(1, str(row.name_department))  # установка имени на итем
            self.__departments_returning[row.id]["item"].setText(2, str(row.id))  # установка id на итем

    def __set_hierarchy_departments(self):
        for dependence in self.__hierarchy:
            if dependence.parent_id is None:
                continue
            self.__departments_returning[dependence.parent_id]["item"].addChild(
                self.__departments_returning[dependence.department_id]["item"])


if __name__ == '__main__':
    hr = Hierarchy()
    print(hr.get_data_about_departments())
