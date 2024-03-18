import os
from datetime import datetime
import pydantic

from src.config import tools
from src.model.user import User
from src.model.for_data_base import db_helper
from src.db.methods.admin_db_methods import AdminMethodsDB
from src.model.custom_exceptions import ClientActiveError, ClientPasswordError, ClientNotFoundError


class Administrator(User):
    def __init__(self):
        super().__init__()
        self.LVL_ACCESS = 1
        self.date_last_changes_password = None
        # self.CURRENT_ID_DEPARTMENT = 1

    @staticmethod
    def get_role():
        return "admin"

    def set_self_data(self, data_admin: {}, login_admin: str):
        self.CURRENT_LOGIN = login_admin
        self.CURRENT_ID = data_admin['id']
        self.CURRENT_NAME = data_admin['name']
        self.CURRENT_PATRONYMIC = data_admin['patronymic']
        self.CURRENT_LAST_NAME = data_admin['last_name']
        self.date_last_changes_password = data_admin['date_last_changes_password']

    def check_password(self, login: str, password: str):
        """
        checks admin authentication

        :param login: admin login
        :param password: admin password
        :return: True if login success, else False
        """
        data_about_admin: {} = AdminMethodsDB.check_password(login)

        if data_about_admin is None:
            raise ClientNotFoundError("Администратор с указанным логином не найден в базе!\n"
                                      "Проверьте логин и выбранную роль пользователя")

        if not data_about_admin['active']:
            raise ClientActiveError("Учетная запись администратора с указанными данными деактивирована.\n"
                                    "Для активации учетной записи обратитесь к супер администратору.")

        password = tools.create_hash_password(password, data_about_admin["salt"])

        if password != bytes(data_about_admin['password']):
            raise ClientPasswordError("Указан неправильный пароль")

        # admin successful login in system
        self.set_self_data(data_admin=data_about_admin, login_admin=login)

        if data_about_admin['super_admin_flag']:
            return 'superAdmin'
        return 'admin'

    def check_needs_password_change(self):
        change = AdminMethodsDB.get_last_change_password_admin(self.CURRENT_ID)
        if change is None:
            return True
        delta_date = datetime.datetime.now() - change
        if delta_date.days > 180:
            return True
        else:
            return False  # пароль не надо менять

    def change_password(self, password: str):
        # self.CURRENT_ID = 5
        try:
            if self.check_password(self.CURRENT_LOGIN, password) == 'admin' or 'superAdmin':
                return False  # старый и новый пароли совпали
        except ClientPasswordError:
            pass
        salt = os.urandom(16)
        password = tools.create_hash_password(password, salt)
        AdminMethodsDB.change_password(self.CURRENT_ID, password, salt, datetime.now().strftime("%d-%m-%Y %H:%M"))
        return True  # пароль изменен

    @staticmethod
    def get_data_about_documents():
        return AdminMethodsDB.get_all_documents()

    @staticmethod
    def edit_document(id_document: int, name_document: str, inner_number: str, output_number: str, output_date,
                      type_document: str):
        AdminMethodsDB.edit_document(id_document, name=name_document, inner_number=inner_number,
                                     output_number=output_number, output_date=output_date, type_document=type_document)
        # db_helper.edit_document(id_document, name_document, inner_number, output_number, output_date, type_document)

    @staticmethod
    def delete_document(id_document: int):
        AdminMethodsDB.delete_document(id_document)

    @staticmethod
    def search_string_in_documents(search_string: str):
        # return db_helper.search_string_in_documents_for_admin(search_string)
        return AdminMethodsDB.find_documents_words(search_string)

    @staticmethod
    def search_string_in_users(search_string: str):
        # return db_helper.search_string_in_users(search_string)
        return AdminMethodsDB.find_users_words(search_string)

    def apply_period_searching_documents(self, flag_date_output: bool, flag_date_download: bool,
                                         start_date_output: str = None, end_date_output: str = None,
                                         start_date_download: str = None, end_date_download: str = None):

        if start_date_output:
            start_date_output = datetime.strptime(start_date_output, "%d.%m.%Y")
        if end_date_output:
            end_date_output = datetime.strptime(end_date_output, "%d.%m.%Y")
        if start_date_download:
            start_date_download = datetime.strptime(start_date_download, "%d.%m.%Y")
        if end_date_download:
            end_date_download = datetime.strptime(end_date_download, "%d.%m.%Y")

        return AdminMethodsDB.find_documents_period(flag_date_output, flag_date_download,
                                                    start_output_date=start_date_output,
                                                    end_output_date=end_date_output,
                                                    start_create_date=start_date_download,
                                                    end_create_date=end_date_download
                                                    )

    @staticmethod
    def apply_period_registration_users(start_date_download: str, end_date_download: str):
        start_date_download = datetime.strptime(start_date_download, "%d.%m.%Y")
        end_date_download = datetime.strptime(end_date_download, "%d.%m.%Y")
        return AdminMethodsDB.find_users_period(start_date_download, end_date_download)

    @staticmethod
    def get_data_about_users():
        return AdminMethodsDB.get_all_users()

    @pydantic.validate_call
    def add_user(self, last_name: str, name: str, patronymic: str, login: str, password: str,
                 id_department: int):
        tools.check_params_empty(locals().values(),
                                 message_error="Переданы пустые аргументы для добавления пользователя")
        salt = os.urandom(16)
        password = tools.create_hash_password(password, salt)

        AdminMethodsDB.add_user_db(last_name, name, patronymic, login, password, salt, id_department, self.CURRENT_ID)

    @staticmethod
    def edit_user_data(last_name: str, name: str, patronymic: str, login: str, password: str, id_user: int,
                       id_department: int):
        data_for_update = {"last_name": last_name, "name": name, "patronymic": patronymic, "login": login,
                           "id_department": id_department}
        tools.check_params_empty(data_for_update.values())

        if password != '':
            salt = os.urandom(16)
            password = tools.create_hash_password(password, salt)
            data_for_update["salt"] = salt
            data_for_update["password"] = password
        AdminMethodsDB.edit_user(id_user, **data_for_update)

    @staticmethod
    def change_activation_status(id_user: int):
        AdminMethodsDB.change_user_activity_status(id_user)
        # db_helper.change_activation_status_user(id_user)


if __name__ == '__main__':
    admin = Administrator()
    admin.check_password("Nur.ru", "Nur")
