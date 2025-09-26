from datetime import date

from pydantic import BaseModel


class CreateWorkExperienceRequest(BaseModel):
    company_name: str
    start_date: date
    end_date: date | None = None
    description_work: str | None = None


class UpdateWorkExperienceRequest(BaseModel):
    company_name: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    description_work: str | None = None
