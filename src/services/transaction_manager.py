from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.interfaces.infrastructure.dao.applicant_dao import IApplicantDAO
from src.interfaces.infrastructure.dao.company_dao import ICompanyDAO
from src.interfaces.infrastructure.dao.resume_dao import IResumeDAO
from src.interfaces.infrastructure.dao.user_dao import IUserDAO
from src.interfaces.infrastructure.dao.vacancy_dao import IVacancyDAO
from src.interfaces.infrastructure.dao.workexperience_dao import IWorkExperienceDAO
from src.interfaces.infrastructure.redis_db import IRedisDB
from src.interfaces.services.transaction_manager import IBaseTransactionManager


class BaseTransactionManager(IBaseTransactionManager):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


class TransactionManager(BaseTransactionManager):
    def __init__(
            self,
            session: AsyncSession,
            user_dao: Type[IUserDAO],
            applicant_dao: Type[IApplicantDAO],
            company_dao: Type[ICompanyDAO],
            resume_dao: Type[IResumeDAO],
            work_experience: Type[IWorkExperienceDAO],
            vacancy_dao: Type[IVacancyDAO]
    ):
        super().__init__(session=session)
        self.user_dao = user_dao(session=session)  # type: ignore
        self.applicant_dao = applicant_dao(session=session)  # type: ignore
        self.company_dao = company_dao(session=session)  # type: ignore
        self.resume_dao = resume_dao(session=session)  # type: ignore
        self.work_experience_dao = work_experience(session=session)  # type: ignore
        self.vacancy_dao = vacancy_dao(session=session)  # type: ignore
