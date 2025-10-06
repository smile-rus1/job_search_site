from typing import Any, Optional

from src.interfaces.infrastructure.redis_db import IRedisDB


class FakeRedisDB(IRedisDB):
    def __init__(self, redis: dict):
        self._redis = redis

    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        self._redis[key] = value
        return True

    async def get(self, key: str) -> Any:
        return self._redis.get(key)

    async def exists(self, key: str) -> bool:
        return key in self._redis.get
