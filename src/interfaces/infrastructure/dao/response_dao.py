from src.dto.db.response.response import BaseResponseDTODAO


class IResponsesDAO:
    async def create_respond(self, respond: BaseResponseDTODAO) -> BaseResponseDTODAO:
        raise NotImplementedError

    async def change_status_respond(self, respond: BaseResponseDTODAO) -> BaseResponseDTODAO:
        raise NotImplementedError
