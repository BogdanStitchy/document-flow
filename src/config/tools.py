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
