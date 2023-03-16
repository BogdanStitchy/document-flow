import hashlib
from datetime import datetime

from src.model.config import config
from src.model.for_data_base import db_helper


class User:
    def __init__(self):
        self.LVL_ACCESS = 2
        self.CURRENT_ID: int = None

    def get_lvl_access(self):
        return self.LVL_ACCESS

    def check_password(self, login: str, password: str):  # переписать под проверку в двух таблицах
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
                print(f"This user with username '{login}' login successful")
                # global current_id, current_access_level
                self.CURRENT_ID, current_access_level = id_and_access_level
                print("lvl = ", current_access_level)
                return 'user'
            else:
                print(f"User {login} no login")
                return False

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

    @staticmethod
    def get_data_about_documents():
        return db_helper.get_data_documents_for_department(1)

    @staticmethod
    def download_document(id_document: int, path_to_save: str):
        data_file = db_helper.get_file_by_id(id_document)
        file = open(path_to_save, 'wb')
        file.write(bytes(data_file))
        file.close()
