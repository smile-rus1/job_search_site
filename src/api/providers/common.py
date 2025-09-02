from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.providers.abstract.common import session_provider
from src.core.config import Config
from src.infrastructure.auth.jwt import JWTAuth
from src.infrastructure.connections import get_db_connection
from src.infrastructure.db.build_transaction_manager import build_tm
from src.infrastructure.hasher import Hasher
from src.interfaces.services.auth import IJWTAuth


def db_session(config: Config):
    sessionmaker = get_db_connection(config.db)

    async def get_db_session() -> AsyncSession:
        async with sessionmaker() as session:
            yield session

    return get_db_session


def tm_getter(
        session: AsyncSession = Depends(session_provider)
):
    """
    This func is get impl of transaction manager
    """

    return build_tm(session)


def hasher_getter() -> Hasher:
    return Hasher()
