from pydantic import BaseModel

from src.api.handlers.user.response.user import UserOut


class CompanyOut(BaseModel):
    user: UserOut
    company_name: str
    address: str | None
    description_company: str | None
    company_is_confirmed: bool | None


class CompanyDataResponse(BaseModel):
    company_id: int
    company_name: str
    description_company: str | None
    address: str | None
