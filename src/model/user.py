import hashlib
import os
from datetime import datetime
import datetime

from src.model.config import config
from src.model.for_data_base import db_helper
from src.model.for_data_base import db_helper_for_hierarchy_derartments as db_helper_departments


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

    def get_lvl_access(self):
        return self.LVL_ACCESS

    def get_login(self):
        return self.CURRENT_LOGIN

    def get_full_name(self):
        return f"{self.CURRENT_LAST_NAME} {self.CURRENT_NAME} {self.CURRENT_PATRONYMIC}"

    def get_number_department(self):
        return self.CURRENT_NUMBER_DEPARTMENT

    def set_full_name(self):
        self.CURRENT_LAST_NAME, self.CURRENT_NAME, self.CURRENT_PATRONYMIC = db_helper.get_full_name_user(
            self.CURRENT_ID)

    def set_department_data(self):
        self.CURRENT_ID_DEPARTMENT, self.CURRENT_NUMBER_DEPARTMENT = db_helper.get_data_department_for_one_user(
            self.CURRENT_ID)

    def check_password(self, login: str, password: str):
        request = db_helper.get_password_user(login)
        # print("request =", request)
        # global current_user_session_id, current_access_level
        # print(f"current id = {current_id}\tcurrent access lvl = {current_access_level}")
        if request is None:
            print("User not found in data base.")
        else:
            print("User found in data base")
            received_password, salt, *id_and_access_level = request
            # print("id_and_access_level = ", id_and_access_level)
            # print('\n')
            # print("rp = ", bytes(received_password))
            # print("original_salt = ", bytes(original_salt.hex(), 'utf-8'))
            # print("salt = ", bytes(salt))
            # print('\n')

            password = hashlib.pbkdf2_hmac(
                config.HASH_FUNCTION,
                password.encode('utf-8'),
                bytes(salt),
                200000,
                dklen=64
            )

            # print("passwordik = ", passwordik.hex().encode('utf-8'))
            if password.hex().encode('utf-8') == bytes(received_password):
                self.CURRENT_LOGIN = login
                print(f"This user with username '{login}' login successful")
                self.CURRENT_ID, current_access_level = id_and_access_level
                self.set_full_name()
                self.set_department_data()
                print("lvl = ", current_access_level)
                return 'user'
            else:
                print(f"User {login} no login")
                return False

    def change_password(self, password: str):
        # self.CURRENT_ID = 5
        if self.check_password(self.CURRENT_LOGIN, password) == "user":
            return False  # старый и новый пароли сходятся
        salt = os.urandom(16)
        password = hashlib.pbkdf2_hmac(
            config.HASH_FUNCTION,
            password.encode('utf-8'),
            bytes(salt.hex(), 'utf-8'),
            200000,
            dklen=64
        )
        db_helper.changes_password_user(self.CURRENT_ID, password.hex(), salt.hex(),
                                        datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))
        return True

    def get_last_change_password(self):
        # self.CURRENT_ID = 6
        return db_helper.get_last_change_password_user(self.CURRENT_ID)

    def delete_file(self):
        pass

    def add_document(self, path_to_document: str, name_document: str, inner_number: str, output_number: str,
                     output_date,
                     type_document: str):
        id_documents = db_helper.add_data_about_document(inner_number, output_number, output_date, name_document,
                                                         datetime.now().strftime("%d-%m-%Y %H:%M"),
                                                         self.CURRENT_ID, type_document)
        file = open(path_to_document, 'rb')
        db_helper.add_file(id_documents, file.read())

    @staticmethod
    def edit_document(id_document, name_document: str, inner_number: str, output_number: str, output_date,
                      type_document: str):
        db_helper.edit_document(id_document, name_document, inner_number, output_number, output_date, type_document)

    def get_data_about_documents(self):
        print("self.CURRENT_ID_DEPARTMENT = ", self.CURRENT_ID_DEPARTMENT)
        print("USER")
        access_id_departments = db_helper_departments.get_id_children_department(self.CURRENT_ID_DEPARTMENT)
        return db_helper.get_data_documents_for_user(access_id_departments)  # self.CURRENT_ID_DEPARTMENT)

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
