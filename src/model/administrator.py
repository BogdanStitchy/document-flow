import os
import hashlib
from datetime import datetime
from src.config import config

from src.model.user import User
from src.model.for_data_base import db_helper
from src.model.for_data_base import db_helper_for_hierarchy_derartments
from src.db.methods.admin_db_methods import AdminDB
from src.model.custom_exceptions import ClientActiveError, ClientPasswordError, ClientNotFoundError


class Administrator(User):
    def __init__(self):
        super().__init__()
        self.LVL_ACCESS = 1
        self.date_last_changes_password = None
        # self.CURRENT_ID_DEPARTMENT = 1

    def set_self_data(self, data_admin: {}, login_admin: str):
        self.CURRENT_LOGIN = login_admin
        self.CURRENT_ID = data_admin['id']
        self.CURRENT_NAME = data_admin['name']
        self.CURRENT_PATRONYMIC = data_admin['patronymic']
        self.CURRENT_LAST_NAME = data_admin['last_name']
        self.date_last_changes_password = data_admin['date_last_changes_password']

    def check_password(self, login: str, password: str):
        # request = db_helper.get_login_data_admin(login)
        data_about_admin: {} = AdminDB.check_password(login)

        if data_about_admin is None:
            raise ClientNotFoundError("Администратор с указанным логином не найден в базе!\n"
                                      "Проверьте логин и выбранную роль пользователя")

        if not data_about_admin['active']:
            raise ClientActiveError("Учетная запись администратора с указанными данными деактивирована.\n"
                                    "Для активации учетной записи обратитесь к супер администратору.")

        password = hashlib.pbkdf2_hmac(
            config.HASH_FUNCTION,
            password.encode('utf-8'),
            bytes(data_about_admin["salt"]),
            200000,
            dklen=64
        )

        if password != bytes(data_about_admin['password']):
            raise ClientPasswordError("Указан неправильный пароль")

        # admin successful login in system
        self.set_self_data(data_admin=data_about_admin, login_admin=login)

        if data_about_admin['super_admin_flag']:
            return 'superAdmin'
        return 'admin'

    # отказаться
    def get_last_change_password(self):
        # self.CURRENT_ID = 6
        return db_helper.get_last_change_password_admin(self.CURRENT_ID)

    def change_password(self, password: str):
        # self.CURRENT_ID = 5
        if self.check_password(self.CURRENT_LOGIN, password) == 'admin' or 'superAdmin':
            return False
        salt = os.urandom(16)
        password = hashlib.pbkdf2_hmac(
            config.HASH_FUNCTION,
            password.encode('utf-8'),
            bytes(salt.hex(), 'utf-8'),
            200000,
            dklen=64
        )
        db_helper.changes_password_admin(self.CURRENT_ID, password.hex(), salt.hex(),
                                         datetime.now().strftime("%d-%m-%Y %H:%M"))
        return True

    def get_data_about_documents(self):
        return db_helper.get_data_documents_for_admin()

    @staticmethod
    def search_string_in_documents(search_string: str):
        return db_helper.search_string_in_documents_for_admin(search_string)

    @staticmethod
    def search_string_in_users(search_string: str):
        return db_helper.search_string_in_users(search_string)

    @staticmethod
    def search_string_in_admins(search_string: str):
        return db_helper.search_string_in_admins(search_string)

    def apply_period_searching_documents(self, flag_date_output: bool, flag_date_download: bool,
                                         start_date_output: str = None, end_date_output: str = None,
                                         start_date_download: str = None, end_date_download: str = None):
        return db_helper.apply_period_searching_documents_for_admin(flag_date_output, flag_date_download,
                                                                    start_date_output=start_date_output,
                                                                    end_date_output=end_date_output,
                                                                    start_date_download=start_date_download,
                                                                    end_date_download=end_date_download)

    @staticmethod
    def apply_period_registration_admins(start_date_download: str, end_date_download: str):
        return db_helper.apply_period_searching_registration_admins(start_date_download, end_date_download)

    @staticmethod
    def apply_period_registration_users(start_date_download: str, end_date_download: str):
        return db_helper.apply_period_searching_registration_users(start_date_download, end_date_download)

    @staticmethod
    def get_data_about_users():
        data = db_helper.get_data_about_users(2)  # for getting data about admin enter 1
        return data

    def add_user(self, last_name: str, name: str, patronymic: str, division_number: str, login: str, password: str,
                 flag_leader: bool):
        salt = os.urandom(16)
        # original_salt = salt  # (salt.hex(), 'utf-8')
        # print("original salt = ", salt)
        # password = 'password'
        # password2 = 'passworasdgasdgsdfgsdfhsdfhd'
        # start_time = time.time()
        # # print(config.HASH_FUNCTION)
        # key1 = hashlib.pbkdf2_hmac(
        #     config.HASH_FUNCTION,
        #     password.encode('utf-8'),
        #     salt,
        #     200000,
        #     dklen=64
        # )
        # key2 = hashlib.pbkdf2_hmac(
        #     config.HASH_FUNCTION,
        #     password2.encode('utf-8'),
        #     salt,
        #     200000,
        #     dklen=64
        # )
        password = hashlib.pbkdf2_hmac(
            config.HASH_FUNCTION,
            password.encode('utf-8'),
            bytes(salt.hex(), 'utf-8'),
            200000,
            dklen=64
        )

        # print(len(str(password)))
        # print(len(str(salt)))
        # this get id for division_number
        id_department = db_helper_for_hierarchy_derartments.get_id_department_by_department_number(int(division_number))
        id_user = db_helper.add_record_user_data(last_name, name, patronymic, id_department, self.CURRENT_ID,
                                                 datetime.now().strftime("%d-%m-%Y %H:%M"))
        # id_user = 14
        db_helper.add_record_user_login(password.hex(), salt.hex(), id_user, login, 2, flag_leader)
        print(f"\nUser {last_name} {name} added in data base\n")

    @staticmethod
    def edit_user_data(last_name: str, name: str, patronymic: str, division_number: str, login: str, password: str,
                       id_user,
                       flag_edit_login: bool):
        id_department = db_helper_for_hierarchy_derartments.get_id_department_by_department_number(int(division_number))
        db_helper.edit_data_user(last_name, name, patronymic, id_department, id_user)

        if password != "":
            salt = os.urandom(16)
            password = hashlib.pbkdf2_hmac(
                config.HASH_FUNCTION,
                password.encode('utf-8'),
                bytes(salt.hex(), 'utf-8'),
                200000,
                dklen=64
            )
            db_helper.edit_user_login_data(login, password.hex(), salt.hex(), id_user)
        elif flag_edit_login:
            db_helper.edit_only_login_user(login, id_user)

    @staticmethod
    def change_activation_status(id_user: int):
        # db_helper.delete_user(id_user)
        db_helper.change_activation_status_user(id_user)


if __name__ == '__main__':
    admin = Administrator()
    admin.check_password("Nur.ru", "Nur")
