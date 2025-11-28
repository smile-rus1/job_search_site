import json
import uuid
from abc import ABC

from loguru import logger

from src.core.config_reader import config
from src.dto.db.company.company import SearchDTODAO, BaseCompanyDTODAO
from src.dto.db.user.user import BaseUserDTODAO
from src.dto.services.company.company import (
    CreateCompanyDTO,
    CompanyOutDTO,
    UpdateCompanyDTO,
    CompanyDTO,
    SearchDTO,
    CompanyDataDTO
)

from src.utils import utils
from src.dto.services.user.user import UserOutDTO, BaseUserDTO
from src.exceptions.infrascructure.user.user import UserAlreadyExist
from src.core.enums import TypeUser
from src.interfaces.infrastructure.hasher import IHasher
from src.interfaces.infrastructure.notifications import AbstractNotifications
from src.interfaces.infrastructure.redis_db import IRedisDB
from src.interfaces.services.transaction_manager import IBaseTransactionManager


class CompanyUseCase(ABC):
    def __init__(self, tm: IBaseTransactionManager, hasher: IHasher):
        self._tm = tm
        self._hasher = hasher


class CreateCompany(CompanyUseCase):
    async def __call__(
            self,
            company_dto: CreateCompanyDTO,
            notifications: AbstractNotifications,
            redis_db: IRedisDB
    ) -> CompanyOutDTO:
        hashed_password = self._hasher.hash(company_dto.user.password)
        company = BaseCompanyDTODAO(
            user=BaseUserDTODAO(
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
            company_created = await self._tm.company_dao.create_company(company)
            await self._tm.commit()

        except UserAlreadyExist:
            logger.bind(
                app_name=f"{CreateCompany.__name__}"
            ).error(f"WITH DATA {company_dto}")
            await self._tm.rollback()
            raise UserAlreadyExist(email=company_dto.user.email)

        token = uuid.uuid4().hex
        redis_key = config.auth.user_confirm_key.format(token=token)

        confirm_link = utils.create_confirm_link(token)

        await redis_db.set(
            key=redis_key,
            value=json.dumps({"user_id": company_created.user.user_id, "type": TypeUser.COMPANY.value}),
            expire=300
        )

        logger.bind(
            app_name=f"{CreateCompany.__name__}"
        ).info(f"LINK TO CONFIRM {confirm_link}")
        notifications.send(
            destination=company_created.user.email,
            template="confirm_email",
            data={
                "subject": "Подтвердите регистрацию",
                "body": f"Перейдите по ссылке для подтверждения: {confirm_link}"
            }
        )

        return CompanyOutDTO(
            user=UserOutDTO(
                user_id=company_created.user.user_id,
                last_name=company_created.user.last_name,
                first_name=company_created.user.first_name,
                email=company_created.user.email
            )
        )


class UpdateCompany(CompanyUseCase):
    async def __call__(self, company_dto: UpdateCompanyDTO) -> None:
        company = BaseCompanyDTODAO(
            user=BaseUserDTODAO(
                user_id=company_dto.user_id,
                email=company_dto.email,
            ),
            company_name=company_dto.company_name,
            description_company=company_dto.description_company,
            address=company_dto.address
        )

        try:
            await self._tm.company_dao.update_company(company)
            await self._tm.commit()

        except UserAlreadyExist:
            logger.bind(
                app_name=f"{UpdateCompany.__name__}"
            ).error(f"WITH DATA {company_dto}")
            await self._tm.rollback()
            raise UserAlreadyExist(company_dto.email)


class GetCompanyByID(CompanyUseCase):
    async def __call__(self, company_id: int) -> CompanyDTO:
        company_data = await self._tm.company_dao.get_company_by_id(company_id)
        return CompanyDTO(
            user=BaseUserDTO(
                last_name=company_data.user.last_name,
                first_name=company_data.user.first_name,
                email=company_data.user.email,
            ),
            company_id=company_data.user.user_id,
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
                company_id=company.user.user_id,
                company_name=company.company_name,
                description_company=company.description_company,
                address=company.address
            )
            for company in companies
        ]


class CompanyService:
    def __init__(
            self,
            tm: IBaseTransactionManager,
            hasher: IHasher,
            notifications: AbstractNotifications,
            redis_db: IRedisDB
    ):
        self._tm = tm
        self._hasher = hasher
        self._notifications = notifications
        self._redis_db = redis_db

    async def create_company(self, company_dto: CreateCompanyDTO) -> CompanyOutDTO:
        return await CreateCompany(tm=self._tm, hasher=self._hasher)(
            company_dto, self._notifications, self._redis_db
        )

    async def update_company(self, company_dto: UpdateCompanyDTO) -> None:
        return await UpdateCompany(tm=self._tm, hasher=self._hasher)(company_dto)

    async def get_company(self, company_id: int) -> CompanyDTO:
        return await GetCompanyByID(tm=self._tm, hasher=self._hasher)(company_id)

    async def search_companies(self, search_company_dto: SearchDTO) -> list[CompanyDataDTO]:
        return await SearchCompanies(tm=self._tm, hasher=self._hasher)(search_company_dto)
