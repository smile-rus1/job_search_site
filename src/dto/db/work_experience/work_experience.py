from dataclasses import dataclass
from datetime import date

from src.dto.base_dto import BaseDTO


@dataclass
class BaseWorkExperienceDTODAO(BaseDTO):
    resume_id: int
    company_name: str
    start_date: date
    work_experience_id: int | None = None
    end_date: date | None = None
    description_work: str | None = None
