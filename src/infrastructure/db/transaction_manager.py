from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.dao import UserDAO
from src.interfaces.infrastructure.dao import IDAO
from src.interfaces.infrastructure.transaction_manager import IBaseTransactionManager


class BaseTransactionManager(IBaseTransactionManager):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


class TransactionManager(BaseTransactionManager):
    user_dao: UserDAO

    def __init__(
            self,
            session: AsyncSession,
            user_dao: Type[UserDAO]
    ):
        super().__init__(session=session)
        self.user_dao = user_dao(session=session)

