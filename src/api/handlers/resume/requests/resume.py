from pydantic import BaseModel

from src.infrastructure.enums import Currency, EmploymentType, GenderEnum


class CreateResumeRequest(BaseModel):
    name_resume: str
    profession: str
    key_skills: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    salary_currency: Currency | None = None
    location: str | None = None
    type_of_employment: list[EmploymentType] | None = None


class UpdateResumeRequest(BaseModel):
    name_resume: str | None = None
    profession: str | None = None
    key_skills: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    salary_currency: Currency | None = None
    location: str | None = None
    type_of_employment: list[EmploymentType] | None = None


class SearchResumeRequest(BaseModel):
    name_resume: str | None = None
    location: str | None = None
    profession: str | None = None
    gender: GenderEnum | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    salary_currency: Currency | None = None
    min_age: int | None = None
    max_age: int | None = None
    start_experience_years: int | None = None
    end_experience_years: int | None = None
    offset: int | None = None
    limit: int | None = None
