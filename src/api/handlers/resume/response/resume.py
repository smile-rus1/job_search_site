from datetime import datetime

from pydantic import BaseModel

from src.api.handlers.applicant.response.applicant import ApplicantOut
from src.api.handlers.work_experience.response.work_experience import WorkExperienceResponse
from src.core.enums import Currency, EmploymentType


class ResumeOutResponse(BaseModel):
    resume_id: int
    name_resume: str
    key_skills: str | None = None
    profession: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    salary_currency: Currency | None = None
    location: str | None = None
    updated_at: datetime | None = None
    type_of_employment: list[EmploymentType] | None = None


class ResumeResponse(BaseModel):
    resume_id: int
    applicant: ApplicantOut
    name_resume: str
    profession: str
    key_skills: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    salary_currency: Currency | None = None
    location: str | None = None
    work_experience: list[WorkExperienceResponse] | None = None
    type_of_employment: list[EmploymentType] | None = None


class ResumeSearchOutResponse(BaseModel):
    resume_id: int
    applicant: ApplicantOut
    name_resume: str | None = None
    profession: str | None = None
    key_skills: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    salary_currency: Currency | None = None
    location: str | None = None
    total_months: int | None = None
    work_experiences: list[WorkExperienceResponse] | None = None
