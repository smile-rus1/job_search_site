from src.dto.db.user.user import BaseUserDTODAO


class IUserDAO:
    async def get_user_by_email(self, email: str) -> BaseUserDTODAO:
        raise NotImplementedError

    async def update_user(self, user: BaseUserDTODAO) -> None:
        raise NotImplementedError

    async def confirm_user(self, user: BaseUserDTODAO) -> bool:
        raise NotImplementedError
