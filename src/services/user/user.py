from abc import ABC

from loguru import logger

from src.dto.db.user.user import CreateUserDTODAO
from src.exceptions.infrascructure.user.user import UserNotFoundByEmail
from src.dto.services.user.user import CreateUserDTO, UserOutDTO, UserDTO
from src.exceptions.infrascructure.user.user import UserAlreadyExist
from src.exceptions.services.auth import InvalidEmail
from src.infrastructure.db.transaction_manager import TransactionManager
from src.interfaces.infrastructure.hasher import IHasher


class UserUseCase(ABC):
    def __init__(self, tm: TransactionManager, hasher: IHasher):
        self._tm = tm
        self._hasher = hasher


class GetUserByEmail(UserUseCase):
    async def __call__(self, email: str) -> UserDTO:
        try:
            user = await self._tm.user_dao.get_user_by_email(email)

        except UserNotFoundByEmail:
            logger.error(f"USER NOT FOUND WITH {email} email")
            raise InvalidEmail(email)

        return UserDTO(
            user_id=user.user_id,
            email=user.email,
            last_name=user.last_name,
            first_name=user.first_name,
            created_at=user.created_at,
            updated_at=user.updated_at
        )


class UserService:
    def __init__(self, tm: TransactionManager, hasher: IHasher):
        self._tm = tm
        self._hasher = hasher

    async def create_user(self, user_dto) -> UserOutDTO:
        return await CreateUser(self._tm, self._hasher)(user_dto)

    async def get_user_by_email(self, email: str) -> UserDTO:
        return await GetUserByEmail(self._tm, self._hasher)(email)
