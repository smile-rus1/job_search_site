from fastapi import APIRouter, Depends, status

from src.api.handlers.user.requests.auth import CreateApplicantRequest, CreateCompanyRequest, AuthDataRequest
from src.api.providers.abstract import services
from src.api.handlers.user.response.user import UserOut
from src.api.providers.auth import TokenAuthDep
from src.dto.services.applicant.applicant import CreateApplicantDTO
from src.dto.services.company.company import CreateCompanyDTO
from src.dto.services.user.auth import AuthUserDTO
from src.dto.services.user.user import CreateUserDTO
from src.services.applicant.applicant import ApplicantService
from src.services.company.company import CompanyService
from src.services.user.auth import AuthService


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post(
    "/register/applicant",
    status_code=status.HTTP_201_CREATED,
    response_model=UserOut,
    responses={
        200: {"description": "Registered"},
        409: {"description": "User already exist"},
        500: {"description": "Internal Server Error"}
    }
)
async def register_applicant(
        applicant_data: CreateApplicantRequest,
        applicant_service: ApplicantService = Depends(services.applicant_service_provider)
):
    applicant_dto = CreateApplicantDTO(
        user=CreateUserDTO(
            email=applicant_data.user.email,
            password=applicant_data.user.password,
            last_name=applicant_data.user.last_name,
            first_name=applicant_data.user.first_name,
            image_url=applicant_data.user.image_url,  # тут нужно будет передавать не image_url а саму картинку
            phone_number=applicant_data.user.phone_number
        ),
        description_applicant=applicant_data.description_applicant,
        address=applicant_data.address,
        level_education=applicant_data.level_education,
        gender=applicant_data.gender,
        date_born=applicant_data.date_born

    )
    applicant_out = await applicant_service.create_applicant(applicant_dto)

    return UserOut(
        user_id=applicant_out.user.user_id,
        last_name=applicant_out.user.last_name,
        first_name=applicant_out.user.first_name,
        email=applicant_out.user.email
    )


@auth_router.post(
    "/register/company",
    status_code=status.HTTP_201_CREATED,
    response_model=UserOut,
    responses={
        200: {"description": "Registered"},
        409: {"description": "User already exist"},
        500: {"description": "Internal Server Error"}
    }
)
async def register_company(
        company_data: CreateCompanyRequest,
        company_service: CompanyService = Depends(services.company_service_provider)
):
    company_dto = CreateCompanyDTO(
        user=CreateUserDTO(
            email=company_data.user.email,
            password=company_data.user.password,
            last_name=company_data.user.last_name,
            first_name=company_data.user.first_name,
            image_url=company_data.user.image_url,  # тут нужно будет передавать не image_url а саму картинку
            phone_number=company_data.user.phone_number
        ),
        company_name=company_data.company_name,
        description_company=company_data.description_company,
        address=company_data.address
    )
    company_out = await company_service.create_company(company_dto)

    return UserOut(
        user_id=company_out.user.user_id,
        last_name=company_out.user.last_name,
        first_name=company_out.user.first_name,
        email=company_out.user.email
    )


@auth_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    responses={
        401: {"description": "Not registered"},
        500: {"description": "Internal Server Error"}
    }
)
async def login_user(
        auth_data: AuthDataRequest,
        auth: TokenAuthDep,
        auth_service: AuthService = Depends(services.auth_service_provider),
):
    """
    Authorize user in system
    """

    auth_dto = AuthUserDTO(email=auth_data.email, password=auth_data.password)
    await auth_service.authenticate_user(auth_dto, auth)

    return {"detail": "Tokens set"}


@auth_router.post(
    "/logout",
    status_code=status.HTTP_200_OK
)
async def logout(auth: TokenAuthDep):
    await auth.unset_tokens()
    return {"detail": "Tokens deleted"}


@auth_router.post(
    "/refresh",
    status_code=status.HTTP_200_OK
)
async def refresh_access_token(auth: TokenAuthDep):
    await auth.refresh_access_token()
    return {"detail": "Access token has been refresh"}
