import os

from dotenv import load_dotenv

from src.api.auth_config import AuthConfig
from src.core.config import Config
from src.api.web_config import APIConfig
from src.infrastructure.db_config import DBConfig
from src.infrastructure.files_work.files_config import FilesWorkConfig
from src.infrastructure.mail.config import MailConfig
from src.infrastructure.redis_db.config import RedisConfig


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
            api_v1_str="/api/" + os.getenv("API_VERSION", "v1"),
            base_url=os.getenv("BASE_URL", "http://localhost:8000"),
            verify_endpoint=os.getenv("VERIFY_ENDPOINT")
        ),
        auth=AuthConfig(
            secret_key=os.getenv("AUTH_SECRET_KEY"),
            algorithm=os.getenv("AUTH_ALGORITHM"),

        ),
        redis=RedisConfig(
            host=os.getenv("REDIS_HOST", "127.0.0.1"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=int(os.getenv("REDIS_DB", 0))
        ),
        mail=MailConfig(
            smtp_server=os.getenv("SMTP_SERVER"),
            smtp_port=int(os.getenv("SMTP_PORT", 465)),
            smtp_user=os.getenv("SMTP_USER"),
            smtp_password=os.getenv("SMTP_PASSWORD"),
            mail_from=os.getenv("MAIL_FROM")
        ),
        files_work=FilesWorkConfig(
            url_save_file=os.getenv("URL_SAVE_FILE"),
            chunk_size=int(os.getenv("CHUNK_SIZE"))
        )
    )


config = config_loader()
