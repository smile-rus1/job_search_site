from src.dto.db.applicant.applicant import BaseApplicantDTODAO


class IApplicantDAO:
    async def create_applicant(self, applicant: BaseApplicantDTODAO) -> BaseApplicantDTODAO:
        raise NotImplementedError

    async def update_applicant(self, applicant: BaseApplicantDTODAO) -> None:
        raise NotImplementedError

    async def get_applicant_by_id(self, applicant_id: int) -> BaseApplicantDTODAO:
        raise NotImplementedError
