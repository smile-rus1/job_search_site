from fastapi import FastAPI

from src.api.init_app import init_app
from src.core.config_reader import config
from src.core.logging import setup_logging


setup_logging()
app = init_app(
    FastAPI(),
    config
)


@app.get("/health-check")
async def heath_check():
    return {"detail": "Alive"}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        app="src.main:app",
        host=config.api.host,
        port=config.api.port,
        reload=True,
        log_level="info",
    )
