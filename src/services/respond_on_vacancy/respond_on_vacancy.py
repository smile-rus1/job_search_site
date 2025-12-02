from abc import ABC

from loguru import logger

from src.utils import utils

from src.core.enums import StatusRespond
from src.dto.db.respond_on_vacancy.respond_on_vacancy import BaseRespondOnVacancyDTODAO
from src.dto.db.resume.resume import BaseResumeDTODAO
from src.dto.db.vacancy.vacancy import BaseVacancyDTODAO
from src.dto.services.respond_on_vacancy.respond_on_vacancy import (
    CreateRespondOnVacancyDTO,
    ChangeStatusRespondDTO
)
from src.exceptions.infrascructure.respond_on_vacancy.respond_on_vacancy import BaseRespondOnVacancyException
from src.interfaces.infrastructure.notifications import AbstractNotifications
from src.interfaces.services.transaction_manager import IBaseTransactionManager


class RespondOnVacancyUseCase(ABC):
    def __init__(self, tm: IBaseTransactionManager):
        self._tm = tm


class CreateRespondOnVacancyByApplicant(RespondOnVacancyUseCase):
    async def __call__(
            self,
            respond_dto: CreateRespondOnVacancyDTO,
            notifications: AbstractNotifications
    ):
        respond = BaseRespondOnVacancyDTODAO(
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

        except BaseRespondOnVacancyException as exc:
            logger.bind(
                app_name=f"{CreateRespondOnVacancyByApplicant.__name__}"
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
            app_name=f"{CreateRespondOnVacancyByApplicant.__name__}"
        ).info(f"DATA {data_notification}")

        notifications.send(
            destination=respond_out.vacancy.company.user.email,
            template="send_respond_notification",
            data=data_notification
        )


class CreateRespondOnVacancyByCompany(RespondOnVacancyUseCase):
    async def __call__(
            self,
            respond_dto: CreateRespondOnVacancyDTO,
            notifications: AbstractNotifications
    ):
        respond = BaseRespondOnVacancyDTODAO(
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

        except BaseRespondOnVacancyException as exc:
            logger.bind(
                app_name=f"{CreateRespondOnVacancyByApplicant.__name__}"
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
            app_name=f"{CreateRespondOnVacancyByCompany.__name__}"
        ).info(f"DATA {data_notification}")

        notifications.send(
            destination=respond_out.vacancy.company.user.email,
            template="send_respond_notification",
            data=data_notification
        )


class ChangeStatusRespond(RespondOnVacancyUseCase):
    async def __call__(
            self,
            respond_dto: ChangeStatusRespondDTO,
            notifications: AbstractNotifications
    ) -> StatusRespond:
        respond = BaseRespondOnVacancyDTODAO(
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
            await self._tm.respond_dao.change_status_respond(respond)
            await self._tm.commit()

        except BaseRespondOnVacancyException as exc:
            logger.bind(
                app_name=f"{ChangeStatusRespond.__name__}"
            ).error(f"WITH DATA {respond_dto}")
            await self._tm.rollback()
            raise exc

        return respond_dto.status


class RespondOnVacancyService:
    def __init__(
            self,
            tm: IBaseTransactionManager,
            notifications: AbstractNotifications,
    ):
        self._tm = tm
        self._notifications = notifications

    async def create_respond_by_applicant(self, respond_dto: CreateRespondOnVacancyDTO):
        return await CreateRespondOnVacancyByApplicant(self._tm)(respond_dto, self._notifications)

    async def create_respond_by_company(self, respond_dto: CreateRespondOnVacancyDTO):
        return await CreateRespondOnVacancyByCompany(self._tm)(respond_dto, self._notifications)

    async def change_status_respond(self, respond_dto: ChangeStatusRespondDTO) -> StatusRespond:
        return await ChangeStatusRespond(self._tm)(respond_dto, self._notifications)
