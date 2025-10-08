from pathlib import Path

from src.infrastructure.files_work.files_work import ImageStorage
from src.services.files_work.files_manager import FilesManager


def build_fm(
        base_dir: Path,
        chunk_size: int | None = None
):
    return FilesManager(
        file_storage=ImageStorage(base_dir, chunk_size=chunk_size)
    )
