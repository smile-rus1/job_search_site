import json

from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from src.exceptions.base import BaseExceptions
from src.exceptions.services.auth import AuthException


async def auth_exception_handler(_, exc: AuthException):
    return JSONResponse(status_code=401, content={"message": exc.message()})


async def db_exception_handler(_, exc: BaseExceptions):
    return JSONResponse(status_code=401, content={"message": exc.message()})


async def validation_exception_handler(_, err: ValidationError | RequestValidationError):
    return JSONResponse(status_code=400, content=json.loads(err.json()))


async def request_validation_exception_handler(_, err: RequestValidationError):
    return JSONResponse(status_code=400, content=err.errors())
