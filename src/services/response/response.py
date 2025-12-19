from abc import ABC

from loguru import logger

from src.utils import utils

from src.core.enums import StatusRespond, ActorType
from src.dto.db.response.response import BaseResponseDTODAO
from src.dto.db.resume.resume import BaseResumeDTODAO
from src.dto.db.vacancy.vacancy import BaseVacancyDTODAO
from src.dto.services.response.response import (
    CreateResponseDTO,
    ChangeStatusResponseDTO
)
from src.exceptions.infrascructure.response.response import BaseResponseException
from src.interfaces.infrastructure.notifications import AbstractNotifications
from src.interfaces.services.transaction_manager import IBaseTransactionManager


class RespondOnVacancyUseCase(ABC):
    def __init__(self, tm: IBaseTransactionManager):
        self._tm = tm


class CreateResponseByApplicant(RespondOnVacancyUseCase):
    async def __call__(
            self,
            respond_dto: CreateResponseDTO,
            notifications: AbstractNotifications
    ):
        respond = BaseResponseDTODAO(
            user_id=respond_dto.user_id,
            vacancy=BaseVacancyDTODAO(
                company=None,
                vacancy_id=respond_dto.vacancy_id
            ),
            resume=BaseResumeDTODAO(
                applicant=None,
                resume_id=respond_dto.resume_id
            ),
            responder_type=respond_dto.responder_type,
            status=StatusRespond.SENT,
            message=respond_dto.message
        )

        try:
            respond_out = await self._tm.respond_dao.create_respond(respond)
            await self._tm.commit()

        except BaseResponseException as exc:
            logger.bind(
                app_name=f"{CreateResponseByApplicant.__name__}"
            ).error(f"WITH DATA {respond_dto}")
            await self._tm.rollback()
            raise exc

        body = ""
        if respond_dto.message is not None:
            body = (
                f"Сообщение от кандидата:"
                f"«{respond_dto.message}»"
            )
        body += f"Ссылка на просмотр его резюме: {utils.create_applicant_resume_link(respond_dto.resume_id)}"

        data_notification = {
            "subject": f"Кандидат откликнулся на вакансию",
            "body": body
        }

        logger.bind(
            app_name=f"{CreateResponseByApplicant.__name__}"
        ).info(f"DATA {data_notification}")

        notifications.send(
            destination=respond_out.vacancy.company.user.email,
            template="send_respond_notification",
            data=data_notification
        )


class CreateResponseByCompany(RespondOnVacancyUseCase):
    async def __call__(
            self,
            respond_dto: CreateResponseDTO,
            notifications: AbstractNotifications
    ):
        respond = BaseResponseDTODAO(
            user_id=respond_dto.user_id,
            vacancy=BaseVacancyDTODAO(
                company=None,
                vacancy_id=respond_dto.vacancy_id
            ),
            resume=BaseResumeDTODAO(
                applicant=None,
                resume_id=respond_dto.resume_id
            ),
            responder_type=respond_dto.responder_type,
            status=StatusRespond.SENT,
            message=respond_dto.message
        )

        try:
            respond_out = await self._tm.respond_dao.create_respond(respond)
            await self._tm.commit()

        except BaseResponseException as exc:
            logger.bind(
                app_name=f"{CreateResponseByApplicant.__name__}"
            ).error(f"WITH DATA {respond_dto}")
            await self._tm.rollback()
            raise exc

        body = ""
        if respond_dto.message is not None:
            body = (
                f"Сообщение от компании:\n"
                f"«{respond_dto.message}»\n"
            )
        body += (
            f"Вакансия {respond_out.vacancy.title}\n"
            f"Ссылка на вакансию: {utils.create_company_vacancy_link(respond_dto.vacancy_id)}\n"
        )

        data_notification = {
            "subject": f"С вами хотят связаться из компании «{respond_out.vacancy.company.company_name}»",
            "body": body
        }

        logger.bind(
            app_name=f"{CreateResponseByCompany.__name__}"
        ).info(f"DATA {data_notification}")

        notifications.send(
            destination=respond_out.vacancy.company.user.email,
            template="send_respond_notification",
            data=data_notification
        )


class ChangeStatusResponse(RespondOnVacancyUseCase):
    async def __call__(
            self,
            respond_dto: ChangeStatusResponseDTO,
            notifications: AbstractNotifications
    ) -> StatusRespond:
        respond = BaseResponseDTODAO(
            user_id=respond_dto.user_id,
            response_id=respond_dto.response_id,
            vacancy=BaseVacancyDTODAO(
                company=None
            ),
            resume=BaseResumeDTODAO(
                applicant=None,
            ),
            responder_type=respond_dto.responder_type,
            status=respond_dto.status,
            message=respond_dto.message
        )
        try:
            res = await self._tm.respond_dao.change_status_respond(respond)
            await self._tm.commit()

        except BaseResponseException as exc:
            logger.bind(
                app_name=f"{ChangeStatusResponse.__name__}"
            ).error(f"WITH DATA {respond_dto}")
            await self._tm.rollback()
            raise exc

        logger.bind(
            app_name=f"{ChangeStatusResponse.__name__}"
        ).info(f"Send email to {res}")

        if res.responder_type == ActorType.APPLICANT:
            destination = res.resume.applicant.user.email
            body = (
                "Вам пришёл отклик от кандидата.\n"
                if respond_dto.message is None else
                "Вам пришёл отклик от кандидата.\n"
                f"«{respond_dto.message}»\n"
            )
            body += f"Ссылка на чат"  # тут мб сделать ссылку на чат
            data_notification = {
                "subject": f"С Вами хотят связаться",
                "body": body
            }

        elif res.responder_type == ActorType.COMPANY:  # ???? тут что-то вот не так, почему-то данные пустые ????
            destination = res.vacancy.company.user.email
            body = (
                "Вам пришло сообщение от компании.\n"
                if respond_dto.message is None else
                "Вам пришло сообщение от компании.\n"
                f"«{respond_dto.message}»\n"
            )
            body += f"Ссылка на чат"  # тут мб сделать ссылку на чат
            data_notification = {
                "subject": f"С Вами хотят связаться",
                "body": body
            }
        else:
            destination = ""
            data_notification = {}

        notifications.send(
            destination=destination,
            template="send_message_about_change_status",
            data=data_notification
        )

        return respond_dto.status


class ResponseService:
    def __init__(
            self,
            tm: IBaseTransactionManager,
            notifications: AbstractNotifications,
    ):
        self._tm = tm
        self._notifications = notifications

    async def create_response_by_applicant(self, respond_dto: CreateResponseDTO):
        return await CreateResponseByApplicant(self._tm)(respond_dto, self._notifications)

    async def create_response_by_company(self, respond_dto: CreateResponseDTO):
        return await CreateResponseByCompany(self._tm)(respond_dto, self._notifications)

    async def change_status_response(self, respond_dto: ChangeStatusResponseDTO) -> StatusRespond:
        return await ChangeStatusResponse(self._tm)(respond_dto, self._notifications)
