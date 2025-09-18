from src.dto.db.user.user import BaseUserDTODAO, UpdateUserDTODAO


class IUserDAO:
    async def get_user_by_email(self, email: str) -> BaseUserDTODAO:
        raise NotImplementedError

    async def update_user(self, user: UpdateUserDTODAO) -> None:
        raise NotImplementedError
