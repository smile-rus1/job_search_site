from src.dto.db.chat.chat import BaseChatDTODAO


class IChatDAO:
    async def send_message(self, chat: BaseChatDTODAO) -> BaseChatDTODAO:
        raise NotImplementedError

    async def change_message(self, chat: BaseChatDTODAO) -> None:
        raise NotImplementedError

    async def delete_message(self, user_id, message_id: int, chat_id: int):
        raise NotImplementedError

    async def user_have_permissions_in_chat(self, user_id: int, chat_id: int) -> bool:
        raise NotImplementedError
