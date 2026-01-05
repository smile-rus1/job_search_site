from abc import ABC

from loguru import logger

from src.dto.db.chat.chat import BaseChatDTODAO
from src.dto.db.chat.message import BaseMessageDTODAO
from src.dto.db.user.user import BaseUserDTODAO
from src.dto.services.chat.chat import CreateMessageInChatDTO, ChangeMessageDTO
from src.exceptions.infrascructure.chat.chat import BaseChatException
from src.interfaces.infrastructure.notifications import AbstractNotifications
from src.interfaces.services.transaction_manager import IBaseTransactionManager


class ChatUseCase(ABC):
    def __init__(self, tm: IBaseTransactionManager):
        self._tm = tm


class SendMessage(ChatUseCase):
    async def __call__(self, dto: CreateMessageInChatDTO):
        message_chat = BaseChatDTODAO(
            chat_id=dto.chat_id,
            message=BaseMessageDTODAO(
                user=BaseUserDTODAO(
                    user_id=dto.create_message.user_id
                ),
                message_id=None,
                message_text=dto.create_message.message_text,
                sender_type=dto.create_message.sender_type
            ),
            response_id=None,
            chat_type=None
        )

        try:
            res = await self._tm.chat_dao.send_message(chat=message_chat)
            await self._tm.commit()

        except BaseChatException as exc:
            logger.bind(
                app_name=f"{SendMessage.__name__}"
            ).error(f"WITH DATA {dto}")
            await self._tm.rollback()
            raise exc

        return  # тут что-то нужно будет вернуть


class ChangeMessage(ChatUseCase):
    async def __call__(self, dto: ChangeMessageDTO) -> None:
        message_chat = BaseChatDTODAO(
            chat_id=dto.chat_id,
            message=BaseMessageDTODAO(
                user=BaseUserDTODAO(
                    user_id=dto.user_id
                ),
                message_text=dto.message_text,
                message_id=dto.message_id,
                sender_type=None
            ),
            response_id=None,
            chat_type=None
        )
        try:
            await self._tm.chat_dao.change_message(message_chat)
            await self._tm.commit()

        except BaseChatException as exc:
            logger.bind(
                app_name=f"{ChangeMessage.__name__}"
            ).error(f"WITH DATA {dto}")
            await self._tm.rollback()
            raise exc


class DeleteMessageFromChat(ChatUseCase):
    async def __call__(self, user_id, message_id: int, chat_id: int):
        await self._tm.chat_dao.delete_message(user_id, message_id, chat_id)
        await self._tm.commit()


class UserHavePermissionsInChat(ChatUseCase):
    async def __call__(self, user_id: int, chat_id: int) -> bool:
        return await self._tm.chat_dao.user_have_permissions_in_chat(user_id, chat_id)


class ChatService:
    def __init__(
            self,
            tm: IBaseTransactionManager,
            notifications: AbstractNotifications,
    ):
        self._tm = tm
        self._notifications = notifications

    async def user_have_permissions_in_chat(self, user_id: int, chat_id: int) -> bool:
        return await UserHavePermissionsInChat(tm=self._tm)(user_id, chat_id)

    async def send_message(self, dto: CreateMessageInChatDTO):
        return await SendMessage(tm=self._tm)(dto)

    async def change_message(self, dto: ChangeMessageDTO) -> None:
        await ChangeMessage(tm=self._tm)(dto)

    async def delete_message(self, user_id, message_id: int, chat_id: int):
        await DeleteMessageFromChat(tm=self._tm)(user_id, message_id, chat_id)
