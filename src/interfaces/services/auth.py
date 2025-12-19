import abc


class IJWTAuth(abc.ABC):
    @abc.abstractmethod
    async def set_tokens(self, user: dict) -> None:
        ...

    @abc.abstractmethod
    async def set_token(self, token: str, token_type: str) -> None:
        ...

    @abc.abstractmethod
    def read_token(self, token_type: str) -> dict | None:
        ...

    @abc.abstractmethod
    async def unset_tokens(self) -> None:
        ...

    async def refresh_access_token(self) -> None:
        ...
