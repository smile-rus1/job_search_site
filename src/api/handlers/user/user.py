from fastapi import APIRouter, Depends, status

from src.api.handlers.user.requests.user import UpdateUserRequest
from src.api.permissions import login_required
from src.api.providers.abstract.services import user_service_provider
from src.api.providers.auth import TokenAuthDep
from src.dto.services.user.user import UpdateUserDTO
from src.services.user.user import UserService


user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.patch(
    "/{user_id}",
    status_code=status.HTTP_201_CREATED,
    responses={
        202: {"description": "User updated"},
        401: {"description": "Not authenticated"},
        409: {"description": "User with this email does not exist"},
        500: {"description": "Internal Server Error"}
    }
)
@login_required
async def update_user(
        user_id: int,
        user_data: UpdateUserRequest,
        auth: TokenAuthDep,
        user_service: UserService = Depends(user_service_provider)
):
    user_dto = UpdateUserDTO(
        user_id=user_id,
        email=auth.request.state.user.email,
        **user_data.__dict__
    )
    await user_service.update_user(user_dto)
    return {"detail": "User has been update"}
