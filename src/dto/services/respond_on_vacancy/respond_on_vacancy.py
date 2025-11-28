from dataclasses import dataclass
from datetime import datetime

from src.core.enums import ActorType, StatusRespond
from src.dto.base_dto import BaseDTO


@dataclass
class BaseRespondOnVacancyDTO(BaseDTO):
    response_id: int | None = None
    responder_type: ActorType = None
    status: StatusRespond | None = None
    response_date: datetime | None = None
    message: str | None = None


@dataclass
class CreateRespondOnVacancyDTO(BaseDTO):
    user_id: int
    vacancy_id: int
    resume_id: int
    response_id: int | None = None
    responder_type: ActorType = None
    response_date: datetime | None = None
    message: str | None = None
