from dataclasses import dataclass

from src.dto.base_dto import BaseDTO
from src.infrastructure.enums import VacancyDuration, Currency


@dataclass
class BaseVacancyTypePriceDTO(BaseDTO):
    vacancy_type_price_id: int | None = None
    duration: VacancyDuration | None = None
    price: float | None = None
    currency: Currency | None = None
