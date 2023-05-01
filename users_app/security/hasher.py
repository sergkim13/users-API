from passlib.context import CryptContext

from config import HASH_SCHEMA


def get_pwd_context():
    return CryptContext(schemes=[HASH_SCHEMA], deprecated='auto')
