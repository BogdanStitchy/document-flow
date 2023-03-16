import os
import hashlib
from datetime import datetime
from src.model.config import config

from src.model.administrator import Administrator
from src.model.for_data_base import db_helper


class SuperAdmin(Administrator):
    def __init__(self):
        super().__init__()
        self.LVL_ACCESS = 0

    @staticmethod
    def add_admin(last_name, name, patronymic, login, password):
        salt = os.urandom(16)
        password = hashlib.pbkdf2_hmac(
            config.HASH_FUNCTION,
            password.encode('utf-8'),
            bytes(salt),
            200000,
            dklen=64
        )

        id_admin = db_helper.add_record_admin_data(last_name, name, patronymic,
                                                   datetime.now().strftime("%d-%m-%Y %H:%M"))

        db_helper.add_record_admin_login(password.hex(), salt.hex(), id_admin, login, 1,
                                         datetime.now().strftime("%d-%m-%Y %H:%M"))

    @staticmethod
    def get_data_about_admins():
        return db_helper.get_data_about_admins()

    @staticmethod
    def delete_admin(id_admin: int):
        db_helper.delete_admin(id_admin)

    @staticmethod
    def edit_admin_data(id_admin, last_name, name, patronymic, login, password, flag_edit_login):
        db_helper.edit_data_admin(last_name, name, patronymic, id_admin)

        if password != "":
            salt = os.urandom(16)
            password = hashlib.pbkdf2_hmac(
                config.HASH_FUNCTION,
                password.encode('utf-8'),
                bytes(salt.hex(), 'utf-8'),
                200000,
                dklen=64
            )
            db_helper.edit_admin_login_data(login, password.hex(), salt.hex(), id_admin)
        elif flag_edit_login:
            db_helper.edit_only_login_admin(login, id_admin)
