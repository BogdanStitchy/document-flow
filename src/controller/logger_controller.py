from loguru import logger
from src.config.types_role import Role
from src.db.database_setup import session_factory
from src.db.models.logs import Logs


# Настройка логгера
controller_logger = logger.bind(client_id="", role="")
controller_logger.add("logs/logs.log",
                      format="{time} {level} role={extra[role]} client_id={extra[client_id]} method={extra[method]} -> {message}",
                      rotation="5 MB", compression="zip")


def write_log_to_database(message):
    msg = message.record['message']
    time = message.record['time']
    level = message.record['level'].name
    client_id = message.record['extra']['client_id']
    role = message.record['extra']['role']
    method = message.record['extra']['method']

    with session_factory() as session:
        new_log = Logs(
            time=time,
            level=level,
            client_id=client_id,
            role=role,
            method=method,
            status=msg
        )
        session.add(new_log)
        session.commit()


def set_setting_logger(role: Role, id_client: int, database_entry=False):
    global controller_logger
    if database_entry:
        controller_logger.add(write_log_to_database,
                              format="{time} {level} {extra[role]} {extra[client_id]} {extra[method]} -> {message}")
    controller_logger = controller_logger.bind(client_id=str(id_client), role=role)


def log(func):
    def wrapper(*args, **kwargs):
        try:
            result_func = func(*args, **kwargs)
            controller_logger.bind(method=func.__name__).info("success")
            return result_func
        except Exception as ex:
            controller_logger.bind(method=func.__name__).critical(str(ex))
            raise ex

    return wrapper
