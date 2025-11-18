from typing import Protocol

from src.interfaces.infrastructure.dao.applicant_dao import IApplicantDAO
from src.interfaces.infrastructure.dao.company_dao import ICompanyDAO
from src.interfaces.infrastructure.dao.resume_dao import IResumeDAO
from src.interfaces.infrastructure.dao.user_dao import IUserDAO
from src.interfaces.infrastructure.dao.vacancy_dao import IVacancyDAO
from src.interfaces.infrastructure.dao.workexperience_dao import IWorkExperienceDAO
from src.interfaces.infrastructure.redis_db import IRedisDB


class IBaseTransactionManager(Protocol):
    user_dao: IUserDAO
    applicant_dao: IApplicantDAO
    company_dao: ICompanyDAO
    resume_dao: IResumeDAO
    work_experience_dao: IWorkExperienceDAO
    vacancy_dao: IVacancyDAO

    async def commit(self):
        raise NotImplementedError

    async def rollback(self):
        raise NotImplementedError
