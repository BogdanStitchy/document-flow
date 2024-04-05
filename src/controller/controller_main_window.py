from typing import Tuple, Optional

from src.controller import logger_controller

from src.model.user import User
from src.model.administrator import Administrator
from src.model.super_admin import SuperAdmin
from src.model.utils.custom_exceptions import ClientPasswordError, ClientActiveError, ClientNotFoundError, \
    FileNotWrittenError
from src.config.types_role import Role

client = SuperAdmin


def __setup_logger(role: Role, id_client: int, database_entry=False):
    """
    needed to explicitly specify logging settings. Called when the user is authorized
    :param role:
    :param id_client:
    :param database_entry:
    :return:
    """
    logger_controller.set_setting_logger(role, id_client, database_entry=database_entry)


def authenticate(login: str, password: str, role: Role) -> Tuple[Optional[str], Optional[str]]:
    """
    Performs user authentication with error handling
    :param login:
    :param password:
    :param role:
    :return: role: str or None, error:str or None
    """
    try:
        user = __check_login(login, password, role)
        return user, None  # Возвращаем объект пользователя и None в качестве ошибки
    except (ClientActiveError, ClientNotFoundError, ClientPasswordError) as ex:
        return None, str(ex)
    except Exception:
        return None, f"Неизвестная ошибка, обратитесь к разработчикам. \nКод ошибки: 001"


@logger_controller.log
def __check_login(login: str, password: str, role: Role):
    """

    :param login:
    :param password:
    :param role: Role.ADMIN or Role.USER
    :return: 'admin' or 'user' or 'superAdmin' or message about error
    """
    if role not in (Role.ADMIN, Role.USER):
        raise ValueError("Значение role ожидается Role.ADMIN или Role.USER")
    global client

    if role == Role.ADMIN:
        client = Administrator()

    elif role == Role.USER:
        client = User()

    result = client.check_password(login, password)

    if result == role.SUPERADMIN:
        client = SuperAdmin()

    __setup_logger(client.get_role(), client.get_id())

    return result


@logger_controller.log
def change_password(password: str):
    return client.change_password(password)


@logger_controller.log
def check_needs_password_change():
    return client.check_needs_password_change()


@logger_controller.log
def get_login():
    return client.get_login()


@logger_controller.log
def get_role():
    return client.get_role()


@logger_controller.log
def get_full_name():
    return client.get_full_name()


@logger_controller.log
def check_password_strength(password: str):
    return client.check_password_strength(password)


# ---------------------------------document mode------------------------------------------------

@logger_controller.log
def add_document_in_database(path_to_document: str, name_document: str, inner_number: str, output_number: str,
                             output_date, type_document: str, note: str):
    client.add_document(path_to_document, name_document, inner_number, output_number, output_date, type_document, note)


@logger_controller.log
def get_data_about_documents():
    return client.get_data_about_documents()


@logger_controller.log
def download_document(id_document: int, path_to_save: str):
    @logger_controller.log
    def try_download_document():
        client.download_document(id_document, path_to_save)

    try:
        try_download_document()
    except FileNotFoundError:
        return "Путь для сохранения файла недопустим"
    except FileNotWrittenError:
        return str(FileNotWrittenError)
    except Exception:
        return "Неизвестная ошибка, обратитесь в отдел разработки. \nКод ошибки 201"


@logger_controller.log
def delete_document(id_document: int):
    client.delete_document(id_document)


@logger_controller.log
def edit_document(id_document: int, name_document: str, inner_number: str, output_number: str,
                  output_date, type_document: str):
    client.edit_document(id_document, name_document, inner_number, output_number, output_date, type_document)


@logger_controller.log
def search_documents(search_string: str):
    return client.search_string_in_documents(search_string)


@logger_controller.log
def apply_period_searching_documents(flag_date_output: bool, flag_date_download: bool,
                                     start_date_output: str = None, end_date_output: str = None,
                                     start_date_download: str = None, end_date_download: str = None):
    return client.apply_period_searching_documents(flag_date_output, flag_date_download,
                                                   start_date_output=start_date_output, end_date_output=end_date_output,
                                                   start_date_download=start_date_download,
                                                   end_date_download=end_date_download)


# ---------------------------------user mode----------------------------------------------------

@logger_controller.log
def get_data_about_users():
    return client.get_data_about_users()


@logger_controller.log
def change_activation_status(id_user: int):
    client.change_activation_status(id_user)


@logger_controller.log
def add_user_in_database(last_name: str, name: str, patronymic: str, login: str, password: str, id_department: int):
    client.add_user(last_name, name, patronymic, login, password, id_department)


@logger_controller.log
def edit_user_data(last_name: str, name: str, patronymic: str, login: str, password: str, id_user: int,
                   id_department: int):
    client.edit_user_data(last_name, name, patronymic, login, password, id_department=id_department, id_user=id_user)


@logger_controller.log
def search_users(search_string: str):
    return client.search_string_in_users(search_string)


@logger_controller.log
def apply_period_searching_registration_users(start_date_download: str, end_date_download: str):
    return client.apply_period_registration_users(start_date_download, end_date_download)


# ---------------------------------admin mode---------------------------------------------------

@logger_controller.log
def add_admin_in_database(last_name: str, name: str, patronymic: str, login: str, password: str):
    client.add_admin(last_name, name, patronymic, login, password)


@logger_controller.log
def get_data_about_admins():
    data = client.get_data_about_admins()
    return data


@logger_controller.log
def change_activation_status_admin(id_admin: int):
    client.change_activation_status_admin(id_admin)


@logger_controller.log
def edit_admin_data(id_admin: int, new_last_name: str, new_name: str, new_patronymic: str, new_login: str,
                    new_password: str):
    client.edit_admin_data(id_admin, new_last_name, new_name, new_patronymic, new_login, new_password)


@logger_controller.log
def search_admins(search_string: str):
    return client.search_string_in_admins(search_string)


@logger_controller.log
def apply_period_registration_admins(start_date_creating: str, end_date_creating: str):
    return client.apply_period_registration_admins(start_date_creating, end_date_creating)


# ---------------------------------department mode----------------------------------------------

@logger_controller.log
def save_hierarchy(list_hierarchy: list):
    client.save_hierarchy(list_hierarchy)


@logger_controller.log
def get_hierarchy():
    return client.get_hierarchy()


@logger_controller.log
def add_department(name_department: str, number_department: int, parent_id: int):
    return client.add_department(name_department, number_department, parent_id)


@logger_controller.log
def delete_departments(id_departments_for_delete: list):
    client.delete_departments(id_departments_for_delete)


@logger_controller.log
def update_data_departments(list_departments: list):
    client.update_data_departments(list_departments)


@logger_controller.log
def change_people_departments(list_replacement_departments: list):
    client.change_people_departments(list_replacement_departments)


@logger_controller.log
def get_all_departments_without_one(id_exempt_department: int):
    return client.get_all_departments_without_one(id_exempt_department)


@logger_controller.log
def get_number_department():
    return client.get_number_department()
