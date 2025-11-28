from dataclasses import dataclass
from datetime import datetime

from src.dto.base_dto import BaseDTO
from src.dto.services.applicant.applicant import ApplicantDTO
from src.dto.services.work_exprerience.work_experience import WorkExperienceDTO
from src.core.enums import Currency, EmploymentType, GenderEnum


@dataclass
class BaseResumeDTO(BaseDTO):
    resume_id: int
    name_resume: str | None = None
    key_skills: str | None = None
    profession: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    salary_currency: Currency | None = None
    is_published: bool | None = None
    location: str | None = None
    updated_at: datetime | None = None
    type_of_employment: EmploymentType | None = None


@dataclass
class CreateResumeDTO(BaseDTO):
    applicant_id: int
    name_resume: str
    profession: str
    key_skills: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    salary_currency: Currency | None = None
    location: str | None = None
    type_of_employment: EmploymentType | None = None


@dataclass
class UpdateResumeDTO(BaseDTO):
    applicant_id: int
    resume_id: int
    name_resume: str | None = None
    profession: str | None = None
    key_skills: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    salary_currency: Currency | None = None
    location: str | None = None
    type_of_employment: EmploymentType | None = None


@dataclass
class ResumeDTO(BaseDTO):
    resume_id: int
    applicant: ApplicantDTO
    name_resume: str
    profession: str
    key_skills: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    salary_currency: Currency | None = None
    location: str | None = None
    work_experience: list[WorkExperienceDTO] | None = None
    type_of_employment: list[EmploymentType] | None = None


@dataclass
class ResumeOutDTO(BaseDTO):
    resume_id: int
    name_resume: str
    key_skills: str | None = None
    profession: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    salary_currency: Currency | None = None
    is_published: bool | None = None
    location: str | None = None
    updated_at: datetime | None = None
    type_of_employment: EmploymentType | None = None


@dataclass
class SearchResumeDTO(BaseDTO):
    name_resume: str | None = None
    location: str | None = None
    profession: str | None = None
    gender: GenderEnum | None = None
    type_of_employment: list[EmploymentType] | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    salary_currency: Currency | None = None
    min_age: int | None = None
    max_age: int | None = None
    start_experience_years: int | None = None
    end_experience_years: int | None = None
    offset: int | None = None
    limit: int | None = None


@dataclass
class ResumeSearchOutDTO(BaseDTO):
    resume_id: int
    applicant: ApplicantDTO
    name_resume: str | None = None
    profession: str | None = None
    key_skills: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    salary_currency: Currency | None = None
    location: str | None = None
    type_of_employment: list[EmploymentType] | None = None
    total_months: int | None = None
    work_experiences: list[WorkExperienceDTO] | None = None
