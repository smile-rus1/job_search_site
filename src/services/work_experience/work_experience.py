from abc import ABC

from loguru import logger

from src.dto.db.work_experience.work_experience import BaseWorkExperienceDTODAO
from src.dto.services.work_exprerience.work_experience import (
    CreateWorkExperienceDTO,
    WorkExperienceDTO,
    UpdateWorkExperienceDTO
)
from src.exceptions.infrascructure.work_experiences.work_experiences import WorkExperiences
from src.interfaces.services.transaction_manager import IBaseTransactionManager


class WorkExperienceUseCase(ABC):
    def __init__(self, tm: IBaseTransactionManager):
        self._tm = tm


class CreateWorkExperience(WorkExperienceUseCase):
    async def __call__(self, work_experience_dto: CreateWorkExperienceDTO) -> WorkExperienceDTO:
        work_experience = BaseWorkExperienceDTODAO(
            resume_id=work_experience_dto.resume_id,
            company_name=work_experience_dto.company_name,
            start_date=work_experience_dto.start_date,
            end_date=work_experience_dto.end_date,
            description_work=work_experience_dto.description_work,

        )

        try:
            result = await self._tm.work_experience_dao.create_work_experience(work_experience)
            await self._tm.commit()

        except WorkExperiences:
            logger.bind(
                app_name=f"{CreateWorkExperience.__name__}"
            ).error(f"WITH DATA {work_experience_dto}")

            await self._tm.rollback()
            raise WorkExperiences()

        return WorkExperienceDTO(**result.__dict__)


class UpdateWorkExperience(WorkExperienceUseCase):
    async def __call__(self, work_experience_dto: UpdateWorkExperienceDTO) -> None:
        work_experience = BaseWorkExperienceDTODAO(
            resume_id=work_experience_dto.resume_id,
            work_experience_id=work_experience_dto.work_experience_id,
            company_name=work_experience_dto.company_name,
            start_date=work_experience_dto.start_date,
            end_date=work_experience_dto.end_date,
            description_work=work_experience_dto.description_work,
        )

        try:
            await self._tm.work_experience_dao.update_work_experience(work_experience)
            await self._tm.commit()

        except WorkExperiences:
            logger.bind(
                app_name=f"{UpdateWorkExperience.__name__}"
            ).error(f"WITH DATA {work_experience_dto}")

            await self._tm.rollback()
            raise WorkExperiences()


class GetWorkExperienceByID(WorkExperienceUseCase):
    async def __call__(self, work_experience_id: int) -> WorkExperienceDTO:
        res = await self._tm.work_experience_dao.get_work_experience_by_id(work_experience_id)

        return WorkExperienceDTO(**res.__dict__)


class DeleteWorkExperience(WorkExperienceUseCase):
    async def __call__(self, applicant_id: int, resume_id: int, work_experience_id: int):
        await self._tm.work_experience_dao.delete_work_experience(applicant_id, resume_id, work_experience_id)
        await self._tm.commit()


class WorkExperienceService:
    def __init__(self, tm: IBaseTransactionManager):
        self._tm = tm

    async def create_work_experience(self, work_experience_dto: CreateWorkExperienceDTO) -> WorkExperienceDTO:
        return await CreateWorkExperience(self._tm)(work_experience_dto)

    async def update_work_experience(self, work_experience_dto: UpdateWorkExperienceDTO) -> None:
        return await UpdateWorkExperience(self._tm)(work_experience_dto)

    async def delete_work_experience(self, applicant_id: int, resume_id: int, work_experience_id: int) -> None:
        await DeleteWorkExperience(self._tm)(applicant_id, resume_id, work_experience_id)

    async def get_work_experience_by_id(self, work_experience_id: int) -> WorkExperienceDTO:
        return await GetWorkExperienceByID(self._tm)(work_experience_id)
