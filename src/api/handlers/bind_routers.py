from fastapi import FastAPI, APIRouter
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from src.api.handlers import (
    auth_router,
    user_router,
    applicant_router,
    company_router,
    resume_router,
    work_experience_router
)

from src.api.handlers.exceptions import (
    auth_exception_handler,
    validation_exception_handler,
    request_validation_exception_handler,
    user_exception_handler,
    applicant_exception_handler,
    company_exception_handler,
    resume_exception_handler, work_experience_exception_handler,
)

from src.api.web_config import APIConfig
from src.exceptions.infrascructure import (
    BaseUserException,
    BaseApplicantException,
    BaseResumeException, BaseWorkExperiencesException
)
from src.exceptions.infrascructure.company.company import BaseCompanyException
from src.exceptions.services.auth import AuthException


def bind_exceptions_handlers(app: FastAPI):
    app.add_exception_handler(AuthException, auth_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)

    """
    Подправить те, которые идут снизу, чтобы не из инфры были exceptions, а из сервисов!
    """
    app.add_exception_handler(BaseUserException, user_exception_handler)
    app.add_exception_handler(BaseApplicantException, applicant_exception_handler)
    app.add_exception_handler(BaseCompanyException, company_exception_handler)
    app.add_exception_handler(BaseResumeException, resume_exception_handler)
    app.add_exception_handler(BaseWorkExperiencesException, work_experience_exception_handler)


def bind_routers():
    api_routers = APIRouter()
    api_routers.include_router(auth_router)
    api_routers.include_router(user_router)
    api_routers.include_router(applicant_router)
    api_routers.include_router(company_router)
    api_routers.include_router(resume_router)
    api_routers.include_router(work_experience_router)

    return api_routers


def bind_routes(app: FastAPI, config: APIConfig):
    routers = bind_routers()
    app.include_router(routers, prefix=config.api_v1_str)
