from sqlalchemy.ext.asyncio import AsyncSession

from src.services.transaction_manager import TransactionManager
from src.infrastructure.db import dao
from src.interfaces.infrastructure.redis_db import IRedisDB


def build_tm(
        session: AsyncSession
) -> TransactionManager:
    return TransactionManager(
        session=session,
        user_dao=dao.UserDAO,
        applicant_dao=dao.ApplicantDAO,
        company_dao=dao.CompanyDAO,
        resume_dao=dao.ResumeDAO,
        work_experience=dao.WorkExperienceDAO,
        vacancy_dao=dao.VacancyDAO
    )
