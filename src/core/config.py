from dataclasses import dataclass

from src.api.auth_config import AuthConfig
from src.api.web_config import APIConfig
from src.infrastructure.db_config import DBConfig


@dataclass
class Config:
    db: DBConfig
    api: APIConfig
    auth: AuthConfig
