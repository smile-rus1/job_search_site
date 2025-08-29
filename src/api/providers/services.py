from fastapi import Depends

from src.api.providers.abstract.common import tm_provider, hasher_provider
from src.infrastructure.db.transaction_manager import TransactionManager
from src.infrastructure.hasher import Hasher
from src.services.applicant.applicant import ApplicantService
from src.services.company.company import CompanyService
from src.services.user.auth import AuthService
from src.services.user.user import UserService


def auth_service_getter(
        tm: TransactionManager = Depends(tm_provider),
        hasher: Hasher = Depends(hasher_provider)
):
    return AuthService(tm=tm, hasher=hasher)


def user_service(
        tm: TransactionManager = Depends(tm_provider),
        hasher: Hasher = Depends(hasher_provider)
):
    return UserService(tm=tm, hasher=hasher)


def applicant_service(
        tm: TransactionManager = Depends(tm_provider),
        hasher: Hasher = Depends(hasher_provider)
):
    return ApplicantService(tm=tm, hasher=hasher)


def company_service(
        tm: TransactionManager = Depends(tm_provider),
        hasher: Hasher = Depends(hasher_provider)
):
    return CompanyService(tm=tm, hasher=hasher)
