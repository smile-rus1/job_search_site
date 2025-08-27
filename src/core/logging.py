from loguru import logger


def setup_logging():
    import os

    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    log_file_path = os.path.join(logs_dir, "log.txt")
    os.makedirs(logs_dir, exist_ok=True)
    logger.add(
        log_file_path,
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
        level="INFO",
        rotation="10 MB"
    )

