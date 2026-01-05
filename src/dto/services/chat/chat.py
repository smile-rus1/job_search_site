from dataclasses import dataclass
from datetime import datetime

from src.core.enums import ChatType
from src.dto.base_dto import BaseDTO
from src.dto.services.chat.message import BaseMessageDTO, CreateMessage


@dataclass
class BaseChatDTO(BaseDTO):
    chat_id: int | None
    message: BaseMessageDTO | None
    chat_type: ChatType | None
    response_id: int | None
    created_at: datetime | None = None


@dataclass
class CreateMessageInChatDTO(BaseDTO):
    chat_id: int | None
    create_message: CreateMessage


@dataclass
class ChangeMessageDTO(BaseDTO):
    chat_id: int
    message_id: int
    user_id: int
    message_text: str
