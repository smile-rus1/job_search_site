from __future__ import annotations
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, DateTime, func, Text, UniqueConstraint
from src.infrastructure.db.models.base import Base
from src.core.enums import StatusRespond
from src.infrastructure.enums_db import StatusRespondEnumDB, ActorTypeEnumDB


class RespondOnVacancyDB(Base):
    __tablename__ = "responses_vacancy"

    response_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    responder_type: Mapped[ActorTypeEnumDB] = mapped_column(ActorTypeEnumDB, nullable=False)
    status: Mapped[StatusRespondEnumDB] = mapped_column(
        StatusRespondEnumDB,
        default=StatusRespond.SENT
    )
    response_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())

    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancies.vacancy_id"), nullable=False)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.resume_id"), nullable=False)

    vacancy: Mapped["VacancyDB"] = relationship(back_populates="responded")  # type: ignore
    resume: Mapped["ResumeDB"] = relationship(back_populates="responded")  # type: ignore
    messages: Mapped[list["ResponseMessageDB"]] = relationship(
        back_populates="response", cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("vacancy_id", "resume_id", name="uq_vacancy_id_resume"),
    )


class ResponseMessageDB(Base):
    __tablename__ = "response_messages"

    message_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sender_type: Mapped[ActorTypeEnumDB] = mapped_column(ActorTypeEnumDB, nullable=False)
    message_text: Mapped[str] = mapped_column(Text, nullable=True)
    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())

    response_id: Mapped[int] = mapped_column(
        ForeignKey("responses_vacancy.response_id", ondelete="CASCADE"), nullable=False
    )
    response: Mapped["RespondOnVacancyDB"] = relationship(back_populates="messages")
