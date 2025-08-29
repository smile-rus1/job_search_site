from abc import ABC

from loguru import logger

from src.dto.db.company.company import CreateCompanyDTODAO
from src.dto.db.user.user import CreateUserDTODAO
from src.dto.services.company.company import CreateCompanyDTO, CompanyOutDTO
from src.dto.services.user.user import UserOutDTO, CreateUserDTO
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


class CompanyService:
    def __init__(self, tm: TransactionManager, hasher: IHasher):
        self._tm = tm
        self._hasher = hasher

    async def create_company(self, applicant_dto: CreateCompanyDTO) -> CompanyOutDTO:
        return await CreateCompany(tm=self._tm, hasher=self._hasher)(applicant_dto)

