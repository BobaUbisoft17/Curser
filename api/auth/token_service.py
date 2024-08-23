from datetime import datetime, timedelta
from typing import Any

import jwt

from .exceptions import InvalidToken


class AuthJWT:

    access_token_expire_minutes = 30
    refresh_token_expire_minutes = 30 * 24 * 60

    def __init__(self, secret_key: str, algorithm: str) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_token(
        self, token_type: str, payload: dict[str, Any], exp_time: int
    ) -> str:
        payload.update(
            type=token_type,
            exp=datetime.now() + timedelta(minutes=exp_time),
        )
        return jwt.encode(
            payload=payload,
            key=self.secret_key,
            algorithm=self.algorithm,
        )

    def create_access_token(self, payload: dict[str, Any]) -> str:
        return self.create_token(
            token_type="accsess",
            payload=payload,
            exp_time=self.access_token_expire_minutes,
        )

    def create_refresh_token(self, payload: dict[str, Any]) -> str:
        return self.create_token(
            token_type="refresh",
            payload=payload,
            exp_time=self.refresh_token_expire_minutes,
        )

    def decode_token(self, token: str) -> dict[str, Any]:
        try:
            return jwt.decode(token, self.secret_key, [self.algorithm])
        except jwt.exceptions.InvalidTokenError:
            raise InvalidToken
