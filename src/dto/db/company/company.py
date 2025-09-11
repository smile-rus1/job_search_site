from dataclasses import dataclass

from src.dto.base_dto import BaseDTO
from src.dto.db.user.user import BaseUserDTODAO, UserOutDTODAO, CreateUserDTODAO


@dataclass
class BaseCompanyDTODAO(BaseDTO):
    user: BaseUserDTODAO
    company_name: str | None = None
    description_company: str | None = None
    address: str | None = None


@dataclass
class CreateCompanyDTODAO(BaseDTO):
    user: CreateUserDTODAO
    company_name: str
    description_company: str | None = None
    address: str | None = None


@dataclass
class UpdateCompanyDTODAO(BaseDTO):
    user_id: int
    email: str
    company_name: str | None = None
    description_company: str | None = None
    address: str | None = None


@dataclass
class CompanyOutDTODAO(BaseDTO):
    user: UserOutDTODAO
    type: str = "company"


@dataclass
class CompanyDTODAO(BaseDTO):
    company_id: int
    user: BaseUserDTODAO
    company_name: str
    description_company: str | None
    address: str | None


@dataclass
class SearchDTODAO(BaseDTO):
    company_name: str | None
    offset: int = 0
    limit: int = 0


@dataclass
class CompanyDataDTODAO(BaseDTO):
    company_id: int
    company_name: str
    description_company: str | None
    address: str | None
