from fastapi import APIRouter, Depends, status

from src.api.handlers.applicant.requests.applicant import UpdateApplicantRequest
from src.api.handlers.applicant.response.applicant import ApplicantOut
from src.api.handlers.user.response.user import UserOut
from src.api.permissions import applicant_required
from src.api.providers.abstract.services import applicant_service_provider
from src.api.providers.auth import TokenAuthDep
from src.dto.services.applicant.applicant import UpdateApplicantDTO
from src.services.applicant.applicant import ApplicantService


applicant_router = APIRouter(prefix="/applicants", tags=["Applicants"])


@applicant_router.patch(
    "/{applicant_id}",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Applicant updated"},
        401: {"description": "Not authenticated"},
        409: {"description": "Applicant with this email does not exist"},
        500: {"description": "Internal Server Error"}
    }
)
@applicant_required
async def update_applicant(
        applicant_id: int,
        applicant_data: UpdateApplicantRequest,
        auth: TokenAuthDep,
        applicant_service: ApplicantService = Depends(applicant_service_provider)
):
    applicant_dto = UpdateApplicantDTO(
        user_id=applicant_id,
        email=auth.request.state.user.email,
        **applicant_data.__dict__
    )

    await applicant_service.update_applicant(applicant_dto)
    return {"detail": "Applicant has been updated"}


@applicant_router.get(
    "/{applicant_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApplicantOut,
    responses={
        200: {"description": "Applicant info"},
        404: {"description": "Applicant with id not found!"},
        500: {"description": "Internal Server Error"}
    }
)
async def get_applicant(
        applicant_id: int,
        applicant_service: ApplicantService = Depends(applicant_service_provider)
):
    applicant_data = await applicant_service.get_applicant(applicant_id)

    return ApplicantOut(
        user=UserOut(
            user_id=applicant_data.applicant_id,
            last_name=applicant_data.user.last_name,
            first_name=applicant_data.user.first_name,
            email=applicant_data.user.email
        ),
        description_applicant=applicant_data.description_applicant,
        address=applicant_data.address,
        gender=applicant_data.gender,
        is_confirmed=applicant_data.is_confirmed,
        level_education=applicant_data.level_education
    )
