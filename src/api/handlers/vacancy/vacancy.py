from fastapi import APIRouter, Depends, status, Body

from src.api.handlers.company.response.company import CompanyOut
from src.api.handlers.user.response.user import UserOut
from src.api.handlers.vacancy.requests.vacancy import CreateVacancyRequest, UpdateVacancyRequest
from src.api.handlers.vacancy.response.vacancy import VacancyResponse, VacancyTimeResponse
from src.api.handlers.vacancy.response.vacancy_access import VacancyAccessResponse
from src.api.handlers.vacancy.response.vacancy_type import VacancyTypeResponse
from src.api.permissions import company_required
from src.api.providers.abstract.services import vacancy_service_provider
from src.api.providers.auth import TokenAuthDep
from src.dto.services.company.company import BaseCompanyDTO
from src.dto.services.user.user import BaseUserDTO
from src.dto.services.vacancy.vacancy import CreateVacancyDTO, UpdateVacancyDTO
from src.dto.services.vacancy.vacancy_type import CreateVacancyType
from src.services.vacancy.vacancy import VacancyService


vacancy_router = APIRouter(
    prefix="/vacancies",
    tags=["Vacancies"]
)


@vacancy_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=VacancyResponse,
    responses={
        201: {"description": "Vacancy was created"},
        403: {"description": "Company access required"},
        500: {"description": "Internal Server Error"}
    }
)
@company_required
async def create_vacancy(
        vacancy_data: CreateVacancyRequest,
        auth: TokenAuthDep,
        vacancy_service: VacancyService = Depends(vacancy_service_provider)
):
    vacancy_dto = CreateVacancyDTO(
        company=BaseCompanyDTO(
            user=BaseUserDTO(
                user_id=auth.request.state.user.user_id
            )
        ),
        title=vacancy_data.title,
        profession=vacancy_data.profession,
        vacancy_type=CreateVacancyType(
            name=vacancy_data.vacancy_type.name,
            duration=vacancy_data.duration
        ),
        description=vacancy_data.description,
        location=vacancy_data.location,
        key_skills=vacancy_data.key_skills,
        salary_min=vacancy_data.salary_min,
        salary_max=vacancy_data.salary_max,
        salary_currency=vacancy_data.salary_currency,
        type_of_employment=vacancy_data.type_of_employment,
        type_work_schedule=vacancy_data.type_work_schedule,
        experience_start=vacancy_data.experience_start,
        experience_end=vacancy_data.experience_end
    )
    res = await vacancy_service.create_vacancy(vacancy_dto)

    return VacancyResponse(
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
        experience_start=vacancy_data.experience_start,
        experience_end=vacancy_data.experience_end
    )


@vacancy_router.patch(
    "/{vacancy_id}",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Vacancy updated"},
        403: {"description": "Company access required"},
        500: {"description": "Internal Server Error"}
    }
)
@company_required
async def update_vacancy(
        vacancy_id: int,
        vacancy_data: UpdateVacancyRequest,
        auth: TokenAuthDep,
        vacancy_service: VacancyService = Depends(vacancy_service_provider)
):
    vacancy_dto = UpdateVacancyDTO(
        company=BaseCompanyDTO(
            user=BaseUserDTO(
                user_id=auth.request.state.user.user_id
            )
        ),
        vacancy_id=vacancy_id,
        title=vacancy_data.title,
        profession=vacancy_data.profession,
        description=vacancy_data.description,
        location=vacancy_data.location,
        key_skills=vacancy_data.key_skills,
        salary_min=vacancy_data.salary_min,
        salary_max=vacancy_data.salary_max,
        salary_currency=vacancy_data.salary_currency,
        type_of_employment=vacancy_data.type_of_employment,
        type_work_schedule=vacancy_data.type_work_schedule,
        experience_start=vacancy_data.experience_start,
        experience_end=vacancy_data.experience_end
    )
    await vacancy_service.update_vacancy(vacancy_dto)

    return {"detail": "Vacancy updated"}


@vacancy_router.get(
    "/{vacancy_id}",
    status_code=status.HTTP_200_OK,
    response_model=VacancyResponse,
    responses={
        200: {"description": "Vacancy info"},
        404: {"description": "Vacancy not found"},
        500: {"description": "Internal Server Error"}
    }
)
async def get_vacancy_by_id(
        vacancy_id: int,
        vacancy_service: VacancyService = Depends(vacancy_service_provider)
):
    result = await vacancy_service.get_vacancy_by_id(vacancy_id)

    return VacancyResponse(
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
        vacancy_type=VacancyTypeResponse(
            name=result.vacancy_type.name
        ),
        vacancy_access=VacancyAccessResponse(
            duration=result.vacancy_access.duration,
            start_date=result.vacancy_access.start_date,
            end_date=result.vacancy_access.end_date,
            is_active=result.vacancy_access.is_active
        ),
        company=CompanyOut(
            company_name=result.company.company_name,
            address=result.company.address,
            company_is_confirmed=result.company.company_is_confirmed,
            description_company=None,
            user=UserOut(
                user_id=result.company.user.user_id,
                email=result.company.user.email,
                image_url=result.company.user.image_url,
                first_name=None,
                last_name=None,
            )
        )
    )


@vacancy_router.get(
    "/search",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": ""},
        403: {"description": "Company access required"},
        500: {"description": "Internal Server Error"}
    }
)
async def search_vacancy(
        vacancy_service: VacancyService = Depends(vacancy_service_provider)
):
    """
    Add the search feature a bit latter!
    """
    return


@vacancy_router.delete(
    "/{vacancy_id}",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        201: {"description": "Vacancy deleted"},
        403: {"description": "Company access required"},
        500: {"description": "Internal Server Error"}
    }
)
@company_required
async def delete_vacancy(
        vacancy_id: int,
        auth: TokenAuthDep,
        vacancy_service: VacancyService = Depends(vacancy_service_provider)
):
    await vacancy_service.delete_vacancy(vacancy_id, auth.request.state.user.user_id)
    return {"detail": "Vacancy deleted"}


@vacancy_router.patch(
    "/{vacancy_id}/change_visibility",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        202: {"description": "Visibility changed"},
        403: {"description": "Company access required"},
        500: {"description": "Internal Server Error"}
    }
)
@company_required
async def change_visibility_vacancy(
        vacancy_id: int,
        auth: TokenAuthDep,
        published: bool = Body(..., embed=True),
        vacancy_service: VacancyService = Depends(vacancy_service_provider)
):
    await vacancy_service.change_visibility_vacancy(vacancy_id, auth.request.state.user.user_id, published)

    return {"detail": "Visibility changed"}


@vacancy_router.patch(
    "/{vacancy_id}/raise_vacancy_in_search",
    status_code=status.HTTP_200_OK,
    response_model=VacancyTimeResponse,
    responses={
        200: {"description": "Vacancy raised in search"},
        403: {"description": "Company access required"},
        500: {"description": "Internal Server Error"}
    }
)
@company_required
async def raise_vacancy_in_search(
        vacancy_id: int,
        auth: TokenAuthDep,
        vacancy_service: VacancyService = Depends(vacancy_service_provider)
):
    res = await vacancy_service.raise_vacancy_in_search(vacancy_id, auth.request.state.user.user_id)

    return VacancyTimeResponse(
        next_update_in_hours=res.get("next_update_in_hours"),
        next_time_update=res.get("next_time_update")
    )
