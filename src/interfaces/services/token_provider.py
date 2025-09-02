import abc
from typing import Any


class IJWTProvider(abc.ABC):
    @abc.abstractmethod
    def _encode_jwt(self, data: dict | Any, expires_delta: int) -> str:
        ...

    @abc.abstractmethod
    def create_access_token(self, data: dict | Any, expires_delta: int | None = None) -> str:
        ...

    @abc.abstractmethod
    def create_refresh_token(self, data: dict | Any, expires_delta: int | None = None) -> str:
        ...

    @abc.abstractmethod
    def decode_token(self, token: str):
        ...

    @abc.abstractmethod
    def read_token(self, token: str) -> dict | None:
        ...
