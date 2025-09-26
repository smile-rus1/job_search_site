from dataclasses import dataclass
from datetime import date

from src.dto.base_dto import BaseDTO


@dataclass
class WorkExperienceDTODAO(BaseDTO):
    work_experience_id: int
    resume_id: int
    company_name: str
    start_date: date
    end_date: date | None = None
    description_work: str | None = None


@dataclass
class CreateWorkExperienceDTODAO(BaseDTO):
    resume_id: int
    applicant_id: int
    company_name: str
    start_date: date
    end_date: date | None = None
    description_work: str | None = None


@dataclass
class UpdateWorkExperienceDTODAO(BaseDTO):
    resume_id: int
    applicant_id: int
    work_experience_id: int
    company_name: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    description_work: str | None = None
