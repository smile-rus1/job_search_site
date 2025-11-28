from pydantic import BaseModel, Field

from src.api.handlers.vacancy.requests.vacancy_type import CreateVacancyTypeRequest
from src.core.enums import (
    Currency,
    EmploymentType,
    WorkScheduleType,
    VacancyDuration
)


class CreateVacancyRequest(BaseModel):
    title: str
    profession: str
    vacancy_type: CreateVacancyTypeRequest
    duration: VacancyDuration
    description: str | None = None
    location: str | None = None
    key_skills: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    salary_currency: Currency | None = None
    experience_start: int | None = Field(None, ge=0)
    experience_end: int | None = Field(None, ge=0)
    type_of_employment: list[EmploymentType] | None = None
    type_work_schedule: list[WorkScheduleType] | None = None


class UpdateVacancyRequest(BaseModel):
    title: str | None = None
    profession: str | None = None
    description: str | None = None
    location: str | None = None
    key_skills: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    salary_currency: Currency | None = None
    experience_start: int | None = Field(None, ge=0)
    experience_end: int | None = Field(None, ge=0)
    type_of_employment: list[EmploymentType] | None = None
    type_work_schedule: list[WorkScheduleType] | None = None
