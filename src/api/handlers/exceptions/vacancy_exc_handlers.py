from starlette.responses import JSONResponse


from src.exceptions.infrascructure.vacancy.vacancy import (
    BaseVacancyException,
    VacancyException,
    VacancyTypeException,
    VacancyNotFoundByID,
    NotUpdatedTimeVacancy,
    VacancyAlreadyInLiked
)


def vacancy_exception_handler(_, exc: BaseVacancyException):
    match exc:
        case VacancyException():
            return JSONResponse(status_code=400, content={"message": exc.message()})

        case VacancyTypeException():
            return JSONResponse(status_code=404, content={"message": exc.message()})

        case VacancyNotFoundByID():
            return JSONResponse(status_code=404, content={"message": exc.message()})

        case NotUpdatedTimeVacancy():
            return JSONResponse(status_code=400, content={"message": exc.message()})

        case VacancyAlreadyInLiked():
            return JSONResponse(status_code=400, content={"message": exc.message()})

        case BaseVacancyException():
            return JSONResponse(status_code=500, content={"message": "Sorry, service not available, please try later"})
