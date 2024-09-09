from calendar import timegm
from datetime import datetime, timedelta
from typing import Any

import jwt
from jwt.exceptions import InvalidTokenError

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
            token_type="access",
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


class TokenVerification:
    def __init__(self, token_type: str, jwt_service: AuthJWT) -> None:
        self.token_type = token_type
        self.jwt_service = jwt_service

    def validate_token(self, token: str) -> dict[str, Any]:
        payload = self.decrypted_token(token)
        self.token_is_active(payload)
        self.check_token_type(payload)

        return payload

    def decrypted_token(self, token: str) -> dict[str, Any]:
        try:
            payload = self.jwt_service.decode_token(token)
        except InvalidTokenError:
            raise InvalidToken

        if payload.get("type") is None or payload.get("username") is None:
            raise InvalidToken
        return payload

    def token_is_active(self, payload: dict[str, Any]) -> None:
        if payload["exp"] < timegm(datetime.now().utctimetuple()):
            raise InvalidToken
        return payload

    def check_token_type(self, payload: dict[str, Any]) -> None:
        if payload["type"] != self.token_type:
            raise InvalidToken
