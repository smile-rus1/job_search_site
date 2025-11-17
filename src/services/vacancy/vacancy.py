from abc import ABC

from loguru import logger

from src.dto.db.company.company import BaseCompanyDTODAO
from src.dto.db.user.user import BaseUserDTODAO
from src.dto.db.vacancy.vacancy import (
    BaseVacancyDTODAO,
    BaseVacancyTypeDTODAO,
    BaseVacancyTypePriceDTODAO
)
from src.dto.services.company.company import BaseCompanyDTO
from src.dto.services.user.user import BaseUserDTO
from src.dto.services.vacancy.vacancy import (
    CreateVacancyDTO,
    VacancyOutDTO,
    UpdateVacancyDTO,
    BaseVacancyDTO
)
from src.dto.services.vacancy.vacancy_access import BaseVacancyAccessDTO
from src.dto.services.vacancy.vacancy_type import BaseVacancyTypeDTO
from src.exceptions.infrascructure.vacancy.vacancy import (
    BaseVacancyException,
    VacancyNotFoundByID,
    NotUpdatedTimeVacancy
)
from src.interfaces.services.transaction_manager import IBaseTransactionManager


class VacancyUseCase(ABC):
    def __init__(self, tm: IBaseTransactionManager):
        self._tm = tm


class CreateVacancy(VacancyUseCase):
    async def __call__(self, vacancy_dto: CreateVacancyDTO) -> VacancyOutDTO:
        vacancy = BaseVacancyDTODAO(
            company=BaseCompanyDTODAO(
                user=BaseUserDTODAO(
                    user_id=vacancy_dto.company.user.user_id
                )
            ),
            vacancy_type=BaseVacancyTypeDTODAO(
                name=vacancy_dto.vacancy_type.name,
                vacancy_type_price=BaseVacancyTypePriceDTODAO(
                    duration=vacancy_dto.vacancy_type.duration
                )
            ),
            title=vacancy_dto.title,
            description=vacancy_dto.description,
            location=vacancy_dto.location,
            key_skills=vacancy_dto.key_skills,
            profession=vacancy_dto.profession,
            salary_min=vacancy_dto.salary_min,
            salary_max=vacancy_dto.salary_max,
            salary_currency=vacancy_dto.salary_currency,
            type_of_employment=vacancy_dto.type_of_employment,
            type_work_schedule=vacancy_dto.type_work_schedule,
            experience_start=vacancy_dto.experience_start,
            experience_end=vacancy_dto.experience_end,
        )
        try:
            res = await self._tm.vacancy_dao.create_vacancy(vacancy)
            await self._tm.commit()

        except BaseVacancyException as exc:
            logger.bind(
                app_name=f"{CreateVacancy.__name__}"
            ).error(f"WITH DATA {vacancy_dto}\nEXCEPTION {exc.message()}")
            await self._tm.rollback()
            raise exc

        return VacancyOutDTO(
            vacancy_id=res.vacancy_id,
            title=res.title,
            profession=res.profession,
            description=res.description,
            location=res.location,
            key_skills=res.key_skills,
            salary_min=res.salary_min,
            salary_max=res.salary_max,
            salary_currency=res.salary_currency,
            type_of_employment=res.type_of_employment,
            type_work_schedule=res.type_work_schedule,
            created_at=res.created_at,
            is_published=res.is_published,
            experience_start=res.experience_start,
            experience_end=res.experience_end
        )


class UpdateVacancy(VacancyUseCase):
    async def __call__(self, vacancy_dto: UpdateVacancyDTO) -> None:
        vacancy = BaseVacancyDTODAO(
            vacancy_id=vacancy_dto.vacancy_id,
            company=BaseCompanyDTODAO(
                user=BaseUserDTODAO(
                    user_id=vacancy_dto.company.user.user_id
                )
            ),
            title=vacancy_dto.title,
            description=vacancy_dto.description,
            location=vacancy_dto.location,
            key_skills=vacancy_dto.key_skills,
            profession=vacancy_dto.profession,
            salary_min=vacancy_dto.salary_min,
            salary_max=vacancy_dto.salary_max,
            salary_currency=vacancy_dto.salary_currency,
            type_of_employment=vacancy_dto.type_of_employment,
            type_work_schedule=vacancy_dto.type_work_schedule,
            experience_start=vacancy_dto.experience_start,
            experience_end=vacancy_dto.experience_end,
        )

        try:
            await self._tm.vacancy_dao.update_vacancy(vacancy)
            await self._tm.commit()

        except BaseVacancyException as exc:
            logger.bind(
                app_name=f"{UpdateVacancy.__name__}"
            ).error(f"WITH DATA {vacancy_dto}\nEXCEPTION {exc.message()}")
            await self._tm.rollback()
            raise exc


class GetVacancyByID(VacancyUseCase):
    async def __call__(self, vacancy_id) -> BaseVacancyDTO:
        try:
            result = await self._tm.vacancy_dao.get_vacancy_by_id(vacancy_id)

        except VacancyNotFoundByID as exc:
            logger.bind(
                app_name=f"{GetVacancyByID.__name__}"
            ).error(f"WITH ID {vacancy_id}\nEXCEPTION {exc.message()}")
            raise exc
        return BaseVacancyDTO(
            vacancy_id=result.vacancy_id,
            title=result.title,
            description=result.description,
            location=result.location,
            key_skills=result.key_skills,
            profession=result.profession,
            salary_min=result.salary_min,
            salary_max=result.salary_max,
            salary_currency=result.salary_currency,
            type_of_employment=result.type_of_employment,
            type_work_schedule=result.type_work_schedule,
            updated_at=result.updated_at,
            is_published=result.is_published,
            is_confirmed=result.is_confirmed,
            experience_start=result.experience_start,
            experience_end=result.experience_end,
            vacancy_type=BaseVacancyTypeDTO(
                name=result.vacancy_type.name
            ),
            vacancy_access=BaseVacancyAccessDTO(
                duration=result.vacancy_access.duration,
                start_date=result.vacancy_access.start_date,
                end_date=result.vacancy_access.end_date,
                is_active=result.vacancy_access.is_active
            ),
            company=BaseCompanyDTO(
                company_name=result.company.company_name,
                address=result.company.address,
                company_is_confirmed=result.company.company_is_confirmed,
                user=BaseUserDTO(
                    user_id=result.company.user.user_id,
                    email=result.company.user.email,
                    image_url=result.company.user.image_url
                )
            )
        )


class DeleteVacancy(VacancyUseCase):
    async def __call__(self, vacancy_id: int, company_id: int) -> None:
        await self._tm.vacancy_dao.delete_vacancy(vacancy_id, company_id)
        await self._tm.commit()


class ChangeVisibilityVacancy(VacancyUseCase):
    async def __call__(self, vacancy_id: int, company_id: int, published: bool) -> None:
        await self._tm.vacancy_dao.change_visibility_vacancy(vacancy_id, company_id, published)
        await self._tm.commit()


class RaiseVacancyInSearch(VacancyUseCase):
    async def __call__(self, vacancy_id: int, company_id: int) -> dict:
        try:
            res = await self._tm.vacancy_dao.raise_vacancy_in_search(vacancy_id, company_id)
            await self._tm.commit()

            return res

        except (NotUpdatedTimeVacancy, BaseVacancyException) as exc:
            logger.bind(
                app_name=f"{RaiseVacancyInSearch.__name__}"
            ).error(f"WITH ID {vacancy_id}\nEXCEPTION {exc.message()}")
            raise exc


class LikeVacancyByApplicant(VacancyUseCase):
    async def __call__(self, vacancy_id: int, applicant_id: int) -> None:
        try:
            await self._tm.vacancy_dao.like_vacancy_by_applicant(vacancy_id, applicant_id)
            await self._tm.commit()

        except VacancyNotFoundByID as exc:
            logger.bind(
                app_name=f"{LikeVacancyByApplicant.__name__}"
            ).error(f"WITH ID {vacancy_id}\nEXCEPTION {exc.message()}")
            await self._tm.rollback()
            raise exc


class DislikeVacancyByApplicant(VacancyUseCase):
    async def __call__(self, vacancy_id: int, applicant_id: int) -> None:
        try:
            await self._tm.vacancy_dao.dislike_vacancy_by_applicant(vacancy_id, applicant_id)
            await self._tm.commit()

        except VacancyNotFoundByID as exc:
            logger.bind(
                app_name=f"{DislikeVacancyByApplicant.__name__}"
            ).error(f"WITH ID {vacancy_id}\nEXCEPTION {exc.message()}")
            await self._tm.rollback()
            raise exc


class GetAllLikedVacanciesByApplicant(VacancyUseCase):
    async def __call__(self, applicant_id: int) -> list[BaseVacancyDTO]:
        res = await self._tm.vacancy_dao.get_all_liked_vacancy(applicant_id)

        return [
            BaseVacancyDTO(
                company=BaseCompanyDTO(
                    user=BaseUserDTO(
                        user_id=vacancy.company.user.user_id
                    ),
                    company_name=vacancy.company.company_name,
                    address=vacancy.company.address,
                ),
                vacancy_id=vacancy.vacancy_id,
                title=vacancy.title,
                experience_start=vacancy.experience_start,
                experience_end=vacancy.experience_end,
                is_published=vacancy.is_published
            )
            for vacancy in res
        ]


class VacancyService:
    def __init__(self, tm: IBaseTransactionManager):
        self._tm = tm

    async def create_vacancy(self, vacancy_dto: CreateVacancyDTO) -> VacancyOutDTO:
        return await CreateVacancy(self._tm)(vacancy_dto)

    async def update_vacancy(self, vacancy_dto: UpdateVacancyDTO) -> None:
        await UpdateVacancy(self._tm)(vacancy_dto)

    async def get_vacancy_by_id(self, vacancy_id) -> BaseVacancyDTO:
        return await GetVacancyByID(self._tm)(vacancy_id)

    async def search_vacancy(self):
        ...

    async def delete_vacancy(self, vacancy_id: int, company_id: int) -> None:
        await DeleteVacancy(self._tm)(vacancy_id, company_id)

    async def change_visibility_vacancy(self, vacancy_id: int, company_id: int, published: bool) -> None:
        """
        Change visibility vacancy is search
        param:
            published: bool - value is responsible for visibility vacancy
        """
        await ChangeVisibilityVacancy(self._tm)(vacancy_id, company_id, published)

    async def raise_vacancy_in_search(self, vacancy_id: int, company_id: int) -> dict:
        """
        Raise vacancy to top in search
        """
        return await RaiseVacancyInSearch(self._tm)(vacancy_id, company_id)

    async def like_vacancy_by_applicant(self, vacancy_id: int, applicant_id: int) -> None:
        await LikeVacancyByApplicant(self._tm)(vacancy_id, applicant_id)

    async def dislike_vacancy_by_applicant(self, vacancy_id: int, applicant_id: int) -> None:
        await DislikeVacancyByApplicant(self._tm)(vacancy_id, applicant_id)

    async def get_all_liked_vacancies_by_applicant(self, applicant_id: int) -> list[BaseVacancyDTO]:
        return await GetAllLikedVacanciesByApplicant(self._tm)(applicant_id)
