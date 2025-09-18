from dataclasses import dataclass
from datetime import date

from src.dto.base_dto import BaseDTO
from src.dto.db.user.user import BaseUserDTODAO, UserOutDTODAO, CreateUserDTODAO, UserDTODAO
from src.infrastructure.enums import GenderEnum, EducationEnum


@dataclass
class BaseApplicantDTODAO(BaseDTO):
    user: BaseUserDTODAO
    description_applicant: str | None = None
    address: str | None = None
    gender: GenderEnum | None = None
    level_education: EducationEnum | None = None


@dataclass
class CreateApplicantDTODAO(BaseDTO):
    user: CreateUserDTODAO
    gender: GenderEnum
    description_applicant: str | None = None
    address: str | None = None
    level_education: EducationEnum | None = None
    date_born: date | None = None


@dataclass
class UpdateApplicantDTODAO(BaseDTO):
    user_id: int
    email: str
    gender: GenderEnum | None = None
    description_applicant: str | None = None
    address: str | None = None
    level_education: EducationEnum | None = None
    date_born: date | None = None


@dataclass
class ApplicantOutDTODAO(BaseDTO):
    user: UserOutDTODAO
    type: str = "applicant"


@dataclass
class ApplicantDTODAO(BaseDTO):
    applicant_id: int
    user: BaseUserDTODAO
    gender: GenderEnum
    description_applicant: str | None = None
    address: str | None = None
    is_confirmed: bool | None = None
    level_education: EducationEnum | None = None
    date_born: date | None = None
