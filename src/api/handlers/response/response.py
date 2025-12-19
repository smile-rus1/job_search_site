from fastapi import APIRouter, Depends, status, Body

from src.api.permissions import company_required, applicant_required, login_required
from src.api.providers.abstract.services import response_service_provider
from src.api.providers.auth import TokenAuthDep
from src.core.enums import ActorType, StatusRespond
from src.dto.services.response.response import CreateResponseDTO, ChangeStatusResponseDTO
from src.services.response.response import ResponseService


response_router = APIRouter(
    prefix="/responds",
    tags=["Respond"]
)


@response_router.post(
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
        respond_service: ResponseService = Depends(response_service_provider)
):
    respond_dto = CreateResponseDTO(
        user_id=auth.request.state.user.user_id,
        resume_id=resume_id,
        vacancy_id=vacancy_id,
        responder_type=ActorType.COMPANY,
        message=message
    )

    await respond_service.create_response_by_company(respond_dto)
    return {"detail": "Respond to applicant resume was created"}


@response_router.post(
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
        message: str = Body(None, embed=True),
        respond_service: ResponseService = Depends(response_service_provider)
):
    respond_dto = CreateResponseDTO(
        user_id=auth.request.state.user.user_id,
        resume_id=resume_id,
        vacancy_id=vacancy_id,
        responder_type=ActorType.APPLICANT,
        message=message
    )

    await respond_service.create_response_by_applicant(respond_dto)
    return {"detail": "Respond to company vacancy was created"}


@response_router.patch(
    "/change_status/{response_id}",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        202: {"description": "Respond changed"},
        400: {"description": "You cannot change this response"},
        403: {"description": "Login required"},
        500: {"description": "Internal Server Error"}
    }
)
@login_required
async def change_status_respond(
        response_id: int,
        auth: TokenAuthDep,
        message: str = Body(None, embed=True),
        status_response: StatusRespond = Body(..., embed=True),
        respond_service: ResponseService = Depends(response_service_provider)
):
    responder_type = ActorType.COMPANY if auth.request.state.user.type == "company" else ActorType.APPLICANT

    respond_dto = ChangeStatusResponseDTO(
        user_id=auth.request.state.user.user_id,
        response_id=response_id,
        message=message,
        responder_type=responder_type,
        status=status_response
    )
    await respond_service.change_status_response(respond_dto)
    return {"detail": f"Status changed on {status_response}"}
