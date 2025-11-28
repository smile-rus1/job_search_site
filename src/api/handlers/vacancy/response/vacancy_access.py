from datetime import datetime

from pydantic import BaseModel

from src.core.enums import VacancyDuration


class VacancyAccessResponse(BaseModel):
    duration: VacancyDuration | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    is_active: bool | None = None
