from src.dto.db.work_experience.work_experience import CreateWorkExperienceDTODAO, WorkExperienceDTODAO, \
    UpdateWorkExperienceDTODAO


class IWorkExperienceDAO:
    async def create_work_experience(self, work_experience: CreateWorkExperienceDTODAO) -> WorkExperienceDTODAO:
        raise NotImplementedError

    async def update_work_experience(self, work_experience: UpdateWorkExperienceDTODAO) -> None:
        raise NotImplementedError

    async def delete_work_experience(self, applicant_id: int, resume_id: int, work_experience_id: int) -> None:
        raise NotImplementedError

    async def get_work_experience_by_id(self, work_experience: int) -> WorkExperienceDTODAO:
        raise NotImplementedError
