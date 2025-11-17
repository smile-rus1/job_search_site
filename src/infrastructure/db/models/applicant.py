from __future__ import annotations

from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer, ForeignKey, Date

from src.infrastructure.db.models import UserDB
from src.infrastructure.enums_db import GenderEnumDB, EducationEnumDB


class ApplicantDB(UserDB):
    __tablename__ = "applicants"

    applicant_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        primary_key=True
    )
    description_applicant: Mapped[str] = mapped_column(Text(), nullable=True)
    date_born: Mapped[date] = mapped_column(Date, nullable=True)
    address: Mapped[str] = mapped_column(String(100), nullable=True)
    gender: Mapped[str] = mapped_column(GenderEnumDB, nullable=False)
    level_education: Mapped[str] = mapped_column(EducationEnumDB, nullable=True)

    resumes: Mapped[list["ResumeDB"]] = relationship(  # type: ignore
        back_populates="applicant",
        cascade="all, delete-orphan"
    )
    liked: Mapped["LikedVacancy"] = relationship(  # type: ignore
        back_populates="applicant",
        cascade="all, delete-orphan"
    )

    __mapper_args__ = {
        "polymorphic_identity": "applicant"
    }
