from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

from src.dto.db.applicant.applicant import ApplicantOutDTODAO, CreateApplicantDTODAO
from src.dto.db.user.user import UserOutDTODAO
from src.exceptions.base import BaseExceptions
from src.exceptions.infrascructure.user.user import UserAlreadyExist
from src.infrastructure.db.dao.base_dao import BaseDAO
from src.infrastructure.db.models import ApplicantDB, UserDB


class ApplicantDAO(BaseDAO):
    async def create(self, applicant: CreateApplicantDTODAO) -> ApplicantOutDTODAO:
        user_sql = (
            insert(UserDB.__table__)
            .values(
                email=applicant.user.email,
                password=applicant.user.password,
                first_name=applicant.user.first_name,
                last_name=applicant.user.last_name,
                phone_number=applicant.user.phone_number,
                image_url=applicant.user.image_url,
                type="applicant"
            )
            .returning(UserDB.user_id)
        )

        try:
            result = await self._session.execute(user_sql)

        except IntegrityError as exc:
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
                is_confirmed=False
            )
            .returning(ApplicantDB.applicant_id)
        )
        try:
            result = await self._session.execute(applicant_sql)
        except IntegrityError as exc:
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

    @staticmethod
    def _error_parser(applicant: CreateApplicantDTODAO, exc: IntegrityError) -> BaseExceptions:
        database_column = exc.__cause__.__cause__.constraint_name
        if database_column == "users_email_key":
            return UserAlreadyExist(applicant.user.email)
