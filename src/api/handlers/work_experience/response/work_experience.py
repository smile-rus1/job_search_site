from datetime import date

from pydantic import BaseModel


class WorkExperienceResponse(BaseModel):
    work_experience_id: int
    resume_id: int
    company_name: str
    start_date: date
    end_date: date | None = None
    description_work: str | None = None
