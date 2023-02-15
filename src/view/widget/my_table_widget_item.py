from PyQt5 import QtWidgets


class MyTableWidgetItem(QtWidgets.QTableWidgetItem):
    def __init__(self, obj):
        super().__init__(obj)
        self.__additional_data = None

    def set_additional_data(self, data):
        self.__additional_data = data

    def get_additional_data(self):
        return self.__additional_data
