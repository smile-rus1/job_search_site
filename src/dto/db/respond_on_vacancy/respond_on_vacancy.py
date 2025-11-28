from dataclasses import dataclass
from datetime import datetime

from src.core.enums import StatusRespond, ActorType
from src.dto.base_dto import BaseDTO
from src.dto.db.resume.resume import BaseResumeDTODAO
from src.dto.db.vacancy.vacancy import BaseVacancyDTODAO


@dataclass
class BaseRespondOnVacancyDTODAO(BaseDTO):
    user_id: int | None
    vacancy: BaseVacancyDTODAO | None
    resume: BaseResumeDTODAO | None
    response_id: int | None = None
    responder_type: ActorType = None
    status: StatusRespond | None = None
    response_date: datetime | None = None
    message: str | None = None
