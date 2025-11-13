from abc import ABC

from loguru import logger

from src.exceptions.infrascructure.user.user import UserNotFoundByEmail
from src.dto.services.user.user import UserDTO, UpdateUserDTO
from src.exceptions.infrascructure.user.user import UserAlreadyExist
from src.exceptions.services.auth import InvalidEmail
from src.interfaces.infrastructure.hasher import IHasher
from src.interfaces.services.transaction_manager import IBaseTransactionManager


class UserUseCase(ABC):
    def __init__(self, tm: IBaseTransactionManager, hasher: IHasher):
        self._tm = tm
        self._hasher = hasher


class GetUserByEmail(UserUseCase):
    async def __call__(self, email: str) -> UserDTO:
        try:
            user = await self._tm.user_dao.get_user_by_email(email)

        except UserNotFoundByEmail:
            logger.bind(
                app_name=f"{GetUserByEmail.__name__}"
            ).error(f"NOT FOUND user with EMAIL: {email}")
            raise InvalidEmail(email)

        return UserDTO(
            user_id=user.user_id,
            email=user.email,
            last_name=user.last_name,
            first_name=user.first_name,
            created_at=user.created_at,
            updated_at=user.updated_at,
            type=user.type
        )


class UpdateUser(UserUseCase):
    async def __call__(self, user_dto: UpdateUserDTO) -> None:
        if user_dto.password is not None:
            hashed_password = self._hasher.hash(user_dto.password)
            user_dto.password = hashed_password
        user = UpdateUserDTODAO(**user_dto.__dict__)

        try:
            await self._tm.user_dao.update_user(user)
            await self._tm.commit()

        except UserAlreadyExist:
            logger.bind(
                app_name=f"{UpdateUser.__name__}"
            ).error(f"WITH DATA {user_dto}")
            await self._tm.rollback()

            raise UserAlreadyExist(user_dto.email)


class UserService:
    def __init__(self, tm: IBaseTransactionManager, hasher: IHasher):
        self._tm = tm
        self._hasher = hasher

    async def get_user_by_email(self, email: str) -> UserDTO:
        return await GetUserByEmail(self._tm, self._hasher)(email)

    async def update_user(self, user_data: UpdateUserDTO) -> None:
        await UpdateUser(self._tm, self._hasher)(user_data)
