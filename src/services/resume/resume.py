from abc import ABC

from loguru import logger

from src.dto.db.resume.resume import CreateResumeDTODAO, UpdateResumeDTODAO, SearchDTODAO
from src.dto.services.applicant.applicant import ApplicantDTO
from src.dto.services.resume.resume import (
    CreateResumeDTO,
    ResumeOutDTO,
    UpdateResumeDTO,
    ResumeDTO,
    SearchResumeDTO,
    ResumeSearchOutDTO
)
from src.dto.services.user.user import BaseUserDTO
from src.dto.services.work_exprerience.work_experience import WorkExperienceDTO
from src.exceptions.infrascructure.resume.resume import ResumeException
from src.interfaces.services.transaction_manager import IBaseTransactionManager


class ResumeUseCase(ABC):
    def __init__(self, tm: IBaseTransactionManager):
        self._tm = tm


class CreateResume(ResumeUseCase):
    async def __call__(self, resume_dto: CreateResumeDTO) -> ResumeOutDTO:
        resume = CreateResumeDTODAO(**resume_dto.__dict__)
        try:
            resume_created = await self._tm.resume_dao.create_resume(resume)
            await self._tm.commit()

        except ResumeException:
            logger.error(f"EXCEPTION HAPPEN IN CREATE RESUME with dto {resume_dto}")
            await self._tm.rollback()
            raise ResumeException()

        return ResumeOutDTO(
            **resume_created.__dict__
        )


class UpdateResume(ResumeUseCase):
    async def __call__(self, resume_dto: UpdateResumeDTO) -> None:
        resume = UpdateResumeDTODAO(**resume_dto.__dict__)

        try:
            await self._tm.resume_dao.update_resume(resume)
            await self._tm.commit()

        except ResumeException:
            logger.error(f"EXCEPTION HAPPEN IN UPDATE RESUME with dto {resume_dto}")
            await self._tm.rollback()
            raise ResumeException()


class GetResumeByID(ResumeUseCase):
    async def __call__(self, resume_id: int) -> ResumeDTO:
        resume = await self._tm.resume_dao.get_resume_by_id(resume_id)
        return ResumeDTO(
            resume_id=resume.resume_id,
            name_resume=resume.name_resume,
            profession=resume.profession,
            key_skills=resume.key_skills,
            salary_min=resume.salary_min,
            salary_max=resume.salary_max,
            salary_currency=resume.salary_currency,
            location=resume.location,
            type_of_employment=resume.type_of_employment,
            applicant=ApplicantDTO(
                applicant_id=resume.applicant.applicant_id,
                gender=resume.applicant.gender,
                description_applicant=resume.applicant.description_applicant,
                address=resume.applicant.address,
                is_confirmed=resume.applicant.is_confirmed,
                level_education=resume.applicant.level_education,
                user=BaseUserDTO(
                    email=resume.applicant.user.email,
                    first_name=resume.applicant.user.first_name,
                    last_name=resume.applicant.user.last_name,
                    phone_number=resume.applicant.user.phone_number,
                    image_url=resume.applicant.user.image_url,
                )
            ),
            work_experience=[
                WorkExperienceDTO(
                    work_experience_id=we.work_experience_id,
                    resume_id=we.resume_id,
                    company_name=we.company_name,
                    start_date=we.start_date,
                    end_date=we.end_date,
                    description_work=we.description_work,
                )
                for we in resume.work_experience
            ]
        )


class SearchResumes(ResumeUseCase):
    async def __call__(self, search_dto: SearchResumeDTO) -> list[ResumeSearchOutDTO]:
        search_dto_dao = SearchDTODAO(**search_dto.__dict__)
        resumes = await self._tm.resume_dao.search_resumes(search_dto_dao)
        dtos: list[ResumeSearchOutDTO] = []

        for r in resumes:
            applicant_dto = ApplicantDTO(
                applicant_id=r.applicant.applicant_id,
                address=r.applicant.address,
                level_education=r.applicant.level_education,
                date_born=r.applicant.date_born,
                gender=r.applicant.gender,
                user=BaseUserDTO(
                    email=r.applicant.user.email,
                    first_name=r.applicant.user.first_name,
                    last_name=r.applicant.user.last_name,
                    phone_number=r.applicant.user.phone_number,
                    image_url=r.applicant.user.image_url
                )
            )

            work_exps = [
                WorkExperienceDTO(
                    resume_id=w.resume_id,
                    work_experience_id=w.work_experience_id,
                    company_name=w.company_name,
                    start_date=w.start_date,
                    end_date=w.end_date,
                    description_work=w.description_work
                )
                for w in r.work_experiences
            ]

            dtos.append(
                ResumeSearchOutDTO(
                    resume_id=r.resume_id,
                    name_resume=r.name_resume,
                    profession=r.profession,
                    key_skills=r.key_skills,
                    salary_min=r.salary_min,
                    salary_max=r.salary_max,
                    salary_currency=r.salary_currency,
                    location=r.location,
                    type_of_employment=r.type_of_employment,
                    total_months=r.total_months,
                    applicant=applicant_dto,
                    work_experiences=work_exps
                )
            )

        return dtos


class DeleteResume(ResumeUseCase):
    async def __call__(self, resume_id: int, applicant_id: int) -> None:
        await self._tm.resume_dao.delete_resume(resume_id, applicant_id)
        await self._tm.commit()


class ResumeService:
    def __init__(self, tm: IBaseTransactionManager):
        self._tm = tm

    async def create_resume(self, resume_dto: CreateResumeDTO) -> ResumeOutDTO:
        return await CreateResume(self._tm)(resume_dto)

    async def update_resume(self, resume_dto: UpdateResumeDTO) -> None:
        await UpdateResume(self._tm)(resume_dto)

    async def get_resume_by_id(self, resume_id: int) -> ResumeDTO:
        return await GetResumeByID(self._tm)(resume_id)

    async def search_resumes(self, search_dto: SearchResumeDTO) -> list[ResumeSearchOutDTO]:
        return await SearchResumes(self._tm)(search_dto)

    async def delete_resume(self, resume_id: int, applicant_id: int) -> None:
        await DeleteResume(self._tm)(resume_id, applicant_id)
