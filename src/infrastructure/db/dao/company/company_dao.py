from dataclasses import asdict

from loguru import logger
from sqlalchemy import insert, update, select, Select, asc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from src.dto.db.company.company import (
    BaseCompanyDTODAO,
    SearchDTODAO
)
from src.dto.db.user.user import BaseUserDTODAO
from src.exceptions.base import BaseExceptions
from src.exceptions.infrascructure.user.user import UserAlreadyExist, UserNotFoundByID
from src.infrastructure.db.models import CompanyDB, UserDB
from src.infrastructure.enums import TypeUser
from src.interfaces.infrastructure.dao.company_dao import ICompanyDAO
from src.interfaces.infrastructure.sqlalchemy_dao import SqlAlchemyDAO


class CompanyDAO(SqlAlchemyDAO, ICompanyDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self._query_builder = CompanyQueryBuilder()

    async def create_company(self, company: BaseCompanyDTODAO) -> BaseCompanyDTODAO:
        user_sql = (
            insert(UserDB.__table__)  # type: ignore
            .values(
                email=company.user.email,
                password=company.user.password,
                first_name=company.user.first_name,
                last_name=company.user.last_name,
                phone_number=company.user.phone_number,
                image_url=company.user.image_url,
                type=TypeUser.COMPANY.value
            )
            .returning(UserDB.user_id)
        )

        try:
            result = await self._session.execute(user_sql)

        except IntegrityError as exc:
            logger.bind(
                app_name=f"{CompanyDAO.__name__} in {self.create_company.__name__}"
            ).error(f"WITH DATA {company}\nMESSAGE: {exc}")
            raise self._error_parser(company, exc)

        user_id = result.scalar_one()

        company_sql = (
            insert(CompanyDB.__table__)  # type: ignore
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
            logger.bind(
                app_name=f"{CompanyDAO.__name__} in {self.create_company.__name__}"
            ).error(f"WITH DATA {company}\nMESSAGE: {exc}")
            raise self._error_parser(company, exc)

        company_id = result.scalar_one()

        return BaseCompanyDTODAO(
            user=BaseUserDTODAO(
                user_id=company_id,
                email=company.user.email,
                first_name=company.user.first_name,
                last_name=company.user.last_name
            )
        )

    async def update_company(self, company: BaseCompanyDTODAO) -> None:
        data = asdict(company)
        user = {k: v for k, v in data.pop("user").items() if v is not None and k not in {"user_id", "email"}}
        company_fields = {k: v for k, v in data.items() if v is not None}

        if user:
            company_fields["user"] = user

        sql = (
            update(CompanyDB)
            .where(
                CompanyDB.company_id == UserDB.user_id,
                UserDB.email == company.user.email,
                CompanyDB.company_id == company.user.user_id
            )
            .values(**company_fields)
        )

        try:
            await self._session.execute(sql)

        except IntegrityError as exc:
            logger.bind(
                app_name=f"{CompanyDAO.__name__} in {self.create_company.__name__}"
            ).error(f"WITH DATA {company}\nMESSAGE: {exc}")
            raise self._error_parser(company, exc)

    async def get_company_by_id(self, user_id: int) -> BaseCompanyDTODAO:
        company_aliased = aliased(CompanyDB, flat=True)
        sql = (
            select(
                company_aliased.company_id,
                company_aliased.company_name,
                company_aliased.address,
                company_aliased.description_company,
                UserDB.email,
                UserDB.first_name,
                UserDB.last_name,
                UserDB.phone_number,
            )
            .join(UserDB, CompanyDB.company_id == UserDB.user_id)
            .where(CompanyDB.company_id == user_id)
        )
        result = await self._session.execute(sql)
        model = result.first()

        if model is None:
            raise UserNotFoundByID(user_id)

        return BaseCompanyDTODAO(
            user=BaseUserDTODAO(
                user_id=model.company_id,
                last_name=model.last_name,
                first_name=model.last_name,
                phone_number=model.phone_number,
                email=model.email
            ),
            address=model.address,
            company_name=model.company_name,
            description_company=model.description_company
        )

    async def search_company(self, search_dto: SearchDTODAO) -> list[BaseCompanyDTODAO]:
        sql = self._query_builder.get_query(
            company_name=search_dto.company_name,
            limit=search_dto.limit,
            offset=search_dto.offset
        )
        result = await self._session.execute(sql)
        models = result.all()

        return [
            BaseCompanyDTODAO(
                user=BaseUserDTODAO(
                    user_id=model.company_id,
                ),
                company_name=model.company_name,
                description_company=model.description_company,
                address=model.address
            )
            for model in models
        ]

    @staticmethod
    def _error_parser(
            company: BaseCompanyDTODAO,
            exc: IntegrityError
    ) -> BaseExceptions:
        database_column = exc.__cause__.__cause__.constraint_name  # type: ignore
        if database_column == "users_email_key":
            return UserAlreadyExist(company.user.email)


class CompanyQueryBuilder:
    def __init__(self):
        self._query = None

    def get_query(
            self,
            company_name: str | None,
            offset: int = 0,
            limit: int = 0
    ) -> Select:
        return (
            self._select(offset, limit)
            ._with_company_name(company_name)
            ._build()
        )

    def _select(self, offset: int = 0, limit: int = 0):
        self._query = (
            select(
                CompanyDB.company_id,
                CompanyDB.company_name,
                CompanyDB.address,
                CompanyDB.description_company,
            )
            .order_by(asc(CompanyDB.company_name))
            .limit(limit)
            .offset(offset)
        )
        return self

    def _with_company_name(self, company_name: str | None):
        if company_name is not None:
            self._query = self._query.where(CompanyDB.company_name.like(f"%{company_name}%"))
        return self

    def _build(self):
        return self._query
