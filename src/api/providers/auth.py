from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from pydantic import ValidationError

from src.api.providers.abstract.services import user_service_provider
from src.core import security
from src.core.config_reader import config
from src.dto.services.user.user import UserDTO
from src.services.user.user import UserService


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{config.api.api_v1_str}/login/access-token"
)

TokenDep = Annotated[str, Depends(oauth2_scheme)]


async def current_user(
        token: TokenDep,
        user_service: UserService = Depends(user_service_provider)
) -> UserDTO:
    try:
        payload = security.decode_token(token)
        email_user = payload.get("email")

    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await user_service.get_user_by_email(email_user)
    return user


CurrentUser = Annotated[UserDTO, Depends(current_user)]
