from dataclasses import dataclass
from datetime import datetime

from src.dto.base_dto import BaseDTO
from src.dto.services.company.company import BaseCompanyDTO
from src.dto.services.vacancy.vacancy_access import BaseVacancyAccessDTO
from src.dto.services.vacancy.vacancy_type import BaseVacancyTypeDTO, CreateVacancyType
from src.core.enums import Currency, EmploymentType, WorkScheduleType


@dataclass
class BaseVacancyDTO(BaseDTO):
    company: BaseCompanyDTO
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
    vacancy_type: BaseVacancyTypeDTO | None = None
    vacancy_access: BaseVacancyAccessDTO | None = None


@dataclass
class CreateVacancyDTO(BaseDTO):
    company: BaseCompanyDTO
    title: str
    profession: str
    vacancy_type: CreateVacancyType
    description: str | None = None
    location: str | None = None
    key_skills: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    salary_currency: Currency | None = None
    experience_start: int | None = None
    experience_end: int | None = None
    type_of_employment: EmploymentType | None = None
    type_work_schedule: WorkScheduleType | None = None


@dataclass
class UpdateVacancyDTO(BaseDTO):
    vacancy_id: int
    company: BaseCompanyDTO
    title: str | None = None
    profession: str | None = None
    description: str | None = None
    location: str | None = None
    key_skills: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    salary_currency: Currency | None = None
    type_of_employment: EmploymentType | None = None
    type_work_schedule: WorkScheduleType | None = None
    is_published: bool | None = None
    experience_start: int | None = None
    experience_end: int | None = None


@dataclass
class VacancyOutDTO(BaseDTO):
    vacancy_id: int
    title: str
    profession: str
    description: str | None = None
    location: str | None = None
    key_skills: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    experience_start: int | None = None
    experience_end: int | None = None
    salary_currency: Currency | None = None
    type_of_employment: EmploymentType | None = None
    type_work_schedule: WorkScheduleType | None = None
    created_at: datetime | None = None
    is_published: bool | None = None
