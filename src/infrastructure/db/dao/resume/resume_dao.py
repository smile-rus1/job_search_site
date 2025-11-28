from dataclasses import asdict
from datetime import date

from loguru import logger
from sqlalchemy import insert, select, update, delete, Select, func, or_, and_, asc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only, joinedload, contains_eager

from src.dto.db.applicant.applicant import BaseApplicantDTODAO
from src.dto.db.resume.resume import (
    BaseResumeDTODAO,
    SearchDTODAO
)
from src.dto.db.user.user import BaseUserDTODAO
from src.dto.db.work_experience.work_experience import BaseWorkExperienceDTODAO
from src.exceptions.base import BaseExceptions
from src.exceptions.infrascructure.resume.resume import ResumeException, ResumeNotFoundByID
from src.infrastructure.db.models import ResumeDB, ApplicantDB, WorkExperienceDB, UserDB
from src.core.enums import GenderEnum, EmploymentType, Currency
from src.interfaces.infrastructure.dao.resume_dao import IResumeDAO
from src.interfaces.infrastructure.sqlalchemy_dao import SqlAlchemyDAO


class ResumeDAO(SqlAlchemyDAO, IResumeDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self._query_builder = ResumeQueryBuilder()

    async def create_resume(self, resume: BaseResumeDTODAO) -> BaseResumeDTODAO:
        sql = (
            insert(ResumeDB)
            .values(
                name_resume=resume.name_resume,
                applicant_id=resume.applicant.user.user_id,
                key_skills=resume.key_skills,
                profession=resume.profession,
                salary_min=resume.salary_min,
                salary_max=resume.salary_max,
                salary_currency=resume.salary_currency,
                location=resume.location,
                type_of_employment=resume.type_of_employment
            ).returning(ResumeDB)
        )

        try:
            result = await self._session.execute(sql)

        except IntegrityError as exc:
            logger.bind(
                app_name=f"{ResumeDAO.__name__} in {self.create_resume.__name__}"
            ).error(f"WITH DATA {resume}\nMESSAGE: {exc}")
            raise self._error_parser()

        model = result.scalar_one()
        return BaseResumeDTODAO(
            applicant=BaseApplicantDTODAO(
                user=BaseUserDTODAO(
                    user_id=resume.applicant.user.user_id
                )
            ),
            resume_id=model.resume_id,
            name_resume=model.name_resume,
            key_skills=model.key_skills,
            profession=model.profession,
            salary_min=model.salary_min,
            salary_max=model.salary_max,
            salary_currency=model.salary_currency,
            is_published=model.is_published,
            location=model.location,
            updated_at=model.updated_at,
            type_of_employment=model.type_of_employment,
        )

    async def update_resume(self, resume: BaseResumeDTODAO) -> None:
        data = asdict(resume)
        resume_fields = {k: v for k, v in data.items() if v is not None and k not in {"resume_id"}}

        sql = (
            update(ResumeDB)
            .where(
                ResumeDB.resume_id == resume.resume_id,
                ResumeDB.applicant_id == resume.applicant.user.user_id
            )
            .values(**resume_fields)
        )

        try:
            await self._session.execute(sql)

        except IntegrityError as exc:
            logger.bind(
                app_name=f"{ResumeDAO.__name__} in {self.update_resume.__name__}"
            ).error(f"WITH DATA {resume}\nMESSAGE: {exc}")
            raise self._error_parser()

    async def get_resume_by_id(self, resume_id: int) -> BaseResumeDTODAO:
        sql = (
            select(ResumeDB)
            .options(
                joinedload(ResumeDB.applicant)
                .joinedload(ApplicantDB.applicants)  # можно с selectinload, но там N + 1 будет
                .load_only(
                    UserDB.email,
                    UserDB.first_name,
                    UserDB.last_name,
                    UserDB.phone_number,
                    UserDB.image_url
                ),
                joinedload(ResumeDB.applicant)
                .load_only(
                    ApplicantDB.applicant_id,
                    ApplicantDB.gender,
                    ApplicantDB.description_applicant,
                    ApplicantDB.address,
                    ApplicantDB.is_confirmed,
                    ApplicantDB.level_education
                ),
                joinedload(ResumeDB.work_experiences)
                .load_only(
                    WorkExperienceDB.work_experience_id,
                    WorkExperienceDB.resume_id,
                    WorkExperienceDB.company_name,
                    WorkExperienceDB.start_date,
                    WorkExperienceDB.end_date,
                    WorkExperienceDB.description_work
                ),
                load_only(
                    ResumeDB.resume_id,
                    ResumeDB.name_resume,
                    ResumeDB.profession,
                    ResumeDB.key_skills,
                    ResumeDB.salary_min,
                    ResumeDB.salary_max,
                    ResumeDB.salary_currency,
                    ResumeDB.location,
                    ResumeDB.type_of_employment
                )
            )
            .where(ResumeDB.resume_id == resume_id)
        )

        result = await self._session.execute(sql)
        resume = result.unique().scalars().one_or_none()

        if resume is None:
            raise ResumeNotFoundByID(resume_id)

        return BaseResumeDTODAO(
            resume_id=resume.resume_id,
            name_resume=resume.name_resume,
            profession=resume.profession,
            key_skills=resume.key_skills,
            salary_min=resume.salary_min,
            salary_max=resume.salary_max,
            salary_currency=resume.salary_currency,
            location=resume.location,
            type_of_employment=resume.type_of_employment,
            applicant=BaseApplicantDTODAO(
                gender=resume.applicant.gender,
                description_applicant=resume.applicant.description_applicant,
                address=resume.applicant.address,
                level_education=resume.applicant.level_education,
                user=BaseUserDTODAO(
                    user_id=resume.applicant.applicant_id,
                    email=resume.applicant.email,
                    first_name=resume.applicant.first_name,
                    last_name=resume.applicant.last_name,
                    phone_number=resume.applicant.phone_number,
                    image_url=resume.applicant.image_url,
                    is_confirmed=resume.applicant.is_confirmed
                )
            ),
            work_experiences=[
                BaseWorkExperienceDTODAO(
                    work_experience_id=we.work_experience_id,
                    resume_id=we.resume_id,
                    company_name=we.company_name,
                    start_date=we.start_date,
                    end_date=we.end_date,
                    description_work=we.description_work
                )
                for we in resume.work_experiences
            ]
        )

    async def delete_resume(self, resume_id: int, applicant_id: int) -> None:
        sql = (
            delete(ResumeDB)
            .where(
                ResumeDB.resume_id == resume_id,
                ResumeDB.applicant_id == applicant_id
            )
        )
        await self._session.execute(sql)

    async def search_resumes(self, search_dto: SearchDTODAO) -> list[BaseResumeDTODAO]:
        sql = self._query_builder.get_query(
            name_resume=search_dto.name_resume,
            location=search_dto.location,
            profession=search_dto.profession,
            gender=search_dto.gender,
            type_of_employment=search_dto.type_of_employment,
            salary_min=search_dto.salary_min,
            salary_max=search_dto.salary_max,
            salary_currency=search_dto.salary_currency,
            min_age=search_dto.min_age,
            max_age=search_dto.max_age,
            start_experience_years=search_dto.start_experience_years,
            end_experience_years=search_dto.end_experience_years,
            offset=search_dto.offset,
            limit=search_dto.limit
        )

        result = await self._session.execute(sql)
        models = result.unique().all()

        dtos: list[BaseResumeDTODAO] = []
        for resume, total_months in models:
            applicant = resume.applicant  # That ApplicatDB joined with UserDB
            dto = BaseResumeDTODAO(
                resume_id=resume.resume_id,
                name_resume=resume.name_resume,
                profession=resume.profession,
                key_skills=resume.key_skills,
                salary_min=resume.salary_min,
                salary_max=resume.salary_max,
                salary_currency=resume.salary_currency,
                location=resume.location,
                type_of_employment=resume.type_of_employment,
                total_months=total_months,
                applicant=BaseApplicantDTODAO(
                    description_applicant=applicant.description_applicant,
                    address=applicant.address,
                    level_education=applicant.level_education,
                    gender=applicant.gender,
                    date_born=applicant.date_born,
                    user=BaseUserDTODAO(
                        user_id=applicant.applicant_id,
                        email=applicant.email,
                        first_name=applicant.first_name,
                        last_name=applicant.last_name,
                        phone_number=applicant.phone_number,
                        image_url=applicant.image_url,
                        is_confirmed=applicant.is_confirmed
                    )
                ),
                work_experiences=[
                    BaseWorkExperienceDTODAO(
                        work_experience_id=w.work_experience_id,
                        resume_id=w.resume_id,
                        company_name=w.company_name,
                        start_date=w.start_date,
                        end_date=w.end_date,
                        description_work=w.description_work,
                    )
                    for w in resume.work_experiences
                ]
            )
            dtos.append(dto)
        return dtos

    @staticmethod
    def _error_parser() -> BaseExceptions:
        return ResumeException()


class ResumeQueryBuilder:
    def __init__(self):
        self._query = None

    def get_query(
            self,
            name_resume: str | None,
            location: str | None,
            profession: str | None,
            gender: GenderEnum | None,
            type_of_employment: EmploymentType | None,
            salary_min: float | None,
            salary_max: float | None,
            salary_currency: Currency | None,
            min_age: int | None,
            max_age: int | None,
            start_experience_years: int | None,
            end_experience_years: int | None,
            offset: int = 0,
            limit: int = 25
    ) -> Select:
        return (
            self._select(offset, limit)
            ._with_experience_between(start_experience_years, end_experience_years)
            ._with_resume_name(name_resume)
            ._with_gender(gender)
            ._with_location(location)
            ._with_profession(profession)
            ._with_type_of_employment(type_of_employment)
            ._with_salary_and_currency(salary_min, salary_max, salary_currency)
            ._with_total_age(min_age, max_age)
            ._build()
        )

    def _select(self, offset: int = 0, limit: int = 0):
        end_date = func.coalesce(WorkExperienceDB.end_date, func.current_date())
        months_diff = (
                (func.extract("year", end_date) - func.extract("year", WorkExperienceDB.start_date)) * 12 +
                (func.extract("month", end_date) - func.extract("month", WorkExperienceDB.start_date))
        )

        self._work_sum_subq = (  # Calculated sum of months and prepared as subquery
            select(
                WorkExperienceDB.resume_id.label("resume_id"),
                func.sum(months_diff).label("total_months")
            )
            .group_by(WorkExperienceDB.resume_id)
            .subquery()
        )

        self._query = (
            select(ResumeDB, self._work_sum_subq.c.total_months)
            .outerjoin(self._work_sum_subq, self._work_sum_subq.c.resume_id == ResumeDB.resume_id)
            .join(ResumeDB.applicant)
            .options(
                contains_eager(ResumeDB.applicant)
                .load_only(
                    ApplicantDB.applicant_id,
                    ApplicantDB.gender,
                    ApplicantDB.address,
                    ApplicantDB.level_education,
                    ApplicantDB.date_born,
                    ApplicantDB.email,
                    ApplicantDB.first_name,
                    ApplicantDB.last_name,
                    ApplicantDB.phone_number,
                    ApplicantDB.description_applicant,
                    ApplicantDB.image_url,
                    ApplicantDB.is_confirmed,
                ),
                joinedload(ResumeDB.work_experiences).load_only(
                    WorkExperienceDB.work_experience_id,
                    WorkExperienceDB.resume_id,
                    WorkExperienceDB.company_name,
                    WorkExperienceDB.start_date,
                    WorkExperienceDB.end_date,
                    WorkExperienceDB.description_work,
                ),
                load_only(
                    ResumeDB.resume_id,
                    ResumeDB.name_resume,
                    ResumeDB.profession,
                    ResumeDB.key_skills,
                    ResumeDB.salary_min,
                    ResumeDB.salary_max,
                    ResumeDB.salary_currency,
                    ResumeDB.location,
                    ResumeDB.type_of_employment,
                ),
            )
            .order_by(asc(ResumeDB.name_resume))
            .limit(limit)
            .offset(offset)
        )
        return self

    def _with_resume_name(self, name_resume: str | None):
        if name_resume is not None:
            self._query = self._query.where(ResumeDB.name_resume.like(f"%{name_resume}%"))
        return self

    def _with_location(self, location: str | None):
        if location is not None:
            self._query = self._query.where(ResumeDB.location.like(f"%{location}%"))
        return self

    def _with_gender(self, gender: GenderEnum | None):
        if gender is not None:
            self._query = (
                self._query
                .join(ResumeDB.applicant)
                .where(ApplicantDB.gender == gender)
            )
        return self

    def _with_profession(self, profession: str | None):
        if profession is not None:
            self._query = self._query.where(ResumeDB.profession.like(f"%{profession}%"))
        return self

    def _with_type_of_employment(self, type_of_employment: list[EmploymentType] | None):
        if type_of_employment is not None:
            type_of_employment_enum = [EmploymentType(x) for x in type_of_employment]
            self._query = self._query.where(
                ResumeDB.type_of_employment.contains(type_of_employment_enum)
            )
        return self

    def _with_salary_and_currency(
            self,
            salary_min: float | None,
            salary_max: float | None,
            salary_currency: Currency | None
    ):
        if salary_currency is not None:
            self._query = self._query.where(
                ResumeDB.salary_currency == salary_currency.value
            )

        if salary_min is not None and salary_max is not None:
            self._query = self._query.where(
                and_(
                    or_(ResumeDB.salary_min.is_(None), ResumeDB.salary_min <= salary_max),
                    or_(ResumeDB.salary_max.is_(None), ResumeDB.salary_max >= salary_min),
                )
            )
        elif salary_min is not None:
            self._query = self._query.where(
                or_(ResumeDB.salary_max.is_(None), ResumeDB.salary_max >= salary_min)
            )
        elif salary_max is not None:
            self._query = self._query.where(
                or_(ResumeDB.salary_min.is_(None), ResumeDB.salary_min <= salary_max)
            )

        return self

    def _with_total_age(self, min_age: int | None, max_age: int | None):
        today = date.today()
        if min_age is not None and max_age is not None:
            latest_birth_date = today.replace(year=today.year - min_age)
            earliest_birth_date = today.replace(year=today.year - max_age)
            self._query = self._query.where(
                and_(
                    ResumeDB.applicant.has(ApplicantDB.date_born.is_not(None)),
                    ResumeDB.applicant.has(ApplicantDB.date_born <= latest_birth_date),
                    ResumeDB.applicant.has(ApplicantDB.date_born >= earliest_birth_date),
                )
            )
        elif min_age is not None:
            latest_birth_date = today.replace(year=today.year - min_age)
            self._query = self._query.where(
                ResumeDB.applicant.has(
                    and_(
                        ApplicantDB.date_born.is_not(None),
                        ApplicantDB.date_born <= latest_birth_date
                    )
                )
            )
        elif max_age is not None:
            earliest_birth_date = today.replace(year=today.year - max_age)
            self._query = self._query.where(
                ResumeDB.applicant.has(
                    and_(
                        ApplicantDB.date_born.is_not(None),
                        ApplicantDB.date_born >= earliest_birth_date
                    )
                )
            )

        return self

    def _with_experience_between(
            self,
            start_experience: int | None = None,
            end_experience: int | None = None,
    ):
        if start_experience is None and end_experience is None:
            return self

        start_months = None if start_experience is None else int(start_experience) * 12
        end_months = None if end_experience is None else int(end_experience) * 12

        #  if start_months and end_months are swapped
        if start_months is not None and end_months is not None and start_months > end_months:
            start_months, end_months = end_months, start_months

        total_months = func.coalesce(self._work_sum_subq.c.total_months, 0)  # count no experience as 0 months

        conds = []
        if start_months is not None:
            conds.append(total_months >= start_months)
        if end_months is not None:
            conds.append(total_months <= end_months)

        if conds:
            self._query = self._query.where(*conds)

        return self

    def _build(self):
        return self._query
