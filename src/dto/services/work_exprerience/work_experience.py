from dataclasses import dataclass
from datetime import date

from src.dto.base_dto import BaseDTO


@dataclass
class WorkExperienceDTO(BaseDTO):
    work_experience_id: int
    resume_id: int
    company_name: str
    start_date: date
    end_date: date | None = None
    description_work: str | None = None
