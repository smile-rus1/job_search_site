from datetime import datetime

from loguru import logger
from sqlalchemy import insert, select, literal, cast
from sqlalchemy.exc import IntegrityError

from src.core.enums import ActorType
from src.dto.db.applicant.applicant import BaseApplicantDTODAO
from src.dto.db.company.company import BaseCompanyDTODAO
from src.dto.db.respond_on_vacancy.respond_on_vacancy import BaseRespondOnVacancyDTODAO
from src.dto.db.resume.resume import BaseResumeDTODAO
from src.dto.db.user.user import BaseUserDTODAO
from src.dto.db.vacancy.vacancy import BaseVacancyDTODAO
from src.exceptions.infrascructure.respond_on_vacancy.respond_on_vacancy import (
    BaseRespondOnVacancyException,
    ResponseAlreadyMaked,
    ResponseNotFoundOnVacancyOrResume,
    ResponsePermissionError
)
from src.infrastructure.db.models import (
    RespondOnVacancyDB,
    ResponseMessageDB,
    CompanyDB,
    ApplicantDB,
    VacancyDB,
    ResumeDB
)
from src.infrastructure.enums_db import StatusRespondEnumDB, ActorTypeEnumDB
from src.interfaces.infrastructure.dao.repond_on_vacancy_dao import IRespondOnVacancyDAO
from src.interfaces.infrastructure.sqlalchemy_dao import SqlAlchemyDAO


class RespondOnVacancyDAO(SqlAlchemyDAO, IRespondOnVacancyDAO):
    async def create_respond(self, respond: BaseRespondOnVacancyDTODAO) -> BaseRespondOnVacancyDTODAO:
        # sql_respond = (
        #     insert(RespondOnVacancyDB)
        #     .values(
        #         responder_type=respond.responder_type,
        #         status=respond.status,
        #         vacancy_id=respond.vacancy.vacancy_id,
        #         resume_id=respond.resume.resume_id
        #     ).returning(RespondOnVacancyDB.response_id)
        # )

        sql_respond = (
            insert(RespondOnVacancyDB)
            .from_select(
                ["responder_type", "status", "vacancy_id", "resume_id"],
                select(
                    cast(literal(respond.responder_type.value), ActorTypeEnumDB),
                    cast(literal(respond.status.value), StatusRespondEnumDB),
                    literal(respond.vacancy.vacancy_id),
                    literal(respond.resume.resume_id),
                ).select_from(
                    ResumeDB if respond.responder_type == ActorType.APPLICANT else VacancyDB
                ).where(
                    (
                            (ResumeDB.resume_id == respond.resume.resume_id) &
                            (ResumeDB.applicant_id == respond.user_id)
                    )
                    if respond.responder_type == ActorType.APPLICANT
                    else
                    (
                            (VacancyDB.vacancy_id == respond.vacancy.vacancy_id) &
                            (VacancyDB.company_id == respond.user_id)
                    )
                )
            )
            .returning(RespondOnVacancyDB.response_id)
        )

        try:
            res = await self._session.execute(sql_respond)

        except IntegrityError as exc:
            logger.bind(
                app_name=f"{RespondOnVacancyDAO.__name__} in {self.create_respond.__name__}"
            ).error(f"WITH DATA {respond}\nMESSAGE: {exc}")
            raise self._error_parser(respond, exc)

        response_id = res.scalar_one_or_none()

        if response_id is None:
            raise ResponsePermissionError()

        sql_message = (
            insert(ResponseMessageDB)
            .values(
                response_id=response_id,
                sender_type=respond.responder_type,
                message_text=respond.message,
            )
        )
        try:
            await self._session.execute(sql_message)

        except IntegrityError as exc:
            logger.bind(
                app_name=f"{RespondOnVacancyDAO.__name__} in {self.create_respond.__name__}"
            ).error(f"WITH DATA {respond} IN CREATE MESSAGE RESPOND\nMESSAGE: {exc}")
            raise self._error_parser(respond, exc)

        row = (
            await self._session.execute(
                select(
                    CompanyDB.email.label("company_email"),
                    CompanyDB.company_name.label("company_name"),
                    ApplicantDB.email.label("applicant_email"),
                    ApplicantDB.applicant_id.label("applicant_id"),
                    VacancyDB.title.label("vacancy_title")
                )
                .select_from(RespondOnVacancyDB)
                .join(VacancyDB, VacancyDB.vacancy_id == RespondOnVacancyDB.vacancy_id)
                .join(CompanyDB, CompanyDB.company_id == VacancyDB.company_id)
                .join(ResumeDB, ResumeDB.resume_id == RespondOnVacancyDB.resume_id)
                .join(ApplicantDB, ApplicantDB.applicant_id == ResumeDB.applicant_id)
                .where(
                    RespondOnVacancyDB.response_id == response_id,
                )
            )
        ).one()

        respond.response_id = response_id
        respond.response_date = datetime.now()
        respond.vacancy = BaseVacancyDTODAO(
            vacancy_id=respond.vacancy.vacancy_id,
            title=row.vacancy_title,
            company=BaseCompanyDTODAO(
                user=BaseUserDTODAO(
                    email=row.company_email
                ),
                company_name=row.company_name
            )
        )
        respond.resume = BaseResumeDTODAO(
            resume_id=respond.resume.resume_id,
            applicant=BaseApplicantDTODAO(
                user=BaseUserDTODAO(
                    email=row.applicant_email
                )
            )
        )

        return respond

    @staticmethod
    def _error_parser(
            respond: BaseRespondOnVacancyDTODAO,
            exc: IntegrityError
    ) -> BaseRespondOnVacancyException:
        error_text = str(exc.orig)

        if "duplicate key value violates unique constraint" in error_text:
            return ResponseAlreadyMaked()

        elif "violates foreign key constraint" in error_text:
            return ResponseNotFoundOnVacancyOrResume()

        return BaseRespondOnVacancyException()
