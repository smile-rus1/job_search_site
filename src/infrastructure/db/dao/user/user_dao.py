from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError

from src.dto.db.user.user import CreateUserDTODAO, UserOutDTODAO, BaseUserDTODAO, UpdateUserDTODAO
from src.exceptions.base import BaseExceptions
from src.exceptions.infrascructure.user.user import UserAlreadyExist, UserNotFoundByEmail
from src.infrastructure.db.dao.base_dao import BaseDAO
from src.infrastructure.db.models.user import UserDB


class UserDAO(BaseDAO):
    async def create(self, user: CreateUserDTODAO) -> UserOutDTODAO:
        sql = insert(UserDB).values(
            email=user.email,
            password=user.password,
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
            image_url=user.image_url
        ).returning(UserDB.user_id)

        try:
            result = await self._session.execute(sql)

        except IntegrityError as exc:
            raise self._error_parser(user, exc)

        row_id = result.scalar()

        return UserOutDTODAO(
            user_id=row_id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email
        )

    async def get_user_by_email(self, email: str) -> BaseUserDTODAO:
        sql = select(UserDB).where(UserDB.email == email)
        result = (await self._session.execute(sql)).scalar()

        if not result:
            raise UserNotFoundByEmail(email)

        return BaseUserDTODAO(
            user_id=result.user_id,
            email=result.email,
            password=result.password,
            first_name=result.first_name,
            last_name=result.last_name,
            updated_at=result.updated_at,
            is_admin=result.is_admin,
            is_superuser=result.is_superuser
        )

    async def update_user(self, user: UpdateUserDTODAO) -> None:
        data_dict = user.__dict__

        update_values = {
            k: v for k, v in data_dict.items()
            if v is not None and k != "user_id" and k != "email"
        }
        sql = (
            update(UserDB)
            .where(
                UserDB.user_id == user.user_id,
                UserDB.email == user.email
            )
            .values(**update_values)
        )

        try:
            await self._session.execute(sql)

        except IntegrityError as exc:
            raise self._error_parser(user, exc)

    @staticmethod
    def _error_parser(
            user: CreateUserDTODAO | UpdateUserDTODAO | BaseUserDTODAO,
            exc: IntegrityError
    ) -> BaseExceptions:
        database_column = exc.__cause__.__cause__.constraint_name
        if database_column == "users_email_key":
            return UserAlreadyExist(user.email)
