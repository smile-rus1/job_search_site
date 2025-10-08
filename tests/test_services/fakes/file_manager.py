from typing import Type, Callable

from src.interfaces.infrastructure.files_work import IFileStorage
from src.services.files_work.files_manager import FilesManager


class FakeFileStorage(IFileStorage):
    def __init__(self):
        self.saved = []

    async def save_file(self, file: Type[Callable], filename: str) -> str | None:
        self.saved.append((file, filename))
        return f"/fakes/dir/{filename}"


class FakeFileManager(FilesManager):
    def __init__(self, file_storage: IFileStorage):
        super().__init__(file_storage)

