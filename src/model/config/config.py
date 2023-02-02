import os
from pathlib import Path


def load_dotenv():
    # working_dir = Path.cwd()
    # print("path:", working_dir)
    # print(Path.cwd().parent)
    # print(Path(Path.cwd()))
    path = Path(Path.home(), "PycharmProjects", "document_flow", "src", "model", "config", ".env")
    # print(path)
    with open(path, 'r') as file:
        lines = file.readlines()
    # print(lines)
    # print(type(lines))
    for line in lines:
        os.environ[line[:line.find('=')]] = line[line.find('=') + 1: line.find('\\')]


load_dotenv()

DRIVER_DB = os.environ['DRIVER_DB']
LOGIN_DB = os.environ['LOGIN_DB']
PASSWORD_DB = os.environ['PASSWORD_DB']
NAME_DB = os.environ['NAME_DB']
HOST = os.environ['HOST']
PORT = os.environ['PORT']
HASH_FUNCTION = os.environ['HASH_FUNCTION']


# print(LOGIN_DB)
# print(PASSWORD_DB)
# print(NAME_DB)
# print(HOST)
# print(type(HOST))
# print(HASH_FUNCTION)
