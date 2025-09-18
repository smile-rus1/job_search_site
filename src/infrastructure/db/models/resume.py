from __future__ import annotations
from datetime import datetime, date

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Boolean, Integer, ForeignKey, Date, Enum, Numeric, DateTime, func
from sqlalchemy.dialects.postgresql import ARRAY
from src.infrastructure.db.models.base import Base
from src.infrastructure.enums import EmploymentType, Currency


class ResumeDB(Base):
    __tablename__ = "resumes"

    resume_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name_resume: Mapped[str] = mapped_column(String(20), nullable=False)
    key_skills: Mapped[str] = mapped_column(Text(), nullable=True)
    profession: Mapped[str] = mapped_column(String(30), nullable=False)
    salary_min: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    salary_max: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    salary_currency: Mapped[Currency] = mapped_column(Enum(Currency), nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    location: Mapped[str] = mapped_column(String(150), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        default=func.now(),
        onupdate=func.now()
    )

    applicant_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("applicants.applicant_id", ondelete='CASCADE')
    )
    applicant: Mapped["ApplicantDB"] = relationship(back_populates="resumes")  # type: ignore

    type_of_employment: Mapped[list[EmploymentType]] = mapped_column(
        ARRAY(Enum(EmploymentType, name="employment_type")),
        nullable=True
    )

    work_experiences: Mapped[list["WorkExperienceDB"]] = relationship(
        back_populates="resume",
        cascade="all, delete-orphan"
    )


class WorkExperienceDB(Base):
    __tablename__ = "work_experiences"

    work_experience_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company_name: Mapped[str] = mapped_column(String(25), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=True)
    description_work: Mapped[str] = mapped_column(Text(), nullable=True)

    resume_id: Mapped[int] = mapped_column(
        ForeignKey("resumes.resume_id", ondelete="CASCADE"),
        nullable=False
    )
    resume: Mapped["ResumeDB"] = relationship(back_populates="work_experiences")
