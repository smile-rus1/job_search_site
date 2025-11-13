from pydantic import BaseModel


class CreateVacancyTypeRequest(BaseModel):
    name: str
