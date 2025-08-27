from abc import ABC

from loguru import logger

from src.dto.infustructure.user.user import CreateUserDTODAO
from src.exceptions.infrascructure.user.user import UserNotFoundByEmail
from src.dto.services.user.user import CreateUserDTO, OutUserDTO, UserDTO
from src.exceptions.infrascructure.user.user import UserAlreadyExist
from src.exceptions.services.auth import InvalidEmail
from src.infrastructure.db.transaction_manager import TransactionManager
from src.interfaces.infrastructure.hasher import IHasher


class UserUseCase(ABC):
    def __init__(self, tm: TransactionManager, hasher: IHasher):
        self._tm = tm
        self._hasher = hasher


class CreateUser(UserUseCase):
    async def __call__(self, user_dto: CreateUserDTO) -> OutUserDTO:
        hashed_password = self._hasher.hash(user_dto.password)
        user = CreateUserDTODAO(
            email=user_dto.email,
            password=hashed_password,
            first_name=user_dto.first_name,
            last_name=user_dto.last_name,
            phone_number=user_dto.phone_number,
            image_url=user_dto.image_url
        )
        try:
            user_out = await self._tm.user_dao.create(user)
            await self._tm.commit()

        except UserAlreadyExist:
            logger.error(f"USER ALREADY EXISTS WITH THIS EMAIL {user_dto.email}")
            await self._tm.rollback()
            raise UserAlreadyExist(email=user_dto.email)

        return OutUserDTO(
            user_id=user_out.user_id,
            first_name=user_out.first_name,
            last_name=user_out.last_name,
            email=user_out.email
        )


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

    async def create_user(self, user_dto) -> OutUserDTO:
        return await CreateUser(self._tm, self._hasher)(user_dto)

    async def get_user_by_email(self, email: str) -> UserDTO:
        return await GetUserByEmail(self._tm, self._hasher)(email)
