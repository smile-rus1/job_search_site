from src.dto.db.company.company import SearchDTODAO, BaseCompanyDTODAO


class ICompanyDAO:
    async def create_company(self, company: BaseCompanyDTODAO) -> BaseCompanyDTODAO:
        raise NotImplementedError

    async def update_company(self, company: BaseCompanyDTODAO) -> None:
        raise NotImplementedError

    async def get_company_by_id(self, user_id: int) -> BaseCompanyDTODAO:
        raise NotImplementedError

    async def search_company(self, search_dto: SearchDTODAO) -> list[BaseCompanyDTODAO]:
        raise NotImplementedError

