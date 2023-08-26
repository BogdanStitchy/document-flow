import src.model.for_data_base.db_helper_for_hierarchy_derartments as db_helper
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5 import QtCore


class Hierarchy:
    """
    Class needs to get and preparation data about hierarchy from a database.
    """

    def __init__(self):
        self.__departments = {}

    def get_data_about_departments(self):
        """
        Get preparation data about hierarchy for QTreeWidget.

        :return: {id(int): {"item": value(QTreeWidgetItem), "name": value(str), "number_department": value(int)}}
        """
        self.__set_naming_all_departments()
        self.__set_hierarchy_departments()
        return self.__departments

    def __set_naming_all_departments(self):
        result = db_helper.get_all_departments()
        print("__set_naming_all_departments reult =\t", result)
        for row in result:
            self.__departments[row[0]] = {"item": QTreeWidgetItem(), "name": row[1], "number_department": row[2]}
            self.__departments[row[0]]["item"].setFlags(
                QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsDragEnabled)
            self.__departments[row[0]]["item"].setText(0, str(row[2]))  # установка номера отдела на итем
            self.__departments[row[0]]["item"].setText(1, str(row[1]))  # установка имени на итем
            self.__departments[row[0]]["item"].setText(2, str(row[0]))  # установка id на итем

    def __set_hierarchy_departments(self):
        hierarchy = db_helper.get_hierarchy()
        for dependence in hierarchy:
            if dependence[1] is None:
                continue
            self.__departments[dependence[1]]["item"].addChild(self.__departments[dependence[0]]["item"])


def add_department_in_db(name_department: str, number_department: int):
    return db_helper.add_department(name_department, number_department)


def delete_department_in_db(id_department: int):
    db_helper.delete_department(id_department)


def update_data_departments(list_departments: list):
    db_helper.update_data_departments(list_departments)


if __name__ == '__main__':
    hr = Hierarchy()
    print(hr.get_data_about_departments())


def create_hierarchy(list_hierarchy: list):
    db_helper.create_hierarchy(list_hierarchy)


def change_people_departments(list_replacement_departments: list):
    db_helper.change_people_departments(list_replacement_departments)
