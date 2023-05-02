import os

from dotenv import load_dotenv

load_dotenv()

# Security
SECRET_KEY = os.environ.get('SECRET_KEY')
JWT_KEY = os.environ.get('JWT_KEY')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')
HASH_SCHEMA = os.environ.get('HASH_SCHEMA')

# Database
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
TEST_DB_NAME = os.environ.get('TEST_DB_NAME')

# Cache
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
REDIS_DB = os.environ.get('REDIS_DB')
REDIS_EXP = os.environ.get('REDIS_EXP')
