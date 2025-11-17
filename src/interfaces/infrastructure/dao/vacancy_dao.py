from src.dto.db.vacancy.vacancy import BaseVacancyDTODAO


class IVacancyDAO:
    async def create_vacancy(self, vacancy: BaseVacancyDTODAO) -> BaseVacancyDTODAO:
        raise NotImplementedError

    async def update_vacancy(self, vacancy: BaseVacancyDTODAO) -> None:
        raise NotImplementedError

    async def get_vacancy_by_id(self, vacancy_id: int) -> BaseVacancyDTODAO:
        raise NotImplementedError

    async def delete_vacancy(self, vacancy_id: int, company_id: int) -> None:
        raise NotImplementedError

    async def change_visibility_vacancy(self, vacancy_id: int, company_id: int, published: bool) -> None:
        raise NotImplementedError

    async def raise_vacancy_in_search(self, vacancy_id: int, company_id: int) -> dict:
        raise NotImplementedError

    async def like_vacancy_by_applicant(self, vacancy_id: int, applicant_id: int) -> None:
        raise NotImplementedError

    async def dislike_vacancy_by_applicant(self, vacancy_id: int, applicant_id: int) -> None:
        raise NotImplementedError

    async def get_all_liked_vacancy(self, applicant_id: int) -> list[BaseVacancyDTODAO]:
        ...
