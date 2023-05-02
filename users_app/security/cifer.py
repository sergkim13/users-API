import jwt

from config import JWT_ALGORITHM, JWT_KEY
from users_app.validation.schemas import Payload


class Cifer:
    '''Cifer which provides cryptographic operations for JWT handling.'''
    def __init__(self, secret_key: str, algorithm: str) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm

    def encode(self, payload: Payload) -> str:
        '''Encodesgiven payload to JWT.'''
        encoded_jwt = jwt.encode(payload.dict(), self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode(self, encoded_jwt: str) -> Payload:
        '''Decodesgiven JWT and returns payload.'''
        payload = jwt.decode(encoded_jwt, self.secret_key, algorithms=[self.algorithm])
        return payload


def get_cifer() -> Cifer:
    '''Returns `Cifer` instance for dependency injection.'''
    return Cifer(JWT_KEY, JWT_ALGORITHM)
