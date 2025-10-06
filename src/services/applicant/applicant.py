import json
import uuid
from abc import ABC

from loguru import logger

from src.core.config_reader import config
from src.dto.db.applicant.applicant import BaseApplicantDTODAO
from src.dto.db.user.user import BaseUserDTODAO
from src.dto.services.applicant.applicant import (
    CreateApplicantDTO,
    ApplicantOutDTO,
    UpdateApplicantDTO,
    ApplicantDTO
)
from src.dto.services.user.user import UserOutDTO, BaseUserDTO
from src.exceptions.infrascructure.user.user import UserAlreadyExist
from src.infrastructure.enums import TypeUser
from src.interfaces.infrastructure.hasher import IHasher
from src.infrastructure.celery import email_tasks

import src.utils.create_confirm_link as create_confirm_link
from src.interfaces.services.transaction_manager import IBaseTransactionManager


class ApplicantUseCase(ABC):
    def __init__(self, tm: IBaseTransactionManager, hasher: IHasher):
        self._tm = tm
        self._hasher = hasher


class CreateApplicant(ApplicantUseCase):
    async def __call__(self, applicant_dto: CreateApplicantDTO) -> ApplicantOutDTO:
        hashed_password = self._hasher.hash(applicant_dto.user.password)
        applicant = BaseApplicantDTODAO(
            user=BaseUserDTODAO(
                email=applicant_dto.user.email,
                password=hashed_password,
                last_name=applicant_dto.user.last_name,
                first_name=applicant_dto.user.first_name,
                image_url=applicant_dto.user.image_url,
                phone_number=applicant_dto.user.phone_number
            ),
            description_applicant=applicant_dto.description_applicant,
            address=applicant_dto.address,
            level_education=applicant_dto.level_education,
            gender=applicant_dto.gender,
            date_born=applicant_dto.date_born
        )

        try:
            applicant_created = await self._tm.applicant_dao.create_applicant(applicant)
            await self._tm.commit()

        except UserAlreadyExist:
            logger.bind(
                app_name=f"{CreateApplicant.__name__}"
            ).error(f"WITH DATA {applicant_dto}")
            await self._tm.rollback()
            raise UserAlreadyExist(email=applicant_dto.user.email)

        token = uuid.uuid4().hex
        redis_key = config.auth.user_confirm_key.format(token=token)

        confirm_link = create_confirm_link.create_confirm_link(token)

        await self._tm.redis_db.set(
            key=redis_key,
            value=json.dumps({"user_id": applicant_created.user.user_id, "type": TypeUser.APPLICANT.value}),
            expire=300
        )

        logger.bind(
            app_name=f"{CreateApplicant.__name__}"
        ).info(f"LINK TO CONFIRM {confirm_link}")
        email_tasks.send_confirmation_email_task.delay(
            to_email=applicant_created.user.email,
            confirm_link=confirm_link
        )

        return ApplicantOutDTO(
            user=UserOutDTO(
                user_id=applicant_created.user.user_id,
                last_name=applicant_dto.user.last_name,
                first_name=applicant_dto.user.first_name,
                email=applicant_dto.user.email
            )
        )


class UpdateApplicant(ApplicantUseCase):
    async def __call__(self, applicant_dto: UpdateApplicantDTO) -> None:
        applicant = BaseApplicantDTODAO(
            user=BaseUserDTODAO(
                user_id=applicant_dto.user_id,
                email=applicant_dto.email,
            ),
            gender=applicant_dto.gender,
            description_applicant=applicant_dto.description_applicant,
            address=applicant_dto.address,
            level_education=applicant_dto.level_education,
            date_born=applicant_dto.date_born,
        )

        try:
            await self._tm.applicant_dao.update_applicant(applicant)
            await self._tm.commit()

        except UserAlreadyExist:
            logger.bind(
                app_name=f"{CreateApplicant.__name__}"
            ).error(f"WITH DATA {applicant_dto}")
            await self._tm.rollback()
            raise UserAlreadyExist(applicant_dto.email)


class GetApplicantByID(ApplicantUseCase):
    async def __call__(self, applicant_id: int) -> ApplicantDTO:
        applicant_data = await self._tm.applicant_dao.get_applicant_by_id(applicant_id)
        return ApplicantDTO(
            user=BaseUserDTO(
                last_name=applicant_data.user.last_name,
                first_name=applicant_data.user.first_name,
                email=applicant_data.user.email,
            ),
            applicant_id=applicant_data.user.user_id,
            description_applicant=applicant_data.description_applicant,
            address=applicant_data.address,
            gender=applicant_data.gender,
            is_confirmed=applicant_data.user.is_confirmed,
            level_education=applicant_data.level_education
        )


class ApplicantService:
    def __init__(self, tm: IBaseTransactionManager, hasher: IHasher):
        self._tm = tm
        self._hasher = hasher

    async def create_applicant(self, applicant_dto: CreateApplicantDTO) -> ApplicantOutDTO:
        return await CreateApplicant(tm=self._tm, hasher=self._hasher)(applicant_dto)

    async def update_applicant(self, applicant_dto: UpdateApplicantDTO) -> None:
        return await UpdateApplicant(tm=self._tm, hasher=self._hasher)(applicant_dto)

    async def get_applicant(self, applicant_id: int) -> ApplicantDTO:
        return await GetApplicantByID(tm=self._tm, hasher=self._hasher)(applicant_id)
