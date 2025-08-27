from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from src.core.config import Config
from src.infrastructure.db.utils.connection_sting_maker import make_connection_sting
from src.infrastructure.db_config import DBConfig


def get_db_connection(db_config: DBConfig):
    engine = create_async_engine(make_connection_sting(db_config))
    maker = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    return maker
