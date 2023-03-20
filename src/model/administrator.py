import os
import hashlib
from datetime import datetime
from src.model.config import config

from src.model.user import User
from src.model.for_data_base import db_helper
from src.model.for_data_base import db_helper_for_hierarchy_derartments


class Administrator(User):
    def __init__(self):
        super().__init__()
        self.LVL_ACCESS = 1

    def check_password(self, login: str, password: str):
        request = db_helper.get_password_admin(login)

        if request is None:
            print("Admin not found in data base.")
        else:
            print("Admin found in data base")
            received_password, salt, *id_and_access_level = request

            password = hashlib.pbkdf2_hmac(
                config.HASH_FUNCTION,
                password.encode('utf-8'),
                bytes(salt),
                200000,
                dklen=64
            )

            if password.hex().encode('utf-8') == bytes(received_password):
                print(f"This Admin with username '{login}' login successful")
                # global current_id, current_access_level
                self.CURRENT_ID, current_access_level = id_and_access_level
                if current_access_level == 0:
                    return 'superAdmin'
                print("lvl = ", current_access_level)
                return 'admin'
            else:
                print(f"Admin {login} no login")
                return False

    def change_password(self, password: str):
        # self.CURRENT_ID = 5
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

    @staticmethod
    def get_data_about_users():
        data = db_helper.get_data_about_users(2)  # for getting data about admin enter 1
        return data

    def add_user(self, last_name: str, name: str, patronymic: str, division_number: str, login: str, password: str):
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
        id_department = db_helper_for_hierarchy_derartments.get_id_department(int(division_number))
        id_user = db_helper.add_record_user_data(last_name, name, patronymic, id_department, self.CURRENT_ID,
                                                 datetime.now().strftime("%d-%m-%Y %H:%M"))
        # id_user = 14
        db_helper.add_record_user_login(password.hex(), salt.hex(), id_user, login, 2)
        print(f"\nUser {last_name} {name} added in data base\n")

    @staticmethod
    def edit_user_data(last_name: str, name: str, patronymic: str, division_number: str, login: str, password: str,
                       id_user,
                       flag_edit_login: bool):
        id_department = db_helper_for_hierarchy_derartments.get_id_department(int(division_number))
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
    def delete_user(id_user: int):
        db_helper.delete_user(id_user)


if __name__ == '__main__':
    admin = Administrator()
    # admin.add_user("Степкин", "Степан", "Степанович", "235", "stepa", "password")
    admin.check_password("Nura@hr.ru", "Nura")
