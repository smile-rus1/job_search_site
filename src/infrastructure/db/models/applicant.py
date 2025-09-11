from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Enum, Boolean, Integer, ForeignKey

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
    address: Mapped[str] = mapped_column(String(100), nullable=True)
    gender: Mapped[str] = mapped_column(Enum(GenderEnum), nullable=False)
    level_education: Mapped[str] = mapped_column(Enum(EducationEnum), nullable=True)
    is_confirmed: Mapped[bool] = mapped_column(Boolean(), default=False)

    __mapper_args__ = {
        "polymorphic_identity": "applicant"
    }
