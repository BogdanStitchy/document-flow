import src.model.for_data_base.db_helper_for_hierarchy_derartments as db_helper
from src.model.handler_hierarchy import Hierarchy


def save_hierarchy(list_hierarchy: []):
    # log
    db_helper.create_hierarchy(list_hierarchy)


def get_hierarchy():
    hierarchy = Hierarchy()
    return hierarchy.get_data_about_departments()
