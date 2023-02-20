import src.model.for_data_base.db_helper_for_hierarchy_derartments as db_helper_for_hierarchy
import src.model.for_data_base.db_helper as db_helper_for_documents_and_users
from src.model import admin
from src.model import handler_hierarchy


def save_hierarchy(list_hierarchy: []):
    # log
    db_helper_for_hierarchy.create_hierarchy(list_hierarchy)


def get_hierarchy():
    hierarchy = handler_hierarchy.Hierarchy()
    return hierarchy.get_data_about_departments()


def add_user_in_database(last_name: str, name: str, patronymic: str, division_number: str, login: str, password: str, ):
    # log
    admin.add_user(last_name, name, patronymic, division_number, login, password)


def add_document_in_database(path_to_document: str, name_document: str, inner_number: str, output_number: str,
                             output_date, type_document: str):
    # log
    admin.add_document(path_to_document, name_document, inner_number, output_number, output_date, type_document)


def get_data_about_documents():
    # log
    data = admin.get_data_about_documents()
    return data


def download_document(id_document: int, path_to_save: str):
    # log
    admin.download_document(id_document, path_to_save)
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
    admin.edit_document(id_document, name_document, inner_number, output_number, output_date, type_document)


def get_data_about_users():
    # log
    data = admin.get_data_about_users()
    return data


def delete_user(id_user: int):
    admin.delete_user(id_user)


def edit_user_data(last_name: str, name: str, patronymic: str, division_number: str, login: str, password: str, id_user,
                   flag_edit_login: bool):
    # log
    admin.edit_user_data(last_name, name, patronymic, division_number, login, password, id_user, flag_edit_login)


def add_admin_in_database(last_name: str, name: str, patronymic: str, login: str, password: str):
    # log
    admin.add_admin(last_name, name, patronymic, login, password)


def get_data_about_admins():
    # log
    data = admin.get_data_about_admins()
    return data


def delete_admin(id_admin: int):
    # log
    admin.delete_admin(id_admin)


def edit_admin_data(id_admin: int, new_last_name: str, new_name: str, new_patronymic: str, new_login: str,
                    new_password: str, flag_edit_login: bool):
    admin.edit_admin_data(id_admin, new_last_name, new_name, new_patronymic, new_login, new_password, flag_edit_login)


def add_department(name_department: str, number_department: int):
    return handler_hierarchy.add_department_in_db(name_department, number_department)


def delete_department(id_department: int):
    # log
    handler_hierarchy.delete_department_in_db(id_department)
