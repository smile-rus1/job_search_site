from fastapi import APIRouter, Depends, status

from src.api.handlers.company.requests.company import UpdateCompanyRequest, SearchCompanyRequest
from src.api.handlers.company.response.company import CompanyOut, CompanyDataResponse
from src.api.handlers.user.response.user import UserOut
from src.api.permissions import company_required
from src.api.providers.abstract.services import company_service_provider
from src.api.providers.auth import TokenAuthDep
from src.dto.services.company.company import UpdateCompanyDTO, SearchDTO
from src.services.company.company import CompanyService


company_router = APIRouter(prefix="/companies", tags=["Companies"])


@company_router.patch(
    "/{company_id}",
    status_code=status.HTTP_201_CREATED,
    responses={
        202: {"description": "Company updated"},
        401: {"description": "Not authenticated"},
        409: {"description": "Company with this email does not exist"},
        500: {"description": "Internal Server Error"}
    }
)
@company_required
async def update_company(
        user_id: int,
        company_data: UpdateCompanyRequest,
        auth: TokenAuthDep,
        company_service: CompanyService = Depends(company_service_provider)
):
    company_dto = UpdateCompanyDTO(
        user_id=user_id,
        email=auth.request.state.user.email,
        **company_data.__dict__
    )

    await company_service.update_company(company_dto)
    return {"detail": "Company has been updated"}


@company_router.get(
    "/{company_id}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Company info"},
        404: {"description": "Company with id not found!"},
        500: {"description": "Internal Server Error"}
    }
)
async def get_company(
        company_id: int,
        company_service: CompanyService = Depends(company_service_provider)
):
    company_data = await company_service.get_company(company_id)
    return CompanyOut(
        user=UserOut(
            user_id=company_data.company_id,
            last_name=company_data.user.last_name,
            first_name=company_data.user.first_name,
            email=company_data.user.email
        ),
        address=company_data.address,
        company_name=company_data.company_name,
        description_company=company_data.description_company
    )


@company_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[CompanyDataResponse],
    responses={
        200: {"description": "Companies info"},
        500: {"description": "Internal Server Error"}
    }
)
async def search_company(
        search_company_data: SearchCompanyRequest = Depends(),
        company_service: CompanyService = Depends(company_service_provider)
):
    search_dto = SearchDTO(**search_company_data.__dict__)
    companies = await company_service.search_companies(search_dto)

    return [
        CompanyDataResponse(**company.__dict__)
        for company in companies
    ]
