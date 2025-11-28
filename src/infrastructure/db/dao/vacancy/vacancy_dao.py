from dataclasses import asdict
from datetime import datetime, timedelta

from loguru import logger
from sqlalchemy import insert, select, update, delete, case, func, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, load_only

from src.dto.db.company.company import BaseCompanyDTODAO
from src.dto.db.user.user import BaseUserDTODAO
from src.dto.db.vacancy.vacancy import BaseVacancyDTODAO, BaseVacancyTypeDTODAO, BaseVacancyAccessDTODAO
from src.exceptions.infrascructure.vacancy.vacancy import (
    BaseVacancyException,
    VacancyException,
    VacancyTypeException,
    VacancyNotFoundByID, NotUpdatedTimeVacancy, VacancyAlreadyInLiked
)
from src.infrastructure.db.models import (
    VacancyDB,
    VacancyTypeDB,
    VacancyAccessDB,
    CompanyDB,
    UserDB
)
from src.infrastructure.db.models.vacancy import LikedVacancy
from src.core.enums import VacancyDuration
from src.interfaces.infrastructure.dao.vacancy_dao import IVacancyDAO
from src.interfaces.infrastructure.sqlalchemy_dao import SqlAlchemyDAO


class VacancyDAO(SqlAlchemyDAO, IVacancyDAO):
    async def create_vacancy(self, vacancy: BaseVacancyDTODAO) -> BaseVacancyDTODAO:
        subquery_vacancy_type = (
            select(VacancyTypeDB.vacancy_types_id)
            .where(
                VacancyTypeDB.name == vacancy.vacancy_type.name
            )
            .scalar_subquery()
        )

        sql = (
            insert(VacancyDB)
            .values(
                title=vacancy.title,
                description=vacancy.description,
                location=vacancy.location,
                key_skills=vacancy.key_skills,
                profession=vacancy.profession,
                salary_min=vacancy.salary_min,
                salary_max=vacancy.salary_max,
                salary_currency=vacancy.salary_currency,
                type_of_employment=vacancy.type_of_employment,
                type_work_schedule=vacancy.type_work_schedule,
                company_id=vacancy.company.user.user_id,
                vacancy_type_id=subquery_vacancy_type,
                experience_start=vacancy.experience_start,
                experience_end=vacancy.experience_end,
            )
            .returning(VacancyDB.vacancy_id)
        )
        try:
            res = await self._session.execute(sql)

        except IntegrityError as exc:
            logger.bind(
                app_name=f"{VacancyDAO.__name__} in {self.create_vacancy.__name__}"

            ).error(f"WITH DATA {vacancy}\nMESSAGE: {exc}")

            raise self._error_parser(vacancy, exc)

        vacancy_id = res.scalar_one()
        duration_days = int(VacancyDuration(vacancy.vacancy_type.vacancy_type_price.duration).value)

        sql_create_vacancy_access = (
            insert(VacancyAccessDB)
            .values(
                vacancy_id=vacancy_id,
                duration=vacancy.vacancy_type.vacancy_type_price.duration,
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(days=duration_days)
            )
        )

        try:
            await self._session.execute(sql_create_vacancy_access)

        except IntegrityError as exc:
            logger.bind(
                app_name=f"{VacancyDAO.__name__} in {self.create_vacancy.__name__}"
            ).error(f"WITH DATA {vacancy}\nEXCEPTION IN CREATE VACANCY_ACCESS: {exc}")
            raise self._error_parser(vacancy, exc)

        vacancy.vacancy_id = vacancy_id
        vacancy.created_at = datetime.now()
        vacancy.is_published = True

        return vacancy

    async def update_vacancy(self, vacancy: BaseVacancyDTODAO) -> None:
        data = asdict(vacancy)
        vacancy_update = {
            k: v for k, v in data.items() if v is not None and k not in {"vacancy_id", "user", "company"}
        }

        sql = (
            update(VacancyDB)
            .where(
                VacancyDB.vacancy_id == vacancy.vacancy_id,
                VacancyDB.company_id == vacancy.company.user.user_id
            )
            .values(**vacancy_update)
        )

        try:
            await self._session.execute(sql)
        except IntegrityError as exc:
            logger.bind(
                app_name=f"{VacancyDAO.__name__} in {self.update_vacancy.__name__}"
            ).error(f"WITH DATA {vacancy}\nEXCEPTION IN UPDATE VACANCY: {exc}")
            raise self._error_parser(vacancy, exc)

    async def get_vacancy_by_id(self, vacancy_id: int) -> BaseVacancyDTODAO:
        sql = (
            select(VacancyDB)
            .options(
                joinedload(VacancyDB.company)
                .load_only(
                    UserDB.user_id,
                    UserDB.email,
                    UserDB.image_url,
                    CompanyDB.company_name,
                    CompanyDB.address,
                    CompanyDB.company_is_confirmed,
                ),
                joinedload(VacancyDB.vacancy_type)
                .load_only(VacancyTypeDB.name),
                joinedload(VacancyDB.access)
                .load_only(
                    VacancyAccessDB.duration,
                    VacancyAccessDB.start_date,
                    VacancyAccessDB.end_date,
                    VacancyAccessDB.is_active,
                ),
                load_only(
                    VacancyDB.title,
                    VacancyDB.description,
                    VacancyDB.location,
                    VacancyDB.key_skills,
                    VacancyDB.profession,
                    VacancyDB.salary_min,
                    VacancyDB.salary_max,
                    VacancyDB.salary_currency,
                    VacancyDB.type_work_schedule,
                    VacancyDB.type_of_employment,
                    VacancyDB.updated_at,
                    VacancyDB.is_published,
                    VacancyDB.is_confirmed,
                    VacancyDB.experience_start,
                    VacancyDB.experience_end,
                )
            )
            .where(VacancyDB.vacancy_id == vacancy_id)
        )

        result = await self._session.execute(sql)
        vacancy = result.scalars().one_or_none()

        if vacancy is None:
            raise VacancyNotFoundByID(vacancy_id)

        return BaseVacancyDTODAO(
            vacancy_id=vacancy_id,
            title=vacancy.title,
            description=vacancy.description,
            location=vacancy.location,
            key_skills=vacancy.key_skills,
            profession=vacancy.profession,
            salary_min=vacancy.salary_min,
            salary_max=vacancy.salary_max,
            salary_currency=vacancy.salary_currency,
            type_of_employment=vacancy.type_of_employment,
            type_work_schedule=vacancy.type_work_schedule,
            updated_at=vacancy.updated_at,
            is_published=vacancy.is_published,
            is_confirmed=vacancy.is_confirmed,
            experience_start=vacancy.experience_start,
            experience_end=vacancy.experience_end,
            company=BaseCompanyDTODAO(
                user=BaseUserDTODAO(
                    user_id=vacancy.company.user_id,
                    email=vacancy.company.email,
                    image_url=vacancy.company.image_url
                ),
                company_name=vacancy.company.company_name,
                address=vacancy.company.address,
                company_is_confirmed=vacancy.company.company_is_confirmed
            ),
            vacancy_access=BaseVacancyAccessDTODAO(
                duration=vacancy.access.duration,
                start_date=vacancy.access.start_date,
                end_date=vacancy.access.end_date,
                is_active=vacancy.access.is_active
            ),
            vacancy_type=BaseVacancyTypeDTODAO(
                name=vacancy.vacancy_type.name
            ),
        )

    async def delete_vacancy(self, vacancy_id: int, company_id: int) -> None:
        sql = (
            delete(VacancyDB)
            .where(
                VacancyDB.vacancy_id == vacancy_id,
                VacancyDB.company_id == company_id
            )
        )
        await self._session.execute(sql)

    async def change_visibility_vacancy(self, vacancy_id: int, company_id: int, published: bool):
        sql = (
            update(VacancyDB)
            .where(
                VacancyDB.vacancy_id == vacancy_id,
                VacancyDB.company_id == company_id
            )
            .values(
                is_published=published
            )
        )
        await self._session.execute(sql)

    async def raise_vacancy_in_search(self, vacancy_id: int, company_id: int) -> dict:
        """
        Тут можно будет задать логику, чтобы нельзя было "поднимать" ваку бесконечно
        Допустим, будет все зависеть от типа вакансии:
        free (раз в 8 часов)
        paid (раз в 6 часа)
        premium (раз в 3 часа)

        """
        # subquery = (
        #     select(VacancyDB.vacancy_id)
        #     .join(VacancyTypeDB, VacancyDB.vacancy_type_id == VacancyTypeDB.vacancy_types_id)
        #     .where(
        #         VacancyDB.vacancy_id == vacancy_id,
        #         VacancyDB.company_id == company_id,
        #         case(
        #             (VacancyTypeDB.name == "free", VacancyDB.updated_at <= func.now() - text("interval '8 hour'")),
        #             (VacancyTypeDB.name == "paid", VacancyDB.updated_at <= func.now() - text("interval '6 hour'")),
        #             (VacancyTypeDB.name == "premium", VacancyDB.updated_at <= func.now() - text("interval '3 hour'")),
        #         )
        #     )
        #     .scalar_subquery()
        # )
        # sql = (
        #     update(VacancyDB)
        #     .where(VacancyDB.vacancy_id == subquery)
        #     .values(updated_at=func.now())
        # )
        # res = await self._session.execute(sql)
        # if res.rowcount == 0:
        #     raise

        sql_time_check = (
            select(
                VacancyDB.vacancy_id,
                VacancyDB.title,
                VacancyTypeDB.name.label("type"),
                (
                    (
                            case(
                                (VacancyTypeDB.name == "free", text("interval '8 hour'")),
                                (VacancyTypeDB.name == "paid", text("interval '6 hour'")),
                                (VacancyTypeDB.name == "premium", text("interval '3 hour'")),
                            )
                            - (func.now() - VacancyDB.updated_at)
                    )
                ).label("time_left")
            )
            .join(VacancyTypeDB, VacancyDB.vacancy_type_id == VacancyTypeDB.vacancy_types_id)
            .where(
                VacancyDB.vacancy_id == vacancy_id,
                VacancyDB.company_id == company_id
            )
        )

        row = (await self._session.execute(sql_time_check)).first()
        vacancy_type = row.type
        if not row:
            raise VacancyNotFoundByID(vacancy_id)

        time_left = row.time_left
        if time_left is not None and time_left.total_seconds() > 0:
            hours = round(time_left.total_seconds() / 3600, 2)
            raise NotUpdatedTimeVacancy(row.title, hours)

        sql = (
            update(VacancyDB)
            .where(VacancyDB.vacancy_id == vacancy_id, VacancyDB.company_id == company_id)
            .values(updated_at=func.now())
        )
        res = await self._session.execute(sql)

        if res.rowcount == 0:
            raise BaseVacancyException()

        limits = {"free": 8, "paid": 6, "premium": 3}
        now = datetime.now()
        next_update_delta = timedelta(hours=limits.get(vacancy_type, 8))
        next_update_time = now + next_update_delta

        return {
            "next_update_in_hours": limits.get(vacancy_type, 8),
            "next_time_update": next_update_time
        }

    async def like_vacancy_by_applicant(self, vacancy_id: int, applicant_id: int) -> None:
        sql = (
            insert(LikedVacancy)
            .values(
                vacancy_id=vacancy_id,
                applicant_id=applicant_id
            )
        )

        try:
            await self._session.execute(sql)

        except IntegrityError as exc:
            logger.bind(
                app_name=f"{VacancyDAO.__name__} in {self.like_vacancy_by_applicant.__name__}"
            ).error(f"EXCEPTION IN LIKE VACANCY: {exc}")
            raise self._error_parser(None, exc, vacancy_id=vacancy_id)

    async def dislike_vacancy_by_applicant(self, vacancy_id: int, applicant_id: int) -> None:
        sql = (
            delete(LikedVacancy)
            .where(
                LikedVacancy.vacancy_id == vacancy_id,
                LikedVacancy.applicant_id == applicant_id
            )
        )
        res = (await self._session.execute(sql)).rowcount
        if res == 0:
            logger.bind(
                app_name=f"{VacancyDAO.__name__} in {self.like_vacancy_by_applicant.__name__}"
            ).error(f"EXCEPTION IN DISLIKE VACANCY")
            raise VacancyNotFoundByID(vacancy_id)

    async def get_all_liked_vacancy(self, applicant_id: int) -> list[BaseVacancyDTODAO]:
        sql = (
            select(
                VacancyDB.vacancy_id,
                VacancyDB.title,
                VacancyDB.company_id,
                CompanyDB.company_name,
                CompanyDB.address,
                VacancyDB.is_published,
                VacancyDB.experience_start,
                VacancyDB.experience_end,
                LikedVacancy.applicant_id,
            )
            .join(CompanyDB, CompanyDB.company_id == VacancyDB.company_id)
            .join(LikedVacancy, LikedVacancy.vacancy_id == VacancyDB.vacancy_id)
            .where(LikedVacancy.applicant_id == applicant_id)
        )
        res = (await self._session.execute(sql)).all()
        return [
            BaseVacancyDTODAO(
                company=BaseCompanyDTODAO(
                    user=BaseUserDTODAO(
                        user_id=vacancy.company_id
                    ),
                    company_name=vacancy.company_name,
                    address=vacancy.address
                ),
                vacancy_id=vacancy.vacancy_id,
                title=vacancy.title,
                experience_start=vacancy.experience_start,
                experience_end=vacancy.experience_end,
                is_published=vacancy.is_published
            )
            for vacancy in res
        ]

    @staticmethod
    def _error_parser(
            vacancy: BaseVacancyDTODAO | None,
            exc: IntegrityError,
            **kwargs
    ) -> BaseVacancyException:
        error_text = str(exc.orig)
        if "vacancy_type_id" in error_text and "null value" in error_text.lower():
            return VacancyTypeException(name=vacancy.vacancy_type.name)

        if "uq_applicant_id_vacancy" in error_text:
            return VacancyAlreadyInLiked(kwargs.get("vacancy_id"))

        if "is not present in table" in error_text:
            return VacancyNotFoundByID(kwargs.get("vacancy_id"))

        return VacancyException()
