from datetime import datetime

from loguru import logger
from sqlalchemy import insert, select, literal, cast, update, or_
from sqlalchemy.exc import IntegrityError

from src.core.enums import ActorType, ChatType
from src.dto.db.applicant.applicant import BaseApplicantDTODAO
from src.dto.db.company.company import BaseCompanyDTODAO
from src.dto.db.response.response import BaseResponseDTODAO
from src.dto.db.resume.resume import BaseResumeDTODAO
from src.dto.db.user.user import BaseUserDTODAO
from src.dto.db.vacancy.vacancy import BaseVacancyDTODAO
from src.exceptions.infrascructure.response.response import (
    BaseResponseException,
    ResponseAlreadyMaked,
    ResponseNotFoundOnVacancyOrResume,
    ResponsePermissionError
)
from src.infrastructure.db.models import (
    ResponsesDB,
    MessageDB,
    CompanyDB,
    ApplicantDB,
    VacancyDB,
    ResumeDB
)
from src.infrastructure.db.models.chat import ChatDB
from src.infrastructure.enums_db import StatusRespondEnumDB, ActorTypeEnumDB
from src.interfaces.infrastructure.dao.response_dao import IResponsesDAO
from src.interfaces.infrastructure.sqlalchemy_dao import SqlAlchemyDAO


class ResponseDAO(SqlAlchemyDAO, IResponsesDAO):
    async def create_respond(self, respond: BaseResponseDTODAO) -> BaseResponseDTODAO:
        sql_respond = (
            insert(ResponsesDB)
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
            .returning(ResponsesDB.response_id)
        )

        try:
            res = await self._session.execute(sql_respond)

        except IntegrityError as exc:
            logger.bind(
                app_name=f"{ResponseDAO.__name__} in {self.create_respond.__name__}"
            ).error(f"WITH DATA {respond}\nMESSAGE: {exc}")
            raise self._error_parser(respond, exc)

        response_id = res.scalar_one_or_none()

        if response_id is None:
            raise ResponsePermissionError()

        sql_chat = (
            insert(ChatDB)
            .values(
                chat_type=ChatType.RESPONSE,
                response_id=response_id
            )
            .returning(ChatDB.chat_id)
        )
        try:
            res_chat = await self._session.execute(sql_chat)
        except IntegrityError as exc:
            logger.bind(
                app_name=f"{ResponseDAO.__name__} in {self.create_respond.__name__}"
            ).error(f"FAILED CHAT CREATE WITH RESPONSE_ID={response_id}\nMESSAGE: {exc}")
            raise self._error_parser(respond, exc)

        chat_id = res_chat.scalar_one()

        sql_message = (
            insert(MessageDB)
            .values(
                chat_id=chat_id,
                sender_id=respond.user_id,
                sender_type=respond.responder_type,
                message_text=respond.message
            )
        )
        try:
            await self._session.execute(sql_message)

        except IntegrityError as exc:
            logger.bind(
                app_name=f"{ResponseDAO.__name__} in {self.create_respond.__name__}"
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
                .select_from(ResponsesDB)
                .join(VacancyDB, VacancyDB.vacancy_id == ResponsesDB.vacancy_id)
                .join(CompanyDB, CompanyDB.company_id == VacancyDB.company_id)
                .join(ResumeDB, ResumeDB.resume_id == ResponsesDB.resume_id)
                .join(ApplicantDB, ApplicantDB.applicant_id == ResumeDB.applicant_id)
                .where(
                    ResponsesDB.response_id == response_id,
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

    async def change_status_respond(self, respond: BaseResponseDTODAO) -> BaseResponseDTODAO:
        sub_sql = (
            select(ResponsesDB.response_id)
            .join(VacancyDB, VacancyDB.vacancy_id == ResponsesDB.vacancy_id)
            .join(CompanyDB, CompanyDB.company_id == VacancyDB.company_id)
            .join(ResumeDB, ResumeDB.resume_id == ResponsesDB.resume_id)
            .join(ApplicantDB, ApplicantDB.applicant_id == ResumeDB.applicant_id)
            .where(
                or_(
                    CompanyDB.user_id == respond.user_id,
                    ApplicantDB.user_id == respond.user_id,
                ),
                ResponsesDB.responder_type != respond.responder_type,
                ResponsesDB.response_id == respond.response_id,
            )
            .scalar_subquery()
        )

        sql = (
            update(ResponsesDB)
            .where(
                ResponsesDB.response_id == sub_sql
            )
            .values(
                status=respond.status
            )
            .returning(ResponsesDB.response_id)
        )
        try:
            row = await self._session.execute(sql)

        except IntegrityError as exc:
            logger.bind(

                app_name=f"{ResponseDAO.__name__} in {self.change_status_respond.__name__}"
            ).error(f"WITH DATA {respond} IN CHANGE STATUS RESPOND\nMESSAGE: {exc}")
            raise self._error_parser(respond, exc)

        response_id = row.scalar_one_or_none()

        if response_id is None:
            raise ResponsePermissionError()

        sql_chat = (
            select(ChatDB.chat_id)
            .where(ChatDB.response_id == response_id)
        )
        chat_id = (await self._session.execute(sql_chat)).scalar_one()

        sql_message = (
            insert(MessageDB)
            .values(
                chat_id=chat_id,
                sender_type=respond.responder_type,
                message_text=respond.message,
                sender_id=respond.user_id
            )
        )
        try:
            await self._session.execute(sql_message)

        except IntegrityError as exc:
            logger.bind(
                app_name=f"{ResponseDAO.__name__} in {self.create_respond.__name__}"
            ).error(f"WITH DATA {respond} IN CREATE MESSAGE RESPOND IN CHANGE STATUS\nMESSAGE: {exc}")
            raise self._error_parser(respond, exc)

        if respond.responder_type == ActorType.COMPANY:
            sql = (
                select(ApplicantDB.email)
                .select_from(ResponsesDB)
                .join(ResumeDB, ResumeDB.resume_id == ResponsesDB.resume_id)
                .join(ApplicantDB, ApplicantDB.applicant_id == ResumeDB.applicant_id)
                .where(ResponsesDB.response_id == respond.response_id)
            )

        elif respond.responder_type == ActorType.APPLICANT:
            sql = (
                select(CompanyDB.email)
                .select_from(ResponsesDB)
                .join(VacancyDB, VacancyDB.vacancy_id == ResponsesDB.vacancy_id)
                .join(CompanyDB, CompanyDB.company_id == VacancyDB.company_id)
                .where(ResponsesDB.response_id == respond.response_id)
            )
        email = (await self._session.execute(sql)).scalar()

        if respond.responder_type == ActorType.APPLICANT:
            respond.vacancy = BaseVacancyDTODAO(
                company=BaseCompanyDTODAO(
                    user=BaseUserDTODAO(
                        email=email
                    )
                )
            )

        elif respond.responder_type == ActorType.COMPANY:
            respond.resume = BaseResumeDTODAO(
                applicant=BaseApplicantDTODAO(
                    user=BaseUserDTODAO(
                        email=email
                    )
                )
            )
        return respond

    @staticmethod
    def _error_parser(
            respond: BaseResponseDTODAO,
            exc: IntegrityError
    ) -> BaseResponseException:
        error_text = str(exc.orig)

        if "duplicate key value violates unique constraint" in error_text:
            return ResponseAlreadyMaked()

        elif "violates foreign key constraint" in error_text:
            return ResponseNotFoundOnVacancyOrResume()

        return BaseResponseException()
