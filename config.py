import os

from dotenv import load_dotenv

load_dotenv()

# Security
SECRET_KEY = os.environ['SECRET_KEY']
JWT_KEY = os.environ['JWT_KEY']
JWT_ALGORITHM = os.environ['JWT_ALGORITHM']
HASH_SCHEMA = os.environ['HASH_SCHEMA']

# Database
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']

# Cache
REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = os.environ['REDIS_PORT']
REDIS_DB = os.environ['REDIS_DB']
REDIS_EXP = os.environ['REDIS_EXP']
