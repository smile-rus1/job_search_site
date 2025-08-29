from dataclasses import dataclass

from src.dto.base_dto import BaseDTO
from src.dto.db.user.user import UserOutDTODAO
from src.dto.services.user.user import CreateUserDTO, UserOutDTO
from src.infrastructure.enums import GenderEnum, EducationEnum


@dataclass
class BaseApplicantDTO(BaseDTO):
    ...


@dataclass
class ApplicantDTO(BaseApplicantDTO):
    user_id: int


@dataclass
class CreateApplicantDTO(BaseDTO):
    user: CreateUserDTO
    gender: GenderEnum
    description_applicant: str | None = None
    address: str | None = None
    level_education: EducationEnum | None = None


@dataclass
class ApplicantOutDTO(BaseDTO):
    user: UserOutDTO
    type: str = "applicant"
