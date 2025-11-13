from pydantic import BaseModel


class VacancyTypeResponse(BaseModel):
    vacancy_types_id: int | None = None
    name: str | None = None
