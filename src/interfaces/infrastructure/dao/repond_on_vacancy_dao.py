from src.dto.db.respond_on_vacancy.respond_on_vacancy import BaseRespondOnVacancyDTODAO


class IRespondOnVacancyDAO:
    async def create_respond(self, respond: BaseRespondOnVacancyDTODAO) -> BaseRespondOnVacancyDTODAO:
        raise NotImplementedError

    async def change_status_respond(self, respond: BaseRespondOnVacancyDTODAO) -> None:
        raise NotImplementedError
