from src.dto.db.company.company import CreateCompanyDTODAO, CompanyOutDTODAO, UpdateCompanyDTODAO, CompanyDTODAO, \
    CompanyDataDTODAO, SearchDTODAO


class ICompanyDAO:
    async def create_company(self, company: CreateCompanyDTODAO) -> CompanyOutDTODAO:
        raise NotImplementedError

    async def update_company(self, company: UpdateCompanyDTODAO) -> None:
        raise NotImplementedError

    async def get_company_by_id(self, user_id: int) -> CompanyDTODAO:
        raise NotImplementedError

    async def search_company(self, search_dto: SearchDTODAO) -> list[CompanyDataDTODAO]:
        raise NotImplementedError

