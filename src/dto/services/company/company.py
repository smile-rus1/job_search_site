from dataclasses import dataclass

from src.dto.base_dto import BaseDTO
from src.dto.services.user.user import CreateUserDTO, UserOutDTO, BaseUserDTO


@dataclass
class BaseCompanyDTO(BaseDTO):
    user: BaseUserDTO
    company_name: str | None = None
    description_company: str | None = None
    address: str | None = None
    company_is_confirmed: bool | None = None


@dataclass
class CreateCompanyDTO(BaseDTO):
    user: CreateUserDTO
    company_name: str
    description_company: str | None = None
    address: str | None = None


@dataclass
class UpdateCompanyDTO(BaseDTO):
    user_id: int
    email: str
    company_name: str | None = None
    description_company: str | None = None
    address: str | None = None


@dataclass
class CompanyOutDTO(BaseDTO):
    user: UserOutDTO
    type: str = "company"


@dataclass
class CompanyDTO(BaseDTO):
    company_id: int
    user: BaseUserDTO
    company_name: str
    address: str | None
    description_company: str | None


@dataclass
class SearchDTO(BaseDTO):
    company_name: str | None
    offset: int = 0
    limit: int = 0


@dataclass
class CompanyDataDTO(BaseDTO):
    company_id: int
    company_name: str
    description_company: str | None
    address: str | None
