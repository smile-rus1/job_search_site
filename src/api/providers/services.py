from fastapi import Depends

from src.api.providers.abstract.common import tm_provider, hasher_provider, fm_provider, notification_email_provider, \
    redis_db_provider
from src.infrastructure.notifications.email import EmailNotifications
from src.interfaces.infrastructure.notifications import AbstractNotifications
from src.interfaces.infrastructure.redis_db import IRedisDB
from src.interfaces.services.transaction_manager import IBaseTransactionManager
from src.infrastructure.hasher import Hasher
from src.services.applicant.applicant import ApplicantService
from src.services.company.company import CompanyService
from src.services.files_work.files_manager import FilesManager
from src.services.files_work.files_work import FilesWorkService
from src.services.resume.resume import ResumeService
from src.services.user.auth import AuthService
from src.services.user.user import UserService
from src.services.vacancy.vacancy import VacancyService
from src.services.work_experience.work_experience import WorkExperienceService


def auth_service_getter(
        tm: IBaseTransactionManager = Depends(tm_provider),
        hasher: Hasher = Depends(hasher_provider),
        redis_db: IRedisDB = Depends(redis_db_provider)
):
    return AuthService(tm=tm, hasher=hasher, redis_db=redis_db)


def user_service_getter(
        tm: IBaseTransactionManager = Depends(tm_provider),
        hasher: Hasher = Depends(hasher_provider)
):
    return UserService(tm=tm, hasher=hasher)


def applicant_service_getter(
        tm: IBaseTransactionManager = Depends(tm_provider),
        hasher: Hasher = Depends(hasher_provider),
        notifications: AbstractNotifications = Depends(notification_email_provider),
        redis_db: IRedisDB = Depends(redis_db_provider)
):
    return ApplicantService(tm=tm, hasher=hasher, notifications=notifications, redis_db=redis_db)


def company_service_getter(
        tm: IBaseTransactionManager = Depends(tm_provider),
        hasher: Hasher = Depends(hasher_provider),
        notifications: AbstractNotifications = Depends(notification_email_provider),
        redis_db: IRedisDB = Depends(redis_db_provider)
):
    return CompanyService(tm=tm, hasher=hasher, notifications=notifications, redis_db=redis_db)


def resume_service_getter(
        tm: IBaseTransactionManager = Depends(tm_provider),
):
    return ResumeService(tm=tm)


def work_experience_getter(
        tm: IBaseTransactionManager = Depends(tm_provider)
):
    return WorkExperienceService(tm=tm)


def files_work_service_getter(
        fm: FilesManager = Depends(fm_provider)
):
    return FilesWorkService(fm)


def vacancy_service_getter(
        tm: IBaseTransactionManager = Depends(tm_provider)
):
    return VacancyService(tm=tm)
