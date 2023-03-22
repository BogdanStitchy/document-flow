import src.model.for_data_base.db_helper as db_helper_for_documents_and_users
# from src.model import admin
# from src.model.main_model import Client
from src.model import handler_hierarchy
from src.model.user import User
from src.model.administrator import Administrator
from src.model.super_admin import SuperAdmin

client = SuperAdmin  # Client("admin").client
role_client: str = ""


def check_login(login: str, password: str, role: str):
    # client.check_password(login, password)
    global client, role_client
    if role == 'admin':

        client = Administrator()
        result = client.check_password(login, password)  # true, false, superAdmin
        role_client = result
        if result == 'superAdmin':
            client = SuperAdmin()
            return 'superAdmin'
        return result
    elif role == 'user':
        role_client = role
        client = User()
        result = client.check_password(login, password)  # true, false
        return result


def save_hierarchy(list_hierarchy: list):
    # log
    handler_hierarchy.create_hierarchy(list_hierarchy)


def get_hierarchy():
    hierarchy = handler_hierarchy.Hierarchy()
    return hierarchy.get_data_about_departments()


def add_user_in_database(last_name: str, name: str, patronymic: str, division_number: str, login: str, password: str, ):
    # log
    client.add_user(last_name, name, patronymic, division_number, login, password)


def add_document_in_database(path_to_document: str, name_document: str, inner_number: str, output_number: str,
                             output_date, type_document: str):
    # log
    client.add_document(path_to_document, name_document, inner_number, output_number, output_date, type_document)


def get_data_about_documents():
    # log
    return client.get_data_about_documents()


def download_document(id_document: int, path_to_save: str):
    # log
    client.download_document(id_document, path_to_save)
    print("Документ сохранен")


def delete_document(name_document: str, inner_number: str, output_number: str):
    # log
    print(name_document)
    print(inner_number)
    print(output_number)
    db_helper_for_documents_and_users.delete_file(name_document, inner_number, output_number)


def edit_document(id_document: int, name_document: str, inner_number: str, output_number: str,
                  output_date, type_document: str):
    # log
    client.edit_document(id_document, name_document, inner_number, output_number, output_date, type_document)


def get_data_about_users():
    # log
    data = client.get_data_about_users()
    return data


def delete_user(id_user: int):
    client.delete_user(id_user)


def edit_user_data(last_name: str, name: str, patronymic: str, division_number: str, login: str, password: str, id_user,
                   flag_edit_login: bool):
    # log
    client.edit_user_data(last_name, name, patronymic, division_number, login, password, id_user, flag_edit_login)


def add_admin_in_database(last_name: str, name: str, patronymic: str, login: str, password: str):
    # log
    client.add_admin(last_name, name, patronymic, login, password)


def get_data_about_admins():
    # log
    data = client.get_data_about_admins()
    return data


def delete_admin(id_admin: int):
    # log
    client.delete_admin(id_admin)


def edit_admin_data(id_admin: int, new_last_name: str, new_name: str, new_patronymic: str, new_login: str,
                    new_password: str, flag_edit_login: bool):
    client.edit_admin_data(id_admin, new_last_name, new_name, new_patronymic, new_login, new_password, flag_edit_login)


def add_department(name_department: str, number_department: int):
    return handler_hierarchy.add_department_in_db(name_department, number_department)


def delete_department(id_department: int):
    # log
    handler_hierarchy.delete_department_in_db(id_department)


def update_data_departments(list_departments: list):
    # log
    handler_hierarchy.update_data_departments(list_departments)


def change_people_departments(list_replacement_departments: list):
    # log
    handler_hierarchy.change_people_departments(list_replacement_departments)


def change_password(password: str):
    # log
    return client.change_password(password)


def get_last_password_change():
    # log
    # client = User()
    return client.get_last_change_password()


def get_login():
    # log
    return client.get_login()


def get_full_name():
    return client.get_full_name()


def get_number_department():
    return client.get_number_department()


def check_password_strength(password: str):
    return client.check_password_strength(password)


def search_documents(search_string: str):
    # log
    return client.search_data_about_documents(search_string)
