from __future__ import annotations

from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Enum, Boolean, Integer, ForeignKey, Date

from src.infrastructure.db.models import UserDB
from src.infrastructure.enums import GenderEnum, EducationEnum


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
    gender: Mapped[str] = mapped_column(Enum(GenderEnum), nullable=False)
    level_education: Mapped[str] = mapped_column(Enum(EducationEnum), nullable=True)
    is_confirmed: Mapped[bool] = mapped_column(Boolean(), default=False)

    resumes: Mapped[list["ResumeDB"]] = relationship(  # type: ignore
        back_populates="applicant",
        cascade="all, delete-orphan"
    )

    __mapper_args__ = {
        "polymorphic_identity": "applicant"
    }
