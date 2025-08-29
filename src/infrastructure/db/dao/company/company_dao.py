from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

from src.dto.db.company.company import CompanyOutDTODAO, CreateCompanyDTODAO
from src.dto.db.user.user import UserOutDTODAO
from src.exceptions.base import BaseExceptions
from src.exceptions.infrascructure.user.user import UserAlreadyExist
from src.infrastructure.db.dao.base_dao import BaseDAO
from src.infrastructure.db.models import CompanyDB, UserDB


class CompanyDAO(BaseDAO):
    async def create(self, company: CreateCompanyDTODAO) -> CompanyOutDTODAO:
        user_sql = (
            insert(UserDB.__table__)
            .values(
                email=company.user.email,
                password=company.user.password,
                first_name=company.user.first_name,
                last_name=company.user.last_name,
                phone_number=company.user.phone_number,
                image_url=company.user.image_url,
                type="company"
            )
            .returning(UserDB.user_id)
        )

        try:
            result = await self._session.execute(user_sql)
        except IntegrityError as exc:
            raise self._error_parser(company, exc)

        user_id = result.scalar_one()

        company_sql = (
            insert(CompanyDB.__table__)
            .values(
                company_id=user_id,
                company_name=company.company_name,
                description_company=company.description_company,
                address=company.address
            ).returning(CompanyDB.company_id)
        )

        try:
            result = await self._session.execute(company_sql)
        except IntegrityError as exc:
            raise self._error_parser(company, exc)

        company_id = result.scalar_one()

        return CompanyOutDTODAO(
            user=UserOutDTODAO(
                user_id=company_id,
                email=company.user.email,
                first_name=company.user.first_name,
                last_name=company.user.last_name
            )
        )
    
    @staticmethod
    def _error_parser(company: CreateCompanyDTODAO, exc: IntegrityError) -> BaseExceptions:
        database_column = exc.__cause__.__cause__.constraint_name
        if database_column == "users_email_key":
            return UserAlreadyExist(company.user.email)
