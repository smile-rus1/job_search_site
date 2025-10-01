from loguru import logger
from sqlalchemy import insert, update, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import aliased

from src.dto.db.applicant.applicant import (
    ApplicantOutDTODAO,
    CreateApplicantDTODAO,
    UpdateApplicantDTODAO,
    BaseApplicantDTODAO, ApplicantDTODAO
)
from src.dto.db.user.user import UserOutDTODAO, BaseUserDTODAO
from src.exceptions.base import BaseExceptions
from src.exceptions.infrascructure.user.user import UserAlreadyExist, UserNotFoundByID
from src.infrastructure.db.models import ApplicantDB, UserDB
from src.infrastructure.enums import TypeUser
from src.interfaces.infrastructure.dao.applicant_dao import IApplicantDAO
from src.interfaces.infrastructure.sqlalchemy_dao import SqlAlchemyDAO


class ApplicantDAO(SqlAlchemyDAO, IApplicantDAO):
    async def create_applicant(self, applicant: CreateApplicantDTODAO) -> ApplicantOutDTODAO:
        user_sql = (
            insert(UserDB.__table__)
            .values(
                email=applicant.user.email,
                password=applicant.user.password,
                first_name=applicant.user.first_name,
                last_name=applicant.user.last_name,
                phone_number=applicant.user.phone_number,
                image_url=applicant.user.image_url,
                type=TypeUser.APPLICANT.value
            )
            .returning(UserDB.user_id)
        )

        try:
            result = await self._session.execute(user_sql)

        except IntegrityError as exc:
            logger.info(f"EXCEPTION IN 'create_applicant': {exc}")
            raise self._error_parser(applicant, exc)

        user_id = result.scalar_one()

        applicant_sql = (
            insert(ApplicantDB.__table__)
            .values(
                applicant_id=user_id,
                description_applicant=applicant.description_applicant,
                address=applicant.address,
                gender=applicant.gender,
                level_education=applicant.level_education,
                date_born=applicant.date_born
            )
            .returning(ApplicantDB.applicant_id)
        )
        try:
            result = await self._session.execute(applicant_sql)

        except IntegrityError as exc:
            logger.info(f"EXCEPTION IN 'create_applicant': {exc}")
            raise self._error_parser(applicant, exc)

        applicant_id = result.scalar_one()

        return ApplicantOutDTODAO(
            user=UserOutDTODAO(
                user_id=applicant_id,
                email=applicant.user.email,
                first_name=applicant.user.first_name,
                last_name=applicant.user.last_name
            )
        )

    async def update_applicant(self, applicant: UpdateApplicantDTODAO) -> None:
        data_dict = applicant.__dict__

        update_values = {
            k: v for k, v in data_dict.items()
            if v is not None and k != "user_id" and k != "email"
        }
        sql = (
            update(ApplicantDB)
            .where(
                ApplicantDB.applicant_id == UserDB.user_id,
                UserDB.email == applicant.email,
                ApplicantDB.applicant_id == applicant.user_id
            )
            .values(**update_values)
        )

        try:
            await self._session.execute(sql)

        except IntegrityError as exc:
            logger.info(f"EXCEPTION IN 'update_applicant': {exc}")
            raise self._error_parser(applicant, exc)

    async def get_applicant_by_id(self, user_id: int) -> ApplicantDTODAO:
        applicant_aliased = aliased(ApplicantDB, flat=True)
        sql = (
            select(
                applicant_aliased.applicant_id,
                applicant_aliased.description_applicant,
                applicant_aliased.address,
                applicant_aliased.level_education,
                applicant_aliased.is_confirmed,
                applicant_aliased.gender,
                UserDB.email,
                UserDB.first_name,
                UserDB.last_name,
                UserDB.phone_number,
            )
            .join(UserDB, applicant_aliased.applicant_id == UserDB.user_id)
            .where(applicant_aliased.applicant_id == user_id)
        )
        result = await self._session.execute(sql)
        model = result.first()

        if model is None:
            raise UserNotFoundByID(user_id)
# ☺
        return ApplicantDTODAO(
            user=BaseUserDTODAO(
                last_name=model.last_name,
                first_name=model.last_name,
                phone_number=model.phone_number,
                email=model.email
            ),
            applicant_id=model.applicant_id,
            description_applicant=model.description_applicant,
            address=model.address,
            level_education=model.level_education,
            gender=model.gender,
            is_confirmed=model.is_confirmed,
        )

    @staticmethod
    def _error_parser(
            applicant: CreateApplicantDTODAO | UpdateApplicantDTODAO | BaseApplicantDTODAO,
            exc: IntegrityError
    ) -> BaseExceptions:
        database_column = exc.__cause__.__cause__.constraint_name
        if database_column == "users_email_key":
            return UserAlreadyExist(applicant.user.email)
