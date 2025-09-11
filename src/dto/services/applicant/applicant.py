from dataclasses import dataclass

from src.dto.base_dto import BaseDTO
from src.dto.services.user.user import CreateUserDTO, UserOutDTO, BaseUserDTO
from src.infrastructure.enums import GenderEnum, EducationEnum


@dataclass
class BaseApplicantDTO(BaseDTO):
    user: BaseUserDTO
    description_applicant: str | None = None
    address: str | None = None
    gender: GenderEnum | None = None
    level_education: EducationEnum | None = None


@dataclass
class ApplicantDTO(BaseDTO):
    applicant_id: int
    user: BaseUserDTO
    gender: GenderEnum
    description_applicant: str
    address: str
    is_confirmed: bool
    level_education: EducationEnum


@dataclass
class CreateApplicantDTO(BaseDTO):
    user: CreateUserDTO
    gender: GenderEnum
    description_applicant: str | None = None
    address: str | None = None
    level_education: EducationEnum | None = None


@dataclass
class UpdateApplicantDTO(BaseDTO):
    user_id: int
    email: str
    gender: GenderEnum | None = None
    description_applicant: str | None = None
    address: str | None = None
    level_education: EducationEnum | None = None


@dataclass
class ApplicantOutDTO(BaseDTO):
    user: UserOutDTO
    type: str = "applicant"
