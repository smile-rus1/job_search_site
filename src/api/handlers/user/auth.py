from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from src.api.providers.auth import CurrentUser
from src.core import security

from src.api.handlers.user.requests.auth import CreateUserRequest, UserOut, Token
from src.api.providers.abstract.services import user_service_provider, auth_service_provider
from src.dto.services.user.auth import AuthUserDTO
from src.dto.services.user.user import CreateUserDTO
from src.services.user.auth import AuthService
from src.services.user.user import UserService


auth_router = APIRouter(tags=["Auth"])


@auth_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    responses={
        200: {"description": "Registered"},
        409: {"description": "User already exist"},
        500: {"description": "Internal Server Error"}
    }
)
async def register_user(  # тут сделать, чтобы регистрация была для applicant и company
        user_data: CreateUserRequest,
        user_service: UserService = Depends(user_service_provider)
):
    user_dto = CreateUserDTO(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        password=user_data.password,
        phone_number=user_data.phone_number,
        image_url=user_data.image_url
    )
    user = await user_service.create_user(user_dto)
    return UserOut(
        user_id=user.user_id,
        last_name=user.last_name,
        first_name=user.first_name,
        email=user.email
    )


@auth_router.post(
    "/login/access-token",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"description": "Not registered"},
        500: {"description": "Internal Server Error"}
    }
)
async def login_user(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        auth_service: AuthService = Depends(auth_service_provider)
):
    auth_dto = AuthUserDTO(email=form_data.username, password=form_data.password)
    user = await auth_service.authenticate_user(auth_dto)

    data_dct = {
        "user_id": user.user_id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    }
    access_token = security.create_access_token(data_dct)

    # мб тут сделать ещё с рефреш-токеном!
    return Token(
        access_token=access_token
    )


# @auth_router.get("/prosto")
# async def prosto(user: CurrentUser):
#     return {"msg": "SECURITY"}
