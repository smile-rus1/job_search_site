from dataclasses import dataclass
from datetime import date

from src.dto.base_dto import BaseDTO
from src.dto.db.user.user import BaseUserDTODAO
from src.infrastructure.enums import GenderEnum, EducationEnum


@dataclass
class BaseApplicantDTODAO(BaseDTO):
    user: BaseUserDTODAO
    description_applicant: str | None = None
    address: str | None = None
    gender: GenderEnum | None = None
    level_education: EducationEnum | None = None
    date_born: date | None = None
