import os
from datetime import datetime
import datetime

from src.config import tools
from src.model.for_data_base import db_helper
from src.model.for_data_base import db_helper_for_hierarchy_derartments as db_helper_departments

from src.db.methods.user_db_methods import UserDB

from src.model.custom_exceptions import ClientPasswordError, ClientActiveError, ClientNotFoundError


class User:
    def __init__(self):
        self.LVL_ACCESS = 2
        self.CURRENT_ID: int = None
        self.CURRENT_NAME: str = None
        self.CURRENT_LAST_NAME: str = None
        self.CURRENT_PATRONYMIC: str = None
        self.CURRENT_LOGIN: str = None
        self.CURRENT_ID_DEPARTMENT: int = None
        self.CURRENT_NUMBER_DEPARTMENT: int = None
        self.date_last_changes_password = None

    def get_lvl_access(self):
        return self.LVL_ACCESS

    def get_login(self):
        return self.CURRENT_LOGIN

    def get_full_name(self):
        return f"{self.CURRENT_LAST_NAME} {self.CURRENT_NAME} {self.CURRENT_PATRONYMIC}"

    def get_number_department(self):
        return self.CURRENT_NUMBER_DEPARTMENT

    def set_self_data(self, data_user: {}, login_user: str):
        self.CURRENT_LOGIN = login_user
        self.CURRENT_ID = data_user['id']
        self.CURRENT_NAME = data_user['name']
        self.CURRENT_PATRONYMIC = data_user['patronymic']
        self.CURRENT_LAST_NAME = data_user['last_name']
        self.date_last_changes_password = data_user['date_last_changes_password']

    def set_department_data(self):
        self.CURRENT_ID_DEPARTMENT, self.CURRENT_NUMBER_DEPARTMENT = db_helper.get_data_department_for_one_user(
            self.CURRENT_ID)

    def check_password(self, login: str, password: str):
        """
        checks user authentication

        :param login: user login
        :param password: user password
        :return: True if login success, else False
        """
        data_user: {} = UserDB.check_password(login)

        if data_user is None:
            raise ClientNotFoundError("Пользователь с указанным логином не найден в базе!\n"
                                      "Проверьте логин и выбранную роль пользователя")

        if not data_user['active']:
            raise ClientActiveError("Учетная запись пользователя с указанными данными деактивирована.\n"
                                    "Для активации учетной записи обратитесь к администратору.")

        password = tools.create_hash_password(password, data_user['salt'])

        if password != bytes(data_user['password']):
            raise ClientPasswordError("Указан неправильный пароль")

        # user successful login in system
        self.set_self_data(data_user=data_user, login_user=login)
        self.set_department_data()
        return 'user'

    def change_password(self, password: str):
        # self.CURRENT_ID = 5
        if self.check_password(self.CURRENT_LOGIN, password) == "user":
            return False  # старый и новый пароли сходятся
        salt = os.urandom(16)
        password = tools.create_hash_password(password, salt)
        db_helper.changes_password_user(self.CURRENT_ID, password.hex(), salt.hex(),
                                        datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))
        return True

    def check_needs_password_change(self):
        # self.CURRENT_ID = 6
        change = UserDB.get_last_change_password_admin(self.CURRENT_ID)
        if change is None:
            return True
        delta_date = datetime.datetime.now() - change
        if delta_date.days > 180:
            return True
        else:
            return False  # пароль не надо менять
        # return db_helper.get_last_change_password_user(self.CURRENT_ID)

    def delete_file(self):
        pass

    def add_document(self, path_to_document: str, name_document: str, inner_number: str, output_number: str,
                     output_date,
                     type_document: str):
        id_documents = db_helper.add_data_about_document(inner_number, output_number, output_date, name_document,
                                                         datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
                                                         self.CURRENT_ID, type_document)
        file = open(path_to_document, 'rb')
        db_helper.add_file(id_documents, file.read())

    @staticmethod
    def edit_document(id_document, name_document: str, inner_number: str, output_number: str, output_date,
                      type_document: str):
        db_helper.edit_document(id_document, name_document, inner_number, output_number, output_date, type_document)

    def get_data_about_documents(self):
        # print("self.CURRENT_ID_DEPARTMENT = ", self.CURRENT_ID_DEPARTMENT)
        # print("USER")
        access_id_departments = db_helper_departments.get_id_children_department(self.CURRENT_ID_DEPARTMENT)
        return db_helper.get_data_documents_for_user(access_id_departments)  # self.CURRENT_ID_DEPARTMENT)

    def search_string_in_documents(self, search_string: str):
        access_id_departments = db_helper_departments.get_id_children_department(self.CURRENT_ID_DEPARTMENT)
        return db_helper.search_string_in_documents_for_user(access_id_departments, search_string)

    def apply_period_searching_documents(self, flag_date_output: bool, flag_date_download: bool,
                                         start_date_output: str = None, end_date_output: str = None,
                                         start_date_download: str = None, end_date_download: str = None):
        access_id_departments = db_helper_departments.get_id_children_department(self.CURRENT_ID_DEPARTMENT)
        return db_helper.apply_period_searching_for_user(access_id_departments, flag_date_output, flag_date_download,
                                                         start_date_output=start_date_output,
                                                         end_date_output=end_date_output,
                                                         start_date_download=start_date_download,
                                                         end_date_download=end_date_download)

    @staticmethod
    def download_document(id_document: int, path_to_save: str):
        data_file = db_helper.get_file_by_id(id_document)
        file = open(path_to_save, 'wb')
        file.write(bytes(data_file))
        file.close()

    def check_password_strength(self, password: str):
        """
        Function for check security password.
        If password was security function return True, else return password vulnerability report.

        :param password: str
        :return: True, if the password is secure, else message (str) password vulnerability
        """

        # Проверяем длину пароля
        if len(password) < 12:
            return "Пароль должен содержать больше 12 символов"

        # Проверяем наличие хотя бы одной цифры
        if not any(char.isdigit() for char in password):
            return "Пароль должен содержать хотя бы одну цифру"

        # Проверяем наличие хотя бы одной буквы в верхнем регистре
        if not any(char.isupper() for char in password):
            return "Пароль должен содержать хотя бы одну заглавнуюю букву"

        # Проверяем наличие хотя бы одной буквы в нижнем регистре
        if not any(char.islower() for char in password):
            return "Пароль должен содержать хотя бы одну прописную букву"

        # Проверяем наличие хотя бы одного специального символа
        special_chars = """!@#$%^&*()_+-={}|[]\:;"'<>?,./"""
        if not any(char in special_chars for char in password):
            return f"Пароль должен содержать хотя бы один специальный символ ({special_chars})"

        # Проверяем на сходство с логином
        if password == self.CURRENT_LOGIN:
            return "Пароль не должен сходится с логином"

        # Если все проверки пройдены, то пароль сильный
        return True


if __name__ == '__main__':
    user = User()
    # user.change_password("Ivan")
    print(user.check_password_strength("Ghbdtasdfsad1@"))
