import os
import hashlib
import time
from datetime import datetime

from src.model.config import config
from src.model.for_data_base import db_helper

current_id = 0
current_access_level = -1


# original_salt = b'\xb1LS\xd6)\x9eZ\xbfT\xbd\x94\xa9\x86\xf9\x8bm'


def test_binary():
    salt = os.urandom(16)
    print(salt)
    hsalt = salt.hex()
    print(hsalt)
    print(bytes(hsalt, 'utf-8'))
    print(bytes(hsalt, 'utf-8') == bytes(salt.hex(), 'utf-8'))


def add_user(last_name: str, name: str, patronymic: str, division_number: str, login: str, password: str):
    salt = os.urandom(16)
    original_salt = salt  # (salt.hex(), 'utf-8')
    print("original salt = ", salt)
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

    print(len(str(password)))
    print(len(str(salt)))
    db_helper.add_record_user_data(last_name, name, patronymic, division_number, current_id, datetime.now())
    id = db_helper.get_id_user(last_name, name, patronymic)
    db_helper.create_departments(password.hex(), salt.hex(), id, login, 0)
    print(f"\nUser {last_name} {name} added in data base\n")


def delete_user(last_name: str, name: str, patronymic: str):
    db_helper.delete_user(last_name, name, patronymic)


def check_password(login: str, password: str):
    request = db_helper.get_password(login)
    # print("request =", request)
    global current_id, current_access_level
    print(f"current id = {current_id}\tcurrent access lvl = {current_access_level}")
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
            # print(f"wwwwwwwUser {login} login")
            # global current_id, current_access_level
            current_id, current_access_level = id_and_access_level
            return True
        else:
            print(f"User {login} no login")
            return False


def create_super_admin():
    password = 'password'
    salt = os.urandom(16)
    key1 = hashlib.pbkdf2_hmac(
        config.HASH_FUNCTION,
        password.encode('utf-8'),
        salt,
        200000,
        dklen=64
    )
    db_helper.add_record_user_data("super admin", "super admin", "superAdminovich", "235", "0", datetime.now())
    db_helper.create_departments(key1.hex(), salt.hex(), 1, "superAdmin", 2)


def delete_file():
    pass


if __name__ == '__main__':
    # add_user("super admin", "super admin", "superAdminovich", "235", "superAdmin", "password")
    start_time = time.time()
    # create_super_admin()
    # add_user("test_name", "test", "test", "333", "login", "privetik")
    # add_user("user1", "user1", "user1", "333", "login1", "user1")
    # test_binary()
    check_password("login", "privetik")
    check_password("login1", "user1")
    print(time.time() - start_time, "seconds")
    # delete_user("test_name", "test", "test")
