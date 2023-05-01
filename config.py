import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ['SECRET_KEY']
JWT_KEY = os.environ['JWT_KEY']
ALGORITHM = os.environ['ALGORITHM']
HASH_SCHEMA = os.environ['HASH_SCHEMA']

DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
