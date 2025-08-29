from fastapi import FastAPI

from src.api.providers import abstract

from src.core.config import Config
from src.api.providers import common as common_provide
from src.api.providers import auth, services


def bind_common(app: FastAPI, config: Config):
    app.dependency_overrides[abstract.common.session_provider] = common_provide.db_session(config)
    app.dependency_overrides[abstract.common.hasher_provider] = common_provide.hasher_getter
    app.dependency_overrides[abstract.common.tm_provider] = common_provide.tm_getter


def bind_auth(app: FastAPI):
    app.dependency_overrides[abstract.auth.auth_provider] = auth.CurrentUser


def bind_services(app: FastAPI):
    app.dependency_overrides[abstract.services.auth_service_provider] = services.auth_service_getter
    app.dependency_overrides[abstract.services.user_service_provider] = services.user_service

    app.dependency_overrides[abstract.services.applicant_service_provider] = services.applicant_service
    app.dependency_overrides[abstract.services.company_service_provider] = services.company_service


def bind_providers(app: FastAPI, config: Config):
    bind_common(app, config)
    bind_auth(app)
    bind_services(app)
