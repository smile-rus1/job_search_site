from abc import ABC

from loguru import logger

from src.dto.db.company.company import CreateCompanyDTODAO, UpdateCompanyDTODAO, SearchDTODAO
from src.dto.db.user.user import CreateUserDTODAO
from src.dto.services.company.company import (
    CreateCompanyDTO,
    CompanyOutDTO,
    UpdateCompanyDTO, CompanyDTO, SearchDTO, CompanyDataDTO
)
from src.dto.services.user.user import UserOutDTO, BaseUserDTO
from src.exceptions.infrascructure.user.user import UserAlreadyExist
from src.infrastructure.db.transaction_manager import TransactionManager
from src.interfaces.infrastructure.hasher import IHasher


class CompanyUseCase(ABC):
    def __init__(self, tm: TransactionManager, hasher: IHasher):
        self._tm = tm
        self._hasher = hasher


class CreateCompany(CompanyUseCase):
    async def __call__(self, company_dto: CreateCompanyDTO) -> CompanyOutDTO:
        hashed_password = self._hasher.hash(company_dto.user.password)
        company = CreateCompanyDTODAO(
            user=CreateUserDTODAO(
                email=company_dto.user.email,
                password=hashed_password,
                last_name=company_dto.user.last_name,
                first_name=company_dto.user.first_name,
                image_url=company_dto.user.image_url,
                phone_number=company_dto.user.phone_number
            ),
            address=company_dto.address,
            company_name=company_dto.company_name,
            description_company=company_dto.description_company,
        )

        try:
            applicant_created = await self._tm.company_dao.create(company)
            await self._tm.commit()

        except UserAlreadyExist:
            logger.error(f"USER ALREADY EXISTS WITH THIS EMAIL {company_dto.user.email}")
            await self._tm.rollback()
            raise UserAlreadyExist(email=company_dto.user.email)

        return CompanyOutDTO(
            user=UserOutDTO(
                user_id=applicant_created.user.user_id,
                last_name=company_dto.user.last_name,
                first_name=company_dto.user.first_name,
                email=company_dto.user.email
            )
        )


class UpdateCompany(CompanyUseCase):
    async def __call__(self, company_data: UpdateCompanyDTO) -> None:
        company = UpdateCompanyDTODAO(**company_data.__dict__)

        try:
            await self._tm.company_dao.update_company(company)
            await self._tm.commit()

        except UserAlreadyExist:
            logger.error(f"EXCEPTION IN UPDATE APPLICANT WITH EMAIL {company_data.email}")
            await self._tm.rollback()
            raise UserAlreadyExist(company_data.email)


class GetCompanyByID(CompanyUseCase):
    async def __call__(self, company_id: int) -> CompanyDTO:
        company_data = await self._tm.company_dao.get_company_by_id(company_id)
        return CompanyDTO(
            user=BaseUserDTO(
                last_name=company_data.user.last_name,
                first_name=company_data.user.first_name,
                email=company_data.user.email,
                updated_at=None,
                created_at=None
            ),
            company_id=company_data.company_id,
            address=company_data.address,
            company_name=company_data.company_name,
            description_company=company_data.description_company
        )


class SearchCompanies(CompanyUseCase):
    async def __call__(self, search_company_dto: SearchDTO) -> list[CompanyDataDTO]:
        search_dto = SearchDTODAO(**search_company_dto.__dict__)
        companies = await self._tm.company_dao.search_company(search_dto)

        return [
            CompanyDataDTO(
                company_id=company.company_id,
                company_name=company.company_name,
                description_company=company.description_company,
                address=company.address
            )
            for company in companies
        ]


class CompanyService:
    def __init__(self, tm: TransactionManager, hasher: IHasher):
        self._tm = tm
        self._hasher = hasher

    async def create_company(self, company_dto: CreateCompanyDTO) -> CompanyOutDTO:
        return await CreateCompany(tm=self._tm, hasher=self._hasher)(company_dto)

    async def update_company(self, company_dto: UpdateCompanyDTO) -> None:
        return await UpdateCompany(tm=self._tm, hasher=self._hasher)(company_dto)

    async def get_company(self, company_id: int) -> CompanyDTO:
        return await GetCompanyByID(tm=self._tm, hasher=self._hasher)(company_id)

    async def search_companies(self, search_company_dto: SearchDTO) -> list[CompanyDataDTO]:
        return await SearchCompanies(tm=self._tm, hasher=self._hasher)(search_company_dto)
