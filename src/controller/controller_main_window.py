import src.model.for_data_base.db_helper_for_hierarchy_derartments as db_helper
from src.model import admin
from src.model.handler_hierarchy import Hierarchy


def save_hierarchy(list_hierarchy: []):
    # log
    db_helper.create_hierarchy(list_hierarchy)


def get_hierarchy():
    hierarchy = Hierarchy()
    return hierarchy.get_data_about_departments()


def add_user_in_database(last_name: str, name: str, patronymic: str, division_number: str, login: str, password: str,
                         access_lvl: int):
    # log
    admin.add_user(last_name, name, patronymic, division_number, login, password, access_lvl)


def add_document_in_database(path_to_document: str, name_document: str, inner_number: str, output_number: str,
                             type_document: str):
    # log
    admin.add_document(path_to_document, name_document, inner_number, output_number, type_document)
