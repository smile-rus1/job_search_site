from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.interfaces.infrastructure.dao.applicant_dao import IApplicantDAO
from src.interfaces.infrastructure.dao.balance_dao import IBalanceDAO
from src.interfaces.infrastructure.dao.chat_dao import IChatDAO
from src.interfaces.infrastructure.dao.company_dao import ICompanyDAO
from src.interfaces.infrastructure.dao.response_dao import IResponsesDAO
from src.interfaces.infrastructure.dao.resume_dao import IResumeDAO
from src.interfaces.infrastructure.dao.user_dao import IUserDAO
from src.interfaces.infrastructure.dao.vacancy_dao import IVacancyDAO
from src.interfaces.infrastructure.dao.workexperience_dao import IWorkExperienceDAO
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
            vacancy_dao: Type[IVacancyDAO],
            respond_dao: Type[IResponsesDAO],
            chat_dao: Type[IChatDAO],
            balance_dao: Type[IBalanceDAO]
    ):
        super().__init__(session=session)
        self.user_dao = user_dao(session=session)  # type: ignore
        self.applicant_dao = applicant_dao(session=session)  # type: ignore
        self.company_dao = company_dao(session=session)  # type: ignore
        self.resume_dao = resume_dao(session=session)  # type: ignore
        self.work_experience_dao = work_experience(session=session)  # type: ignore
        self.vacancy_dao = vacancy_dao(session=session)  # type: ignore
        self.respond_dao = respond_dao(session=session)  # type: ignore
        self.chat_dao = chat_dao(session=session)  # type: ignore
        self.balance_dao = balance_dao(session=session)  # type: ignore
