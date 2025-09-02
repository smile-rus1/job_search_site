from abc import ABC

from loguru import logger

from src.dto.services.user.auth import AuthUserDTO, AuthUserOutDTO
from src.dto.services.user.user import UserDTO
from src.exceptions.infrascructure.user.user import UserNotFoundByEmail
from src.exceptions.services.auth import InvalidEmail, InvalidPassword
from src.infrastructure.db.transaction_manager import TransactionManager
from src.interfaces.infrastructure.hasher import IHasher
from src.interfaces.services.auth import IJWTAuth


class AuthUseCase(ABC):
    def __init__(self, tm: TransactionManager, hasher: IHasher):
        self._tm = tm
        self._hasher = hasher


class AuthenticateUser(AuthUseCase):
    async def __call__(self, auth_dto: AuthUserDTO, auth: IJWTAuth) -> AuthUserOutDTO:
        try:
            user = await self._tm.user_dao.get_user_by_email(auth_dto.email)

        except UserNotFoundByEmail:
            logger.error(f"USER NOT FOUND WITH {auth_dto.email} email")
            raise InvalidEmail(auth_dto.email)

        if not self._hasher.verify(auth_dto.password, user.password):
            logger.error(f"INCORRECT PASSWORD ON USER {auth_dto.email}")
            raise InvalidPassword()

        data_dct = {
            "user_id": user.user_id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_admin": user.is_admin,
            "is_superuser": user.is_superuser
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


class AuthService:
    def __init__(self, tm: TransactionManager, hasher: IHasher):
        self._tm = tm
        self._hasher = hasher

    async def authenticate_user(self, auth_dto: AuthUserDTO, auth: IJWTAuth) -> AuthUserOutDTO:
        return await AuthenticateUser(self._tm, self._hasher)(auth_dto, auth)
