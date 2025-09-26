import os

from dotenv import load_dotenv

from src.api.auth_config import AuthConfig
from src.core.config import Config
from src.api.web_config import APIConfig
from src.infrastructure.db_config import DBConfig


def config_loader() -> Config:
    load_dotenv()

    return Config(
        db=DBConfig(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=int(os.getenv("DB_PORT", 5432)),
            driver=os.getenv("DB_DRIVER"),
            db_name=os.getenv("DB_NAME")
        ),
        api=APIConfig(
            port=int(os.getenv("WEB_PORT", 8000)),
            host=os.getenv("WEB_HOST", "localhost"),
            debug=bool(os.getenv("DEBUG", True)),
            api_v1_str="/api/" + os.getenv("API_VERSION", "v1")
        ),
        auth=AuthConfig(
            secret_key=os.getenv("AUTH_SECRET_KEY"),
            algorithm=os.getenv("AUTH_ALGORITHM"),

        ),
    )


config = config_loader()
