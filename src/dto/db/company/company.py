from dataclasses import dataclass

from src.dto.base_dto import BaseDTO
from src.dto.db.user.user import BaseUserDTODAO


@dataclass
class BaseCompanyDTODAO(BaseDTO):
    user: BaseUserDTODAO | None
    company_name: str | None = None
    description_company: str | None = None
    address: str | None = None
    company_is_confirmed: bool | None = None


@dataclass
class SearchDTODAO(BaseDTO):
    company_name: str | None
    offset: int = 0
    limit: int = 0
