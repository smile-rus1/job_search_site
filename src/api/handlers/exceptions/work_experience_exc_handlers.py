from fastapi.responses import JSONResponse

from src.exceptions.infrascructure import BaseWorkExperiencesException
from src.exceptions.infrascructure.work_experiences.work_experiences import (
    WorkExperiences,
    WorkExperiencesNotFoundByID
)


def work_experience_exception_handler(_, exc: BaseWorkExperiencesException):
    match exc:
        case WorkExperiences():
            return JSONResponse(status_code=400, content={"message": exc.message()})

        case WorkExperiencesNotFoundByID():
            return JSONResponse(status_code=404, content={"message": exc.message()})
