import os
import hashlib
import time
from datetime import datetime

from src.model.config import config
from src.model.for_data_base import db_helper
from src.model.for_data_base import db_helper_for_hierarchy_derartments

current_user_session_id = 1
current_access_level = 0  # 0 - super admin; 1 - admin; 2 - just user


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

    # print(len(str(password)))
    # print(len(str(salt)))
    # this get id for division_number
    id_department = db_helper_for_hierarchy_derartments.get_id_department(int(division_number))
    id_user = db_helper.add_record_user_data(last_name, name, patronymic, id_department, current_user_session_id,
                                             datetime.now().strftime("%d-%m-%Y %H:%M"))
    # id = db_helper.get_id_user(last_name, name, patronymic)
    db_helper.add_record_user_login(password.hex(), salt.hex(), id_user, login, 2)
    print(f"\nUser {last_name} {name} added in data base\n")


def delete_user(last_name: str, name: str, patronymic: str):
    db_helper.delete_user(last_name, name, patronymic)


def check_password(login: str, password: str):  # переписать под проверку в двух таблицах
    request = db_helper.get_password(login)
    # print("request =", request)
    global current_user_session_id, current_access_level
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
            print(f"This user with username '{login}' login successful")
            # global current_id, current_access_level
            current_user_session_id, current_access_level = id_and_access_level
            print("lvl = ", current_access_level)
            return current_access_level
        else:
            print(f"User {login} no login")
            return False


def create_super_admin():
    password = 'super'
    salt = os.urandom(16)
    key1 = hashlib.pbkdf2_hmac(
        config.HASH_FUNCTION,
        password.encode('utf-8'),
        salt,
        200000,
        dklen=64
    )
    db_helper.add_record_admin_data("super admin", "super admin", "super", datetime.now())
    db_helper.add_record_admin_login(key1.hex(), salt.hex(), 1, "super", 0)


def delete_file():
    pass


def add_document(path_to_document: str, name_document: str, inner_number: str, output_number: str, output_date,
                 type_document: str):
    id_documents = db_helper.add_data_about_document(inner_number, output_number, output_date, name_document,
                                                     datetime.now().strftime("%d-%m-%Y %H:%M"),
                                                     current_user_session_id, type_document)
    file = open(path_to_document, 'rb')
    db_helper.add_file(id_documents, file.read())


def edit_document(id_document, name_document: str, inner_number: str, output_number: str, output_date,
                  type_document: str):
    db_helper.edit_document(id_document, name_document, inner_number, output_number, output_date, type_document)


def get_data_about_documents():
    return db_helper.get_data_documents_for_department(1)


def download_document(id_document: int, path_to_save: str):
    data_file = db_helper.get_file_by_id(id_document)
    file = open(path_to_save, 'wb')
    file.write(bytes(data_file))
    file.close()


def get_data_about_users():
    data = db_helper.get_data_about_users(2)  # for getting data about admin enter 1
    return data


if __name__ == '__main__':
    # # add_user("super admin", "super admin", "superAdminovich", "235", "superAdmin", "password")
    # start_time = time.time()
    # # create_super_admin()
    #
    # # add_user("test_name", "test", "test", "235", "login", "privetik")
    # # add_user("user1", "user1", "user1", "401", "login1", "user1")
    #
    # # test_binary()
    #
    # check_password("login", "privetik")
    # check_password("login1", "user1")
    # check_password("vanya", "vavak")
    # print(time.time() - start_time, "seconds")
    # # delete_user("test_name", "test", "test")
    # # time = datetime.now()
    # # print(datetime.now().strftime("%d-%m-%Y %H:%M"))
    create_super_admin()
