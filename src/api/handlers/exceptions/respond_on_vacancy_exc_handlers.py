from starlette.responses import JSONResponse

from src.exceptions.infrascructure.respond_on_vacancy.respond_on_vacancy import (
    BaseRespondOnVacancyException,
    ResponseAlreadyMaked,
    ResponseNotFoundOnVacancyOrResume,
    ResponsePermissionError
)


def respond_on_vacancy_exception_handler(_, exc: BaseRespondOnVacancyException):
    match exc:
        case ResponseAlreadyMaked():
            return JSONResponse(status_code=400, content={"message": exc.message()})

        case ResponseNotFoundOnVacancyOrResume():
            return JSONResponse(status_code=400, content={"message": exc.message()})

        case ResponsePermissionError():
            return JSONResponse(status_code=400, content={"message": exc.message()})

        case BaseRespondOnVacancyException():
            return JSONResponse(status_code=500, content={"message": "Sorry, service not available, please try later"})
