from starlette.responses import JSONResponse

from src.exceptions.infrascructure.response.response import (
    BaseResponseException,
    ResponseAlreadyMaked,
    ResponseNotFoundOnVacancyOrResume,
    ResponsePermissionError
)


def response_exception_handler(_, exc: BaseResponseException):
    match exc:
        case ResponseAlreadyMaked():
            return JSONResponse(status_code=400, content={"message": exc.message()})

        case ResponseNotFoundOnVacancyOrResume():
            return JSONResponse(status_code=400, content={"message": exc.message()})

        case ResponsePermissionError():
            return JSONResponse(status_code=400, content={"message": exc.message()})

        case BaseResponseException():
            return JSONResponse(status_code=500, content={"message": "Sorry, service not available, please try later"})
