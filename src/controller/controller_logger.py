from loguru import logger
from src.config.types_role import Role

# Настройка логгера
controller_logger = logger.bind(client_id="", role="")
controller_logger.add("logs.log",
                      format="{time} {level} role={extra[role]} client_id={extra[client_id]} method={extra[method]} -> {message}")


def set_setting_logger(role: Role, id_client: int):
    global controller_logger
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
