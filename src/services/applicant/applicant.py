from abc import ABC

from loguru import logger

from src.dto.db.applicant.applicant import CreateApplicantDTODAO, UpdateApplicantDTODAO
from src.dto.db.user.user import CreateUserDTODAO
from src.dto.services.applicant.applicant import CreateApplicantDTO, ApplicantOutDTO, UpdateApplicantDTO, ApplicantDTO
from src.dto.services.user.user import UserOutDTO, BaseUserDTO
from src.exceptions.infrascructure.user.user import UserAlreadyExist
from src.infrastructure.db.transaction_manager import TransactionManager
from src.interfaces.infrastructure.hasher import IHasher


class ApplicantUseCase(ABC):
    def __init__(self, tm: TransactionManager, hasher: IHasher):
        self._tm = tm
        self._hasher = hasher


class CreateApplicant(ApplicantUseCase):
    async def __call__(self, applicant_dto: CreateApplicantDTO) -> ApplicantOutDTO:
        hashed_password = self._hasher.hash(applicant_dto.user.password)
        applicant = CreateApplicantDTODAO(
            user=CreateUserDTODAO(
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
            logger.error(f"USER ALREADY EXISTS WITH THIS EMAIL {applicant_dto.user.email}")
            await self._tm.rollback()
            raise UserAlreadyExist(email=applicant_dto.user.email)

        return ApplicantOutDTO(
            user=UserOutDTO(
                user_id=applicant_created.user.user_id,
                last_name=applicant_dto.user.last_name,
                first_name=applicant_dto.user.first_name,
                email=applicant_dto.user.email
            )
        )


class UpdateApplicant(ApplicantUseCase):
    async def __call__(self, applicant_data: UpdateApplicantDTO) -> None:
        applicant = UpdateApplicantDTODAO(**applicant_data.__dict__)

        try:
            await self._tm.applicant_dao.update_applicant(applicant)
            await self._tm.commit()

        except UserAlreadyExist:
            logger.error(f"EXCEPTION IN UPDATE APPLICANT WITH EMAIL {applicant_data.email}")
            await self._tm.rollback()
            raise UserAlreadyExist(applicant_data.email)


class GetApplicantByID(ApplicantUseCase):
    async def __call__(self, applicant_id: int) -> ApplicantDTO:
        applicant_data = await self._tm.applicant_dao.get_applicant_by_id(applicant_id)
        return ApplicantDTO(
            user=BaseUserDTO(
                last_name=applicant_data.user.last_name,
                first_name=applicant_data.user.first_name,
                email=applicant_data.user.email,
            ),
            applicant_id=applicant_data.applicant_id,
            description_applicant=applicant_data.description_applicant,
            address=applicant_data.address,
            gender=applicant_data.gender,
            is_confirmed=applicant_data.is_confirmed,
            level_education=applicant_data.level_education
        )


class ApplicantService:
    def __init__(self, tm: TransactionManager, hasher: IHasher):
        self._tm = tm
        self._hasher = hasher

    async def create_applicant(self, applicant_dto: CreateApplicantDTO) -> ApplicantOutDTO:
        return await CreateApplicant(tm=self._tm, hasher=self._hasher)(applicant_dto)

    async def update_applicant(self, applicant_dto: UpdateApplicantDTO) -> None:
        return await UpdateApplicant(tm=self._tm, hasher=self._hasher)(applicant_dto)

    async def get_applicant(self, applicant_id: int) -> ApplicantDTO:
        return await GetApplicantByID(tm=self._tm, hasher=self._hasher)(applicant_id)
