from sqlalchemy.ext.asyncio import AsyncSession

from src.interfaces.infrastructure.dao import IDAO


class BaseDAO(IDAO):
    def __init__(self, session: AsyncSession):
        self._session = session
