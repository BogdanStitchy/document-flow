import os
from src.config import tools

from src.model.administrator import Administrator
from src.model.for_data_base import db_helper
from src.db.methods.super_admin_db_methods import SuperAdminMethodsDB


class SuperAdmin(Administrator):
    def __init__(self):
        super().__init__()
        self.LVL_ACCESS = 0
        self.CURRENT_ID = 1
        self.CURRENT_LAST_NAME = "Супер"
        self.CURRENT_NAME = "Админ"
        self.CURRENT_PATRONYMIC = "СА"

    @staticmethod
    def add_admin(last_name: str, name: str, patronymic: str, login: str, password: str):
        salt = os.urandom(16)
        password = tools.create_hash_password(password, salt)
        SuperAdminMethodsDB.add_admin(name, patronymic, last_name, login, password, salt)

    @staticmethod
    def get_data_about_admins():
        # return db_helper.get_data_about_admins()
        return SuperAdminMethodsDB.get_all_admins()

    @staticmethod
    def search_string_in_admins(search_string: str):
        return SuperAdminMethodsDB.find_admins_words(search_string)

    @staticmethod
    def change_activation_status_admin(id_admin: int):
        SuperAdminMethodsDB.change_admin_activity_status(id_admin)

    @staticmethod
    def add_department(name_department: str, number_department: int, parent_id: int or None):
        id_added_department = SuperAdminMethodsDB.add_department(name_department, number_department)
        SuperAdminMethodsDB.add_one_hierarchy_department(id_added_department, parent_id)

    @staticmethod
    def edit_admin_data(id_admin, last_name, name, patronymic, login, password, flag_edit_login):
        raise "Нужно изменить метод обновления"
        # EDIT!!!
        db_helper.edit_data_admin(last_name, name, patronymic, id_admin)

        if password != "":
            salt = os.urandom(16)
            password = tools.create_hash_password(password, salt)
            db_helper.edit_admin_login_data(login, password.hex(), salt.hex(), id_admin)
        elif flag_edit_login:
            db_helper.edit_only_login_admin(login, id_admin)
