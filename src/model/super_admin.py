import os
from datetime import datetime

from src.config import tools
from src.model import handler_hierarchy

from src.model.administrator import Administrator
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
    def get_role():
        return "superAdmin"

    # -------------------------------------admin manipulation-------------------------------------------------------
    @staticmethod
    def add_admin(last_name: str, name: str, patronymic: str, login: str, password: str):
        tools.check_params_empty(locals().values())
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
    def apply_period_registration_admins(start_date_creating: str, end_date_creating: str):
        start_date_creating = datetime.strptime(start_date_creating, "%d.%m.%Y")
        end_date_creating = datetime.strptime(end_date_creating, "%d.%m.%Y")
        return SuperAdminMethodsDB.find_admins_period(start_date_creating, end_date_creating)
        # return db_helper.apply_period_searching_registration_admins(start_date_download, end_date_download)

    @staticmethod
    def change_activation_status_admin(id_admin: int):
        SuperAdminMethodsDB.change_admin_activity_status(id_admin)

    @staticmethod
    def edit_admin_data(id_admin: int, last_name: str, name: str, patronymic: str, login: str, password: str):
        data_for_update = {"last_name": last_name, "name": name, "patronymic": patronymic, "login": login}
        tools.check_params_empty(data_for_update.values())

        if password != '':
            salt = os.urandom(16)
            password = tools.create_hash_password(password, salt)
            data_for_update["salt"] = salt
            data_for_update["password"] = password
        SuperAdminMethodsDB.edit_admin(id_admin, **data_for_update)

    # -------------------------------------department manipulation------------------------------------------------------
    @staticmethod
    def add_department(name_department: str, number_department: int, parent_id: int or None) -> int:
        id_added_department = SuperAdminMethodsDB.add_department(name_department, number_department)
        SuperAdminMethodsDB.add_one_hierarchy_department(id_added_department, parent_id)
        return id_added_department

    @staticmethod
    def save_hierarchy(list_hierarchy: list):
        SuperAdminMethodsDB.create_full_hierarchy(list_hierarchy)

    @staticmethod
    def delete_departments(id_departments_for_delete: list):
        SuperAdminMethodsDB.delete_departments(id_departments_for_delete)

    @staticmethod
    def update_data_departments(list_departments: list):
        SuperAdminMethodsDB.update_all_departments(list_departments)

    @staticmethod
    def change_people_departments(list_replacement_departments: list):
        SuperAdminMethodsDB.update_user_departments(list_replacement_departments)

    @staticmethod
    def get_hierarchy():
        departments = SuperAdminMethodsDB.get_all_departments()
        hierarchy = SuperAdminMethodsDB.get_full_hierarchy_departments()
        hierarchy = handler_hierarchy.Hierarchy(departments, hierarchy)
        return hierarchy.get_data_about_departments()

    @staticmethod
    def get_all_departments_without_one(id_exempt_department: int):
        return SuperAdminMethodsDB.get_all_departments_without_one(id_exempt_department)
