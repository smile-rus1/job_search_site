import json
from abc import ABC

from loguru import logger

from src.core.config_reader import config
from src.dto.db.user.user import BaseUserDTODAO
from src.dto.services.user.auth import AuthUserDTO, AuthUserOutDTO
from src.exceptions.infrascructure.user.user import UserNotFoundByEmail, BaseUserException
from src.exceptions.services.auth import InvalidEmail, InvalidPassword
from src.interfaces.infrastructure.hasher import IHasher
from src.interfaces.infrastructure.redis_db import IRedisDB
from src.interfaces.services.transaction_manager import IBaseTransactionManager
from src.interfaces.services.auth import IJWTAuth


class AuthUseCase(ABC):
    def __init__(self, tm: IBaseTransactionManager, hasher: IHasher):
        self._tm = tm
        self._hasher = hasher


class AuthenticateUser(AuthUseCase):
    async def __call__(self, auth_dto: AuthUserDTO, auth: IJWTAuth) -> AuthUserOutDTO:
        try:
            user = await self._tm.user_dao.get_user_by_email(auth_dto.email)

        except UserNotFoundByEmail:
            logger.bind(
                app_name=f"{AuthenticateUser.__name__}"
            ).error(f"USER NOT FOUND WITH: {auth_dto.email}")
            raise InvalidEmail(auth_dto.email)

        if not self._hasher.verify(auth_dto.password, user.password):
            logger.bind(
                app_name=f"{AuthenticateUser.__name__}"
            ).error(f"INCORRECT PASSWORD ON USER: {auth_dto.email}")
            raise InvalidPassword()

        data_dct = {
            "user_id": user.user_id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_admin": user.is_admin,
            "is_superuser": user.is_superuser,
            "type": user.type
        }

        await auth.set_tokens(data_dct)

        return AuthUserOutDTO(
            user_id=user.user_id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            is_superuser=user.is_superuser,
            is_admin=user.is_admin
        )


class VerifyUser(AuthUseCase):
    async def __call__(self, token: str, redis_db: IRedisDB) -> bool:
        redis_key = config.auth.user_confirm_key.format(token=token)
        data = await redis_db.get(redis_key)
        if data is None:
            return False

        user_data: dict = json.loads(data.decode("utf-8"))
        user = BaseUserDTODAO(user_id=user_data.get("user_id"), type=user_data.get("type"))
        try:
            is_confirmed = await self._tm.user_dao.confirm_user(user)
            await self._tm.commit()

            return is_confirmed

        except BaseUserException:
            logger.bind(
                app_name=f"{VerifyUser.__name__}"
            ).error(f"TOKEN {token}")
            await self._tm.rollback()


class AuthService:
    def __init__(self, tm: IBaseTransactionManager, hasher: IHasher, redis_db: IRedisDB):
        self._tm = tm
        self._hasher = hasher
        self._redis_db = redis_db

    async def authenticate_user(self, auth_dto: AuthUserDTO, auth: IJWTAuth) -> AuthUserOutDTO:
        return await AuthenticateUser(self._tm, self._hasher)(auth_dto, auth)

    async def verify_user(self, token: str) -> bool:
        return await VerifyUser(self._tm, self._hasher)(token, self._redis_db)
