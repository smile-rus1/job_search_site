from dataclasses import dataclass

from src.dto.base_dto import BaseDTO
from src.dto.services.user.user import CreateUserDTO, UserOutDTO
from src.infrastructure.enums import GenderEnum, EducationEnum


@dataclass
class BaseCompanyDTO(BaseDTO):
    ...


@dataclass
class ApplicantDTO(BaseCompanyDTO):
    user_id: int


@dataclass
class CreateCompanyDTO(BaseDTO):
    user: CreateUserDTO
    company_name: str
    description_company: str | None = None
    address: str | None = None


@dataclass
class CompanyOutDTO(BaseDTO):
    user: UserOutDTO
    type: str = "company"
