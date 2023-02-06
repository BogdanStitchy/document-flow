import src.model.for_data_base.handler_for_hierarchy_derartments as db_helper


def save_hierarchy(list_hierarchy: []):
    # log
    db_helper.create_hierarchy(list_hierarchy)
