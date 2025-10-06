from dataclasses import asdict

from src.dto.db.applicant.applicant import BaseApplicantDTODAO
from src.interfaces.infrastructure.dao.applicant_dao import IApplicantDAO


class FakeApplicantDAO(IApplicantDAO):
    def __init__(self):
        self._storage = []

    async def create_applicant(self, applicant: BaseApplicantDTODAO):
        self._storage.append(applicant)
        return applicant

    async def update_applicant(self, applicant: BaseApplicantDTODAO) -> None:
        applicant_dto: BaseApplicantDTODAO = next(
            ap for ap in self._storage if ap.user.user_id == applicant.user.user_id
        )
        data = asdict(applicant)
        user = {k: v for k, v in data.pop("user").items() if v is not None and k not in {"user_id", "email"}}
        applicant_fields = {k: v for k, v in data.items() if v is not None}

        if user:
            applicant_fields["user"] = user

        for k, v in applicant_fields.items():
            setattr(applicant_dto, k, v)

    async def get_applicant_by_id(self, applicant_id):
        return next(
            (applicant for applicant in self._storage if applicant.user.user_id == applicant_id),
            None
        )
