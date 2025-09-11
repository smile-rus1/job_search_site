from pydantic import BaseModel


class UpdateCompanyRequest(BaseModel):
    company_name: str | None = None
    description_company: str | None = None
    address: str | None = None


class SearchCompanyRequest(BaseModel):
    company_name: str | None = None
    offset: int = 0
    limit: int = 100
