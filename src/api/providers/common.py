from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.providers.abstract.common import session_provider, redis_pool_provider, redis_db_provider
from src.core.config import Config
from src.infrastructure.connections import get_db_connection, get_redis_connections
from src.infrastructure.db.build_transaction_manager import build_tm
from src.infrastructure.hasher import Hasher
from src.infrastructure.redis_db.redis_db import RedisDB
from src.interfaces.infrastructure.redis_db import IRedisDB


def db_session(config: Config):
    sessionmaker = get_db_connection(config.db)

    async def get_db_session() -> AsyncSession:
        async with sessionmaker() as session:
            yield session

    return get_db_session


def redis_pool_getter(config: Config):
    def get_pool_redis():
        return get_redis_connections(redis_config=config.redis)

    return get_pool_redis


def redis_db_getter(
        redis: Redis = Depends(redis_pool_provider)
) -> IRedisDB:
    return RedisDB(redis=redis)


def tm_getter(
        session: AsyncSession = Depends(session_provider),
        redis_db: IRedisDB = Depends(redis_db_provider)
):
    """
    This func is get impl of transaction manager
    """

    return build_tm(session, redis_db)


def hasher_getter() -> Hasher:
    return Hasher()
