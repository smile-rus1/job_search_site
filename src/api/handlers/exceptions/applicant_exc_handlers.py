from starlette.responses import JSONResponse

from src.exceptions.infrascructure.applicant.applicant import BaseApplicantException


def applicant_exception_handler(_, exc: BaseApplicantException):
    ...
