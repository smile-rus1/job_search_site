import pytest

from src.dto.services.company.company import UpdateCompanyDTO, SearchDTO
from src.infrastructure.hasher import Hasher
from src.services.company.company import CompanyService
from test_services.fakes.transaction_manager import FakeTransactionalManager


@pytest.mark.asyncio
async def test_create_company(company_data_dto):
    uow = FakeTransactionalManager()
    hasher = Hasher()
    company_service = CompanyService(uow, hasher)

    company = await company_service.create_company(company_data_dto)

    assert company is not None
    assert uow.committed


@pytest.mark.asyncio
async def test_update_company(company_data_dto):
    uow = FakeTransactionalManager()
    hasher = Hasher()
    company_service = CompanyService(uow, hasher)

    await uow.company_dao.create_company(company_data_dto)

    update_company = UpdateCompanyDTO(
        user_id=2,
        email="example_company@mail.ru",
        address="NEW_ADDRESS"
    )

    await company_service.update_company(update_company)

    company = await uow.company_dao.get_company_by_id(2)
    assert company is not None
    assert company.address == "NEW_ADDRESS"
    assert company.company_name == "example_company"


@pytest.mark.asyncio
async def test_get_company_by_id(company_data_dto):
    uow = FakeTransactionalManager()
    hasher = Hasher()
    company_service = CompanyService(uow, hasher)

    await uow.company_dao.create_company(company_data_dto)

    company = await company_service.get_company(2)

    assert company is not None
    assert company.company_name == "example_company"


@pytest.mark.asyncio
async def test_search_company(company_data_dto):
    uow = FakeTransactionalManager()
    hasher = Hasher()
    company_service = CompanyService(uow, hasher)

    await uow.company_dao.create_company(company_data_dto)

    search_dto = SearchDTO(
        offset=0,
        limit=10,
        company_name="example_company"
    )

    companies = await company_service.search_companies(search_dto)

    assert len(companies) == 1
