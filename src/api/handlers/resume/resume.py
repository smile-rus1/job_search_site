from fastapi import APIRouter, Depends, status, Query

from src.api.handlers.applicant.response.applicant import ApplicantOut
from src.api.handlers.resume.requests.resume import CreateResumeRequest, UpdateResumeRequest, SearchResumeRequest
from src.api.handlers.resume.response.resume import ResumeOutResponse, ResumeResponse, ResumeSearchOutResponse
from src.api.handlers.user.response.user import UserOut
from src.api.handlers.work_experience.response.work_experience import WorkExperienceResponse
from src.api.permissions import applicant_required
from src.api.providers.abstract.services import resume_service_provider
from src.api.providers.auth import TokenAuthDep
from src.dto.services.resume.resume import CreateResumeDTO, UpdateResumeDTO, SearchResumeDTO
from src.core.enums import EmploymentType
from src.services.resume.resume import ResumeService


resume_router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"]
)


@resume_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ResumeOutResponse,
    responses={
        201: {"description": "Resume was created"},
        403: {"description": "Applicant access required"},
        500: {"description": "Internal Server Error"}
    }

)
@applicant_required
async def create_resume(
        resume_data: CreateResumeRequest,
        auth: TokenAuthDep,
        resume_service: ResumeService = Depends(resume_service_provider)
):
    resume_dto = CreateResumeDTO(
        applicant_id=auth.request.state.user.user_id,
        **resume_data.__dict__
    )

    created_resume = await resume_service.create_resume(resume_dto)

    return ResumeOutResponse(**created_resume.__dict__)


@resume_router.patch(
    "/{resume_id}",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Resume updated"},
        403: {"description": "Applicant access required"},
        500: {"description": "Internal Server Error"}
    }

)
@applicant_required
async def update_resume(
        resume_id: int,
        resume_data: UpdateResumeRequest,
        auth: TokenAuthDep,
        resume_service: ResumeService = Depends(resume_service_provider)
):
    resume_dto = UpdateResumeDTO(
        resume_id=resume_id,
        applicant_id=auth.request.state.user.user_id,
        **resume_data.__dict__
    )
    await resume_service.update_resume(resume_dto)

    return {"detail": "Resume updated"}


@resume_router.get(
    "/{resume_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResumeResponse,
    responses={
        200: {"description": "Resume"},
        404: {"description": "Resume not found"},
        500: {"description": "Internal Server Error"}
    }

)
async def get_resume_by_id(
        resume_id: int,
        resume_service: ResumeService = Depends(resume_service_provider)
):
    resume_data = await resume_service.get_resume_by_id(resume_id)

    return ResumeResponse(
        resume_id=resume_data.resume_id,
        name_resume=resume_data.name_resume,
        profession=resume_data.profession,
        key_skills=resume_data.key_skills,
        salary_min=resume_data.salary_min,
        salary_max=resume_data.salary_max,
        salary_currency=resume_data.salary_currency,
        location=resume_data.location,
        applicant=ApplicantOut(
            user=UserOut(
                user_id=resume_data.applicant.applicant_id,
                last_name=resume_data.applicant.user.last_name,
                first_name=resume_data.applicant.user.first_name,
                email=resume_data.applicant.user.email
            ),
            description_applicant=resume_data.applicant.description_applicant,
            gender=resume_data.applicant.gender,
            address=resume_data.applicant.address,
            is_confirmed=resume_data.applicant.is_confirmed,
            level_education=resume_data.applicant.level_education,
        ),
        type_of_employment=resume_data.type_of_employment,
        work_experience=[
            WorkExperienceResponse(
                work_experience_id=we.work_experience_id,
                resume_id=we.resume_id,
                company_name=we.company_name,
                start_date=we.start_date,
                end_date=we.end_date,
                description_work=we.description_work,
            )
            for we in resume_data.work_experience
        ]
    )


@resume_router.get(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=list[ResumeSearchOutResponse],
    responses={
        200: {"description": "Resumes"},
        404: {"description": "Resume not found"},
        500: {"description": "Internal Server Error"}
    }

)
async def search_resumes(
        search: SearchResumeRequest = Depends(),
        type_of_employment: list[EmploymentType] | None = Query(None),
        resume_service: ResumeService = Depends(resume_service_provider)
):
    search_dto = SearchResumeDTO(
        type_of_employment=type_of_employment,
        **search.__dict__
    )
    resumes = await resume_service.search_resumes(search_dto)

    responses: list[ResumeSearchOutResponse] = []

    for r in resumes:
        applicant = ApplicantOut(
            address=r.applicant.address,
            level_education=r.applicant.level_education,
            date_born=r.applicant.date_born,
            gender=r.applicant.gender,
            user=UserOut(
                user_id=r.applicant.applicant_id,
                email=r.applicant.user.email,
                first_name=r.applicant.user.first_name,
                last_name=r.applicant.user.last_name,
                phone_number=r.applicant.user.phone_number,
                image_url=r.applicant.user.image_url,
            ),
        )

        work_exps = [
            WorkExperienceResponse(
                resume_id=w.resume_id,
                work_experience_id=w.work_experience_id,
                company_name=w.company_name,
                start_date=w.start_date,
                end_date=w.end_date,
                description_work=w.description_work,
            )
            for w in r.work_experiences
        ]

        responses.append(
            ResumeSearchOutResponse(
                resume_id=r.resume_id,
                applicant=applicant,
                name_resume=r.name_resume,
                profession=r.profession,
                key_skills=r.key_skills,
                salary_min=r.salary_min,
                salary_max=r.salary_max,
                salary_currency=r.salary_currency,
                location=r.location,
                total_months=r.total_months,
                work_experiences=work_exps,
            )
        )

    return responses


@resume_router.delete(
    "/{resume_id}",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        201: {"description": "Resume deleted"},
        403: {"description": "Applicant access required"},
        500: {"description": "Internal Server Error"}
    }

)
@applicant_required
async def delete_resume(
        resume_id: int,
        auth: TokenAuthDep,
        resume_service: ResumeService = Depends(resume_service_provider)
):
    await resume_service.delete_resume(resume_id, auth.request.state.user.user_id)
    return {"detail": "deleted"}
