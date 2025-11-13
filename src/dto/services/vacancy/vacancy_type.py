from dataclasses import dataclass

from src.dto.base_dto import BaseDTO
from src.infrastructure.enums import VacancyDuration


@dataclass
class BaseVacancyTypeDTO(BaseDTO):
    vacancy_types_id: int | None = None
    name: str | None = None


@dataclass
class CreateVacancyType(BaseDTO):
    name: str
    duration: VacancyDuration
