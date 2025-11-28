from fastapi import APIRouter, Depends, status, Body

from src.api.permissions import company_required, applicant_required
from src.api.providers.abstract.services import respond_vacancy_provider
from src.api.providers.auth import TokenAuthDep
from src.core.enums import ActorType
from src.dto.services.respond_on_vacancy.respond_on_vacancy import CreateRespondOnVacancyDTO
from src.services.respond_on_vacancy.respond_on_vacancy import RespondOnVacancyService


respond_on_vacancy_router = APIRouter(
    prefix="/responds",
    tags=["Respond"]
)


@respond_on_vacancy_router.post(
    "/response_by_company/{vacancy_id}/{resume_id}",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Respond to applicant was created"},
        400: {"description": "Response already maked. Yor can make once response"},
        403: {"description": "Company access required"},
        500: {"description": "Internal Server Error"}
    }
)
@company_required
async def respond_by_company(
        vacancy_id: int,
        resume_id: int,
        auth: TokenAuthDep,
        message: str = Body(None),
        respond_service: RespondOnVacancyService = Depends(respond_vacancy_provider)
):
    respond_dto = CreateRespondOnVacancyDTO(
        user_id=auth.request.state.user.user_id,
        resume_id=resume_id,
        vacancy_id=vacancy_id,
        responder_type=ActorType.COMPANY,
        message=message
    )

    await respond_service.create_respond_by_company(respond_dto)
    return {"detail": "Respond to applicant resume was created"}


@respond_on_vacancy_router.post(
    "/response_by_applicant/{resume_id}/{vacancy_id}",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Respond to applicant was created"},
        400: {"description": "Response already maked. Yor can make once response"},
        403: {"description": "Company access required"},
        500: {"description": "Internal Server Error"}
    }
)
@applicant_required
async def respond_by_applicant(
        resume_id: int,
        vacancy_id: int,
        auth: TokenAuthDep,
        message: str = Body(None),
        respond_service: RespondOnVacancyService = Depends(respond_vacancy_provider)
):
    respond_dto = CreateRespondOnVacancyDTO(
        user_id=auth.request.state.user.user_id,
        resume_id=resume_id,
        vacancy_id=vacancy_id,
        responder_type=ActorType.APPLICANT,
        message=message
    )

    await respond_service.create_respond_by_applicant(respond_dto)
    return {"detail": "Respond to company vacancy was created"}
