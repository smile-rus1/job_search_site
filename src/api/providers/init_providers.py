from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.middleware.auth import AuthenticationMiddleware
from src.api.providers import abstract

from src.core.config import Config
from src.api.providers import common as common_provide
from src.api.providers import services


def bind_common(app: FastAPI, config: Config):
    app.dependency_overrides[abstract.common.session_provider] = common_provide.db_session(config)
    app.dependency_overrides[abstract.common.redis_pool_provider] = common_provide.redis_pool_getter(config)
    app.dependency_overrides[abstract.common.hasher_provider] = common_provide.hasher_getter
    app.dependency_overrides[abstract.common.tm_provider] = common_provide.tm_getter
    app.dependency_overrides[abstract.common.fm_provider] = common_provide.fm_getter(config)
    app.dependency_overrides[abstract.common.redis_db_provider] = common_provide.redis_db_getter
    app.dependency_overrides[abstract.common.notification_email_provider] = common_provide.notification_email_getter


# def bind_auth(app: FastAPI):
#     ...


def bind_services(app: FastAPI):
    app.dependency_overrides[abstract.services.auth_service_provider] = services.auth_service_getter  # type: ignore
    app.dependency_overrides[abstract.services.user_service_provider] = services.user_service_getter  # type: ignore
    app.dependency_overrides[abstract.services.applicant_service_provider] = services.applicant_service_getter  # type: ignore
    app.dependency_overrides[abstract.services.company_service_provider] = services.company_service_getter  # type: ignore
    app.dependency_overrides[abstract.services.resume_service_provider] = services.resume_service_getter  # type: ignore
    app.dependency_overrides[abstract.services.work_experience_service_provider] = services.work_experience_getter  # type: ignore
    app.dependency_overrides[abstract.services.files_work_service_provider] = services.files_work_service_getter  # type: ignore
    app.dependency_overrides[abstract.services.vacancy_service_provider] = services.vacancy_service_getter  # type: ignore
    app.dependency_overrides[abstract.services.respond_vacancy_provider] = services.respond_vacancy_getter  # type: ignore


def bind_middlewares(app: FastAPI):
    app.add_middleware(AuthenticationMiddleware)  # type: ignore
    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def bind_providers(app: FastAPI, config: Config):
    bind_common(app, config)
    bind_middlewares(app)
    # bind_auth(app)
    bind_services(app)
