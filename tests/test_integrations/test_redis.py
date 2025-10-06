import pytest


@pytest.mark.asyncio
async def test_set_get(redis_db):
    redis_db = await redis_db

    await redis_db.set("simple", "code", expire=10)

    value = await redis_db.get("simple")
    assert value == "code"


@pytest.mark.asyncio
async def test_exists(redis_db):
    redis_db = await redis_db

    await redis_db.set("x", "1")

    assert await redis_db.exists("x")
    assert not await redis_db.exists("y")
