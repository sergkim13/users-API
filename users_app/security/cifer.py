import jwt
from config import JWT_KEY, ALGORITHM
from users_app.schemas.schemas import Payload


class Cifer:
    def __init__(self, secret_key: str, algorithm: str) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm

    def encode(self, payload: Payload) -> str:

        encoded_jwt = jwt.encode(payload.dict(), self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode(self, encoded_jwt: str) -> Payload:
        payload = jwt.decode(encoded_jwt, self.secret_key, algorithms=[self.algorithm])
        return payload


def get_cifer() -> Cifer:
    return Cifer(JWT_KEY, ALGORITHM)
