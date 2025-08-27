from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError

from src.core.config_reader import config


def create_access_token(data: dict | Any, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta is None:
        expires_delta = timedelta(minutes=15)

    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.auth.secret_key, algorithm=config.auth.algorithm)

    return encoded_jwt


def decode_token(token: str):
    try:
        payload = jwt.decode(token, key=config.auth.secret_key, algorithms=config.auth.algorithm)

    except (JWTError, ValidationError) as exc:
        raise exc

    return payload
