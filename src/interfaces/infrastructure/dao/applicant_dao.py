from src.dto.db.applicant.applicant import CreateApplicantDTODAO, ApplicantOutDTODAO, UpdateApplicantDTODAO, \
    ApplicantDTODAO


class IApplicantDAO:
    async def create_applicant(self, applicant: CreateApplicantDTODAO) -> ApplicantOutDTODAO:
        raise NotImplementedError

    async def update_applicant(self, applicant: UpdateApplicantDTODAO) -> None:
        raise NotImplementedError

    async def get_applicant_by_id(self, applicant_id: int) -> ApplicantDTODAO:
        raise NotImplementedError
