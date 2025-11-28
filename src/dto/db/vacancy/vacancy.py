from dataclasses import dataclass
from datetime import datetime

from src.dto.base_dto import BaseDTO
from src.dto.db.company.company import BaseCompanyDTODAO
from src.core.enums import (
    Currency,
    EmploymentType,
    WorkScheduleType,
    VacancyDuration
)


@dataclass
class BaseVacancyTypePriceDTODAO(BaseDTO):
    vacancy_type_price_id: int | None = None
    duration: VacancyDuration | None = None
    price: float | None = None
    currency: Currency | None = None


@dataclass
class BaseVacancyTypeDTODAO(BaseDTO):
    vacancy_types_id: int | None = None
    name: str | None = None
    vacancy_type_price: BaseVacancyTypePriceDTODAO | None = None


@dataclass
class BaseVacancyAccessDTODAO(BaseDTO):
    vacancy_id: int | None = None
    duration: VacancyDuration | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    is_active: bool | None = None


@dataclass
class BaseVacancyDTODAO(BaseDTO):
    company: BaseCompanyDTODAO | None
    vacancy_id: int | None = None
    title: str | None = None
    description: str | None = None
    location: str | None = None
    key_skills: str | None = None
    profession: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    salary_currency: Currency | None = None
    type_of_employment: list[EmploymentType] | None = None
    type_work_schedule: list[WorkScheduleType] | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    is_published: bool | None = None
    is_confirmed: bool | None = None
    experience_start: int | None = None
    experience_end: int | None = None
    vacancy_type: BaseVacancyTypeDTODAO | None = None
    vacancy_access: BaseVacancyAccessDTODAO | None = None

    # по идее тут еще будут поля с других моделек допустим длительность, название вакансии (платная/без платной)
    #



