from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError

from starlette.requests import Request
from starlette.responses import Response

from src.core.config_reader import config
from src.exceptions.services.auth import RefreshTokenNotValid
from src.interfaces.services.auth import IJWTAuth
from src.interfaces.services.token_provider import IJWTProvider
from src.utils.datetimes import get_timezone_now


class JWTProvider(IJWTProvider):
    def _encode_jwt(self, data: dict | Any, expires_delta: int) -> str:
        to_encode = data.copy()

        expire = get_timezone_now() + timedelta(seconds=expires_delta)
        to_encode.update({"exp": expire})
        encoded_token = jwt.encode(to_encode, config.auth.secret_key, algorithm=config.auth.algorithm)
        return encoded_token

    def create_access_token(
            self,
            data: dict | Any,
            expires_delta: int | None = config.auth.access_token_expire
    ) -> str:
        return self._encode_jwt(
            data=data,
            expires_delta=expires_delta
        )

    def create_refresh_token(
            self,
            data: dict | Any,
            expires_delta: int | None = config.auth.refresh_token_expire
    ) -> str:
        return self._encode_jwt(
            data=data,
            expires_delta=expires_delta
        )

    def decode_token(self, token: str):
        try:
            payload = jwt.decode(token, key=config.auth.secret_key, algorithms=config.auth.algorithm)

        except (JWTError, ValidationError) as exc:
            raise exc

        return payload

    def read_token(self, token: str | None) -> dict | None:
        if token is None:
            return

        try:
            payload = self.decode_token(token)
            user_id = payload.get("user_id")
            if user_id is None:
                return

        except (JWTError, ValidationError):
            return
        return payload


class JWTAuth(IJWTAuth):
    def __init__(
        self,
        request: Request | None = None,
        response: Response | None = None
    ):
        self.request = request
        self.response = response
        self._jwt_provider = JWTProvider()

    async def set_tokens(self, user: dict) -> None:
        data = {
            "user_id": user.get("user_id"),
            "email": user.get("email"),
            "first_name": user.get("first_name"),
            "last_name": user.get("last_name"),
            "is_admin": user.get("is_admin"),
            "is_superuser": user.get("is_superuser")
        }

        access_token = self._jwt_provider.create_access_token(data)
        refresh_token = self._jwt_provider.create_refresh_token(data)

        await self.set_token(token=access_token, token_type=config.auth.access_token_name)
        await self.set_token(token=refresh_token, token_type=config.auth.refresh_token_name)

    async def set_token(self, token: str, token_type: str) -> None:
        self.response.set_cookie(key=token_type, value=token)

    async def _get_token(self, token_name: str):
        return self.request.cookies.get(token_name, "")

    async def read_token(self, token_type: str) -> dict | None:
        token = ""
        if token_type == config.auth.access_token_name:
            token = await self._get_token(config.auth.access_token_name)
        elif token_type == config.auth.refresh_token_name:
            token = await self._get_token(config.auth.refresh_token_name)

        token_data = self._jwt_provider.read_token(token)
        return token_data

    async def unset_tokens(self):
        self.response.delete_cookie(config.auth.access_token_name)
        self.response.delete_cookie(config.auth.refresh_token_name)

    async def refresh_access_token(self) -> None:
        refresh_token_data = await self.read_token(config.auth.refresh_token_name)
        if refresh_token_data is None:
            raise RefreshTokenNotValid()

        access_token = self._jwt_provider.create_access_token(refresh_token_data)
        await self.set_token(token=access_token, token_type=config.auth.access_token_name)
