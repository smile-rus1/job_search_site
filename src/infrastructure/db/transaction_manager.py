from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.dao import UserDAO
from src.infrastructure.db.dao.applicant.applicant_dao import ApplicantDAO
from src.infrastructure.db.dao.company.company_dao import CompanyDAO
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
    applicant_dao: ApplicantDAO
    company_dao: CompanyDAO

    def __init__(
            self,
            session: AsyncSession,
            user_dao: Type[UserDAO],
            applicant_dao: Type[ApplicantDAO],
            company_dao: Type[CompanyDAO]
    ):
        super().__init__(session=session)
        self.user_dao = user_dao(session=session)
        self.applicant_dao = applicant_dao(session=session)
        self.company_dao = company_dao(session=session)
