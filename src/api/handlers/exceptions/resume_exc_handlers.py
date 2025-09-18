from starlette.responses import JSONResponse

from src.exceptions.infrascructure import BaseResumeException
from src.exceptions.infrascructure.resume.resume import ResumeException, ResumeNotFoundByID


def resume_exception_handler(_, exc: BaseResumeException):
    match exc:
        case ResumeException():
            return JSONResponse(status_code=400, content={"message": exc.message()})

        case ResumeNotFoundByID():
            return JSONResponse(status_code=404, content={"message": exc.message()})
