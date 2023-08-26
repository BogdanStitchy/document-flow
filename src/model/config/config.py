import os
from pathlib import Path


def load_dotenv():
    path = Path(Path.cwd(), "src", "model", "config", ".env")

    with open(path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        os.environ[line[:line.find('=')]] = line[line.find('=') + 1: line.find('\\')]


load_dotenv()

DRIVER_DB = os.environ['DRIVER_DB']
DIALECT_DB = os.environ['DIALECT_DB']
LOGIN_DB = os.environ['LOGIN_DB']
PASSWORD_DB = os.environ['PASSWORD_DB']
NAME_DB = os.environ['NAME_DB']
HOST = os.environ['HOST']
PORT = os.environ['PORT']
HASH_FUNCTION = os.environ['HASH_FUNCTION']
