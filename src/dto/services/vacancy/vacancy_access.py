from dataclasses import dataclass
from datetime import datetime

from src.dto.base_dto import BaseDTO
from src.infrastructure.enums import VacancyDuration


@dataclass
class BaseVacancyAccessDTO(BaseDTO):
    vacancy_id: int | None = None
    duration: VacancyDuration | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    is_active: bool | None = None
