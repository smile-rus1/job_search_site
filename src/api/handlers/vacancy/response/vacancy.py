from datetime import datetime

from pydantic import BaseModel

from src.api.handlers.company.response.company import CompanyOut
from src.api.handlers.vacancy.response.vacancy_access import VacancyAccessResponse
from src.api.handlers.vacancy.response.vacancy_type import VacancyTypeResponse
from src.core.enums import (
    Currency,
    EmploymentType,
    WorkScheduleType,
)


class VacancyResponse(BaseModel):
    company: CompanyOut | None = None
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
    vacancy_type: VacancyTypeResponse | None = None
    vacancy_access: VacancyAccessResponse | None = None


class VacancyTimeResponse(BaseModel):
    next_update_in_hours: float
    next_time_update: datetime


class VacancyLikedResponse(BaseModel):
    company_id: int
    company_name: str
    vacancy_id: int
    title: str
    is_published: bool
    address: str | None = None
    experience_start: int | None = None
    experience_end: int | None = None
