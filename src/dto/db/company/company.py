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
class SearchDTODAO(BaseDTO):
    company_name: str | None
    offset: int = 0
    limit: int = 0
