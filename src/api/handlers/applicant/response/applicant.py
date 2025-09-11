from pydantic import BaseModel

from src.api.handlers.user.response.user import UserOut
from src.infrastructure.enums import EducationEnum, GenderEnum


class ApplicantOut(BaseModel):
    user: UserOut
    gender: GenderEnum
    description_applicant: str
    address: str
    is_confirmed: bool
    level_education: EducationEnum
