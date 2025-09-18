from src.dto.db.resume.resume import CreateResumeDTODAO, BaseResumeDTODAO, UpdateResumeDTODAO, ResumeDTODAO


class IResumeDAO:
    async def create_resume(self, resume: CreateResumeDTODAO) -> BaseResumeDTODAO:
        raise NotImplementedError

    async def update_resume(self, resume: UpdateResumeDTODAO) -> None:
        raise NotImplementedError

    async def get_resume_by_id(self, resume_id: int) -> ResumeDTODAO:
        raise NotImplementedError

    async def delete_resume(self, resume_id: int, applicant_id: int) -> None:
        raise NotImplementedError

    async def search_resumes(self, search_dto):
        raise NotImplementedError
