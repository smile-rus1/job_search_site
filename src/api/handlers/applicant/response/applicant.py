from datetime import date

from pydantic import BaseModel

from src.api.handlers.user.response.user import UserOut
from src.core.enums import EducationEnum, GenderEnum


class ApplicantOut(BaseModel):
    user: UserOut
    gender: GenderEnum
    address: str
    level_education: EducationEnum
    is_confirmed: bool | None = None
    description_applicant: str | None = None
    date_born: date | None = None
