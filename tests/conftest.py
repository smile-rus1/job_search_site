from datetime import date

import pytest

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import StaticPool

import redis.asyncio as redis

from src.dto.db.applicant.applicant import BaseApplicantDTODAO
from src.dto.db.company.company import BaseCompanyDTODAO
from src.dto.db.user.user import BaseUserDTODAO
from src.core.enums import GenderEnum, EducationEnum
from src.infrastructure.redis_db.redis_db import RedisDB

Base = declarative_base()


@pytest.fixture
async def async_session():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    maker = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with maker() as session:
        yield session


@pytest.fixture(scope="session")
async def redis_client():
    pool = redis.ConnectionPool.from_url(
        "redis://localhost:6379",
        decode_responses=True,
        max_connections=20,
    )
    return redis.Redis(connection_pool=pool)


@pytest.fixture
async def redis_db(redis_client):
    db = RedisDB(await redis_client)
    return db


@pytest.fixture()
def applicant_data_dto():
    return BaseApplicantDTODAO(
        user=BaseUserDTODAO(
            user_id=1,
            email="example@mail.ru",
            first_name="example1",
            last_name="example1_last",
            password="123456789",
            phone_number="+37521312",
            image_url="new.png",
        ),
        gender=GenderEnum.MALE.value,
        description_applicant="some description",
        address="some address",
        level_education=EducationEnum.WITHOUT_EDUCATION.value,
        date_born=date(1999, 11, 25),
    )


@pytest.fixture()
def company_data_dto():
    return BaseCompanyDTODAO(
        user=BaseUserDTODAO(
            user_id=2,
            email="example_company@mail.ru",
            first_name="example_company",
            last_name="example_company_last",
            password="123456789",
            phone_number="+37521312",
            image_url="new.png",
        ),
        company_name="example_company",
        description_company="just description",
        address="address"
    )
