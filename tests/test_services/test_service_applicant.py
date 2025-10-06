from datetime import date

import pytest

from src.dto.services.applicant.applicant import UpdateApplicantDTO
from src.infrastructure.hasher import Hasher
from src.services.applicant.applicant import ApplicantService
from test_services.fakes.transaction_manager import FakeTransactionalManager


@pytest.mark.asyncio
async def test_create_applicant(applicant_data_dto):
    uow = FakeTransactionalManager()
    hasher = Hasher()
    applicant_service = ApplicantService(uow, hasher)

    applicant = await applicant_service.create_applicant(applicant_data_dto)

    assert applicant is not None
    assert uow.committed


@pytest.mark.asyncio
async def test_update_applicant(applicant_data_dto):
    uow = FakeTransactionalManager()
    hasher = Hasher()
    applicant_service = ApplicantService(uow, hasher)

    await uow.applicant_dao.create_applicant(applicant_data_dto)

    update_applicant_dt = UpdateApplicantDTO(
        user_id=1,
        email="example@mail.ru",
        address="new_address"
    )
    await applicant_service.update_applicant(update_applicant_dt)

    applicant = await uow.applicant_dao.get_applicant_by_id(1)

    assert applicant is not None
    assert applicant.address == "new_address"
    assert applicant.date_born == date(1999, 11, 25)


@pytest.mark.asyncio
async def test_get_applicant_by_id(applicant_data_dto):
    uow = FakeTransactionalManager()
    hasher = Hasher()
    applicant_service = ApplicantService(uow, hasher)

    await uow.applicant_dao.create_applicant(applicant_data_dto)

    applicant = await applicant_service.get_applicant(1)

    assert applicant is not None
    assert applicant.user.email == "example@mail.ru"
