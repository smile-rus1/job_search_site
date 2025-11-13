from dataclasses import asdict

from loguru import logger
from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import IntegrityError

from src.dto.db.work_experience.work_experience import BaseWorkExperienceDTODAO
from src.exceptions.infrascructure import BaseWorkExperiencesException
from src.exceptions.infrascructure.work_experiences.work_experiences import WorkExperiences, WorkExperiencesNotFoundByID
from src.infrastructure.db.models import WorkExperienceDB, ResumeDB
from src.interfaces.infrastructure.dao.workexperience_dao import IWorkExperienceDAO
from src.interfaces.infrastructure.sqlalchemy_dao import SqlAlchemyDAO


class WorkExperienceDAO(SqlAlchemyDAO, IWorkExperienceDAO):
    async def create_work_experience(self, work_experience: BaseWorkExperienceDTODAO) -> BaseWorkExperienceDTODAO:
        sub_sql = (
            select(ResumeDB.resume_id)
            .where(
                ResumeDB.resume_id == work_experience.resume_id
            )
            .scalar_subquery()
        )
        sql = (
            insert(WorkExperienceDB)
            .values(
                company_name=work_experience.company_name,
                start_date=work_experience.start_date,
                end_date=work_experience.end_date,
                description_work=work_experience.description_work,
                resume_id=sub_sql
            )
            .returning(WorkExperienceDB)
        )

        try:
            res = (await self._session.execute(sql)).scalar_one()

        except IntegrityError as exc:
            logger.bind(
                app_name=f"{WorkExperienceDAO.__name__} in {self.create_work_experience.__name__}"
            ).error(f"WITH DATA {work_experience}\nMESSAGE: {exc}")
            raise self._error_parser()

        return BaseWorkExperienceDTODAO(
            resume_id=res.resume_id,
            work_experience_id=res.work_experience_id,
            description_work=res.description_work,
            company_name=res.company_name,
            start_date=res.start_date,
            end_date=res.end_date,
        )

    async def update_work_experience(self, work_experience: BaseWorkExperienceDTODAO) -> None:
        data = asdict(work_experience)
        print(data)
        work_experience_fields = {
            k: v for k, v in data.items() if v is not None and k not in {"work_experience_id"}
        }

        sub_sql = (
            select(ResumeDB.resume_id)
            .where(
                ResumeDB.resume_id == work_experience.resume_id
            )
            .scalar_subquery()
        )

        sql = (
            update(WorkExperienceDB)
            .where(
                WorkExperienceDB.work_experience_id == work_experience.work_experience_id,
                WorkExperienceDB.resume_id == sub_sql
            )
            .values(**work_experience_fields)
        )

        try:
            await self._session.execute(sql)

        except IntegrityError as exc:
            logger.bind(
                app_name=f"{WorkExperienceDAO.__name__} in {self.update_work_experience.__name__}"
            ).error(f"WITH DATA {work_experience}\nMESSAGE: {exc}")
            raise self._error_parser()

    async def delete_work_experience(self, applicant_id: int, resume_id: int, work_experience_id: int) -> None:
        sub_sql = (
            select(ResumeDB.resume_id)
            .where(
                ResumeDB.applicant_id == applicant_id,
                ResumeDB.resume_id == resume_id
            )
            .scalar_subquery()
        )

        sql = (
            delete(WorkExperienceDB)
            .where(
                WorkExperienceDB.work_experience_id == work_experience_id,
                WorkExperienceDB.resume_id == sub_sql
            )
        )
        await self._session.execute(sql)

    async def get_work_experience_by_id(self, work_experience_id: int) -> BaseWorkExperienceDTODAO:
        sql = (
            select(
                WorkExperienceDB.work_experience_id,
                WorkExperienceDB.description_work,
                WorkExperienceDB.company_name,
                WorkExperienceDB.start_date,
                WorkExperienceDB.end_date,
                WorkExperienceDB.resume_id
            )
            .where(WorkExperienceDB.work_experience_id == work_experience_id)
        )
        res = (await self._session.execute(sql)).first()  # ☺

        if res is None:
            raise WorkExperiencesNotFoundByID(work_experience_id)

        return BaseWorkExperienceDTODAO(
            resume_id=res.resume_id,
            work_experience_id=res.work_experience_id,
            description_work=res.description_work,
            company_name=res.company_name,
            start_date=res.start_date,
            end_date=res.end_date
        )

    @staticmethod
    def _error_parser() -> BaseWorkExperiencesException:
        return WorkExperiences()
