from dataclasses import dataclass
from datetime import datetime

from src.core.enums import ChatType
from src.dto.base_dto import BaseDTO
from src.dto.db.chat.message import BaseMessageDTODAO


@dataclass
class BaseChatDTODAO(BaseDTO):
    chat_id: int | None
    message: BaseMessageDTODAO | None
    chat_type: ChatType | None
    response_id: int | None
    created_at: datetime | None = None
