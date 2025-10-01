from dataclasses import dataclass

from src.api.auth_config import AuthConfig
from src.api.web_config import APIConfig
from src.infrastructure.db_config import DBConfig
from src.infrastructure.mail.config import MailConfig
from src.infrastructure.redis_db.config import RedisConfig


@dataclass
class Config:
    db: DBConfig
    api: APIConfig
    auth: AuthConfig
    redis: RedisConfig
    mail: MailConfig
