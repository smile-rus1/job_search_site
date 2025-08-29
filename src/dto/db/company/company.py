from dataclasses import dataclass

from src.dto.base_dto import BaseDTO
from src.dto.db.user.user import BaseUserDTODAO, UserOutDTODAO, CreateUserDTODAO


@dataclass
class BaseApplicantDTODAO(BaseDTO):
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
class CompanyOutDTODAO(BaseDTO):
    user: UserOutDTODAO
    type: str = "company"
