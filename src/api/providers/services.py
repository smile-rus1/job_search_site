from typing import Any

from fastapi import Depends

from src.api.providers.abstract.common import tm_provider, hasher_provider
from src.dto.services.user.user import UserDTO
from src.infrastructure.db.transaction_manager import TransactionManager
from src.infrastructure.hasher import Hasher
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
