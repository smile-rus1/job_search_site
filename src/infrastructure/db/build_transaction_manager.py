from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.transaction_manager import TransactionManager
from src.infrastructure.db import dao


def build_tm(session: AsyncSession) -> TransactionManager:
    return TransactionManager(
        session=session,
        user_dao=dao.UserDAO
    )
