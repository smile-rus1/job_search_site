from typing import Annotated

from fastapi import Depends

from starlette.requests import Request
from starlette.responses import Response


from src.infrastructure.auth.jwt import JWTAuth
from src.interfaces.services.auth import IJWTAuth


async def get_jwt_token_auth(request: Request = None, response: Response = None) -> JWTAuth:
    return JWTAuth(request=request, response=response)


TokenAuthDep = Annotated[IJWTAuth, Depends(get_jwt_token_auth)]
