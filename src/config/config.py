import os
from dotenv import load_dotenv

load_dotenv()

DRIVER_DB = os.environ['DRIVER_DB']
DIALECT_DB = os.environ['DIALECT_DB']
LOGIN_DB = os.environ['LOGIN_DB']
PASSWORD_DB = os.environ['PASSWORD_DB']
NAME_DB = os.environ['NAME_DB']
HOST = os.environ['HOST']
PORT = os.environ['PORT']
HASH_FUNCTION = os.environ['HASH_FUNCTION']
