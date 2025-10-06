from dataclasses import asdict

from src.dto.db.company.company import BaseCompanyDTODAO
from src.interfaces.infrastructure.dao.company_dao import ICompanyDAO


class FakeCompanyDAO(ICompanyDAO):
    def __init__(self):
        self._storage: [BaseCompanyDTODAO] = []

    async def create_company(self, company: BaseCompanyDTODAO):
        self._storage.append(company)
        return company

    async def update_company(self, company: BaseCompanyDTODAO):
        company_dto: BaseCompanyDTODAO = next(
            com for com in self._storage if com.user.user_id == company.user.user_id
        )
        data = asdict(company)
        user = {k: v for k, v in data.pop("user").items() if v is not None and k not in {"user_id", "email"}}
        company_fields = {k: v for k, v in data.items() if v is not None}

        if user:
            company_fields["user"] = user

        for k, v in company_fields.items():
            setattr(company_dto, k, v)

    async def get_company_by_id(self, user_id: int):
        return next(
            (applicant for applicant in self._storage if applicant.user.user_id == user_id),
            None
        )

    async def search_company(self, search_dto):
        lst_companies = [
            com for com in self._storage if com.company_name == search_dto.company_name
        ]
        return lst_companies
