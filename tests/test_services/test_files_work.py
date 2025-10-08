import uuid

import pytest

from src.services.files_work.files_work import FilesWorkService
from test_services.fakes.file_manager import FakeFileStorage, FakeFileManager


@pytest.mark.asyncio
async def test_upload_local_files(monkeypatch):
    fake_storage = FakeFileStorage()
    fake_manager = FakeFileManager(fake_storage)

    files_service = FilesWorkService(fake_manager)
    fixed_uuid = "abc123"

    monkeypatch.setattr(uuid, "uuid4", lambda: type("U", (), {"hex": fixed_uuid})())

    fake_file = object()

    path_file = await files_service.upload_image(fake_file, "test.png")

    assert path_file == f"/fakes/dir/test_{fixed_uuid}.png"
    assert fake_storage.saved[0][1] == f"test_{fixed_uuid}.png"
