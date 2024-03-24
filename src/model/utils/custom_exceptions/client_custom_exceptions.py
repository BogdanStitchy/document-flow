class ClientNotFoundError(Exception):
    """Исключение, вызываемое, когда клиент не найден в базе данных"""
    pass


class ClientPasswordError(Exception):
    """Исключение, вызываемое, когда пароль клиента недействителен"""
    pass


class ClientActiveError(Exception):
    """Исключение, вызываемое, когда учетная запись клиента деактивирована"""
    pass


class FileNotWrittenError(Exception):
    """Исключение вызываемое, когда файл не удалось записать на устройство пользователя"""
    pass
