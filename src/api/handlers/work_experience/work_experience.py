from fastapi import APIRouter, Depends, status

from src.api.handlers.work_experience.request.work_experience import (
    CreateWorkExperienceRequest,
    UpdateWorkExperienceRequest
)
from src.api.handlers.work_experience.response.work_experience import WorkExperienceResponse
from src.api.permissions import applicant_required
from src.api.providers.abstract.services import work_experience_service_provider
from src.api.providers.auth import TokenAuthDep
from src.dto.services.work_exprerience.work_experience import (
    CreateWorkExperienceDTO,
    UpdateWorkExperienceDTO
)
from src.services.work_experience.work_experience import WorkExperienceService


work_experience_router = APIRouter(
    prefix="/work_experiences",
    tags=["WorkExperiences"]
)


@work_experience_router.post(
    "/",
    response_model=WorkExperienceResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        202: {"description": "WorkExperience was created"},
        403: {"description": "Applicant access required"},
        500: {"description": "Internal Server Error"}
    }
)
@applicant_required
async def create_work_experience(
        resume_id: int,
        auth: TokenAuthDep,
        work_experience_data: CreateWorkExperienceRequest,
        work_experience: WorkExperienceService = Depends(work_experience_service_provider)
):
    work_experience_dto = CreateWorkExperienceDTO(
        resume_id=resume_id,
        applicant_id=auth.request.state.user.user_id,
        **work_experience_data.__dict__
    )
    result = await work_experience.create_work_experience(work_experience_dto)

    return WorkExperienceResponse(**result.__dict__)


@work_experience_router.patch(
    "/{work_experience_id}",
    status_code=status.HTTP_201_CREATED,
    responses={
        202: {"description": "WorkExperience was updated"},
        403: {"description": "Applicant access required"},
        500: {"description": "Internal Server Error"}
    }
)
@applicant_required
async def update_work_experience(
        resume_id: int,
        work_experience_id: int,
        auth: TokenAuthDep,
        work_experience_data: UpdateWorkExperienceRequest,
        work_experience: WorkExperienceService = Depends(work_experience_service_provider)
):
    work_experience_dto = UpdateWorkExperienceDTO(
        resume_id=resume_id,
        work_experience_id=work_experience_id,
        applicant_id=auth.request.state.user.user_id,
        **work_experience_data.__dict__
    )
    await work_experience.update_work_experience(work_experience_dto)

    return {"detail": "WorkExperience was updated"}


@work_experience_router.get(
    "/{work_experience_id}",
    status_code=status.HTTP_200_OK,
    response_model=WorkExperienceResponse,
    responses={
        200: {"description": "WorkExperience deleted"},
        404: {"description": "WorkExperience not found!"},
        500: {"description": "Internal Server Error"}
    }
)
async def get_work_experience_by_id(
        work_experience_id: int,
        work_experience: WorkExperienceService = Depends(work_experience_service_provider)
):
    work_experience_dto = await work_experience.get_work_experience_by_id(work_experience_id)
    return WorkExperienceResponse(**work_experience_dto.__dict__)


@work_experience_router.delete(
    "/{work_experience_id}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "WorkExperience deleted"},
        403: {"description": "Applicant access required"},
        500: {"description": "Internal Server Error"}
    }
)
@applicant_required
async def delete_work_experience(
        resume_id: int,
        work_experience_id: int,
        auth: TokenAuthDep,
        work_experience: WorkExperienceService = Depends(work_experience_service_provider)
):
    await work_experience.delete_work_experience(
        auth.request.state.user.user_id,
        resume_id,
        work_experience_id
    )

    return {"detail": "WorkExperience deleted"}
