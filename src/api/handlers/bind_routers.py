from fastapi import FastAPI, APIRouter
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from src.api.handlers.exceptions.common_exc_handlers import (
    auth_exception_handler,
    validation_exception_handler,
    request_validation_exception_handler,
)
from src.api.handlers.exceptions.user_exc_handlers import user_exception_handler
from src.api.handlers.user.auth import auth_router
from src.api.web_config import APIConfig
from src.exceptions.infrascructure.user.user import BaseUserException
from src.exceptions.services.auth import AuthException


def bind_exceptions_handlers(app: FastAPI):
    app.add_exception_handler(AuthException, auth_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    app.add_exception_handler(BaseUserException, user_exception_handler)


def bind_routers():
    api_routers = APIRouter()
    api_routers.include_router(auth_router)

    return api_routers


def bind_routes(app: FastAPI, config: APIConfig):
    routers = bind_routers()
    app.include_router(routers, prefix=config.api_v1_str)
