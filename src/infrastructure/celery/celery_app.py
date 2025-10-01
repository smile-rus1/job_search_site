from celery import Celery

from src.core.config_reader import config


celery_app = Celery(
    "mail_tasks",
    broker=f"redis://{config.redis.host}:{config.redis.port}/0",
    backend=f"redis://{config.redis.host}:{config.redis.port}/0"
)
