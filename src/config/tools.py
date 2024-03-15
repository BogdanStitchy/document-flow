import hashlib
from src.config import config


def create_hash_password(password: str, salt: bytes):
    password = hashlib.pbkdf2_hmac(
        config.HASH_FUNCTION,
        password.encode('utf-8'),
        salt,
        200000,
        dklen=64
    )
    return password


def check_params_empty(params: dict.values, message_error: str = "Переданы пусты аргументы"):
    for value in params:
        if value == "":
            raise ValueError(message_error)
