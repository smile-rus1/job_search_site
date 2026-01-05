from dataclasses import dataclass
from datetime import datetime

from src.core.enums import ActorType
from src.dto.base_dto import BaseDTO
from src.dto.db.user.user import BaseUserDTODAO


@dataclass
class BaseMessageDTODAO(BaseDTO):
    message_id: int | None
    user: BaseUserDTODAO | None
    sender_type: ActorType | None
    message_text: str | None = None
    created_at: datetime | None = None
