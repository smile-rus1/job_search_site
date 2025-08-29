from dataclasses import dataclass

from src.dto.base_dto import BaseDTO
from src.dto.db.user.user import BaseUserDTODAO, UserOutDTODAO, CreateUserDTODAO
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


@dataclass
class ApplicantOutDTODAO(BaseDTO):
    user: UserOutDTODAO
    type: str = "applicant"
