from passlib.context import CryptContext

from config import HASH_SCHEMA


def get_pwd_context():
    '''Returns `CryptContext` instance for dependency injection.'''
    return CryptContext(schemes=[HASH_SCHEMA], deprecated='auto')
