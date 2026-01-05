from dataclasses import dataclass
from datetime import datetime

from src.core.enums import ActorType
from src.dto.base_dto import BaseDTO
from src.dto.services.user.user import BaseUserDTO


@dataclass
class BaseMessageDTO(BaseDTO):
    message_id: int | None
    user: BaseUserDTO | None
    sender_type: ActorType | None
    message_text: str | None = None
    created_at: datetime | None = None


@dataclass
class CreateMessage(BaseDTO):
    user_id: int
    sender_type: ActorType | None
    message_text: str | None = None
