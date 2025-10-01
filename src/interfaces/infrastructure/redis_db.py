import abc
from typing import Any, Optional

from redis.asyncio import Redis


class IRedisDB(abc.ABC):
    def __init__(self, redis: Redis):
        self._redis = redis

    @abc.abstractmethod
    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, key: str) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    async def exists(self, key: str) -> bool:
        raise NotImplementedError
