from datetime import date

from pydantic import BaseModel

from src.infrastructure.enums import GenderEnum, EducationEnum


class UpdateApplicantRequest(BaseModel):
    gender: GenderEnum | None = None
    description_applicant: str | None = None
    address: str | None = None
    level_education: EducationEnum | None = None
    date_born: date | None = None
