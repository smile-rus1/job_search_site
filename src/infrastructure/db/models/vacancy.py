from __future__ import annotations
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Boolean, Integer, ForeignKey, Numeric, DateTime, func, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from src.infrastructure.db.models.base import Base
from src.infrastructure.enums import Currency
from src.infrastructure.enums_db import (
    VacancyDurationEnumDB,
    CurrencyEnumDB,
    EmploymentTypeEnumDB,
    WorkScheduleTypeEnumDB
)


class VacancyDB(Base):
    __tablename__ = "vacancies"

    vacancy_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(Text(), nullable=True)
    location: Mapped[str] = mapped_column(String(100), nullable=True)
    key_skills: Mapped[str] = mapped_column(Text(), nullable=True)
    profession: Mapped[str] = mapped_column(String(30), nullable=False)
    salary_min: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    salary_max: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    salary_currency: Mapped[CurrencyEnumDB] = mapped_column(CurrencyEnumDB, nullable=True)
    experience_start: Mapped[int] = mapped_column(Integer, nullable=True)
    experience_end: Mapped[int] = mapped_column(Integer, nullable=True)

    type_of_employment: Mapped[list[EmploymentTypeEnumDB]] = mapped_column(
        ARRAY(EmploymentTypeEnumDB),
        nullable=True
    )
    type_work_schedule: Mapped[list[WorkScheduleTypeEnumDB]] = mapped_column(
        ARRAY(WorkScheduleTypeEnumDB),
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        default=func.now(),
        onupdate=func.now()
    )
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    is_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)

    company_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("companies.company_id", ondelete='CASCADE'),
    )
    company: Mapped["CompanyDB"] = relationship(back_populates="vacancies")  # type: ignore
    access: Mapped["VacancyAccessDB"] = relationship(back_populates="vacancy", uselist=False)

    vacancy_type_id: Mapped[int] = mapped_column(
        ForeignKey("vacancy_types.vacancy_types_id"),
        nullable=False
    )
    vacancy_type: Mapped["VacancyTypeDB"] = relationship(back_populates="vacancy")
    liked: Mapped["LikedVacancy"] = relationship(back_populates="vacancy")


class VacancyAccessDB(Base):
    __tablename__ = "vacancy_access"

    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey("vacancies.vacancy_id", ondelete="CASCADE"),
        primary_key=True
    )
    vacancy: Mapped["VacancyDB"] = relationship(back_populates="access", uselist=False)
    duration: Mapped[VacancyDurationEnumDB] = mapped_column(VacancyDurationEnumDB)
    start_date: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class VacancyTypeDB(Base):
    __tablename__ = "vacancy_types"

    vacancy_types_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)  # free, paid, premium...

    prices: Mapped[list["VacancyTypePriceDB"]] = relationship(back_populates="vacancy_type")
    vacancy: Mapped[list["VacancyDB"]] = relationship(back_populates="vacancy_type")


class VacancyTypePriceDB(Base):
    __tablename__ = "vacancy_type_prices"

    vacancy_type_price_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    duration: Mapped[VacancyDurationEnumDB] = mapped_column(VacancyDurationEnumDB)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[CurrencyEnumDB] = mapped_column(CurrencyEnumDB, default=Currency.BYN, nullable=False)

    vacancy_type_id: Mapped[int] = mapped_column(
        ForeignKey("vacancy_types.vacancy_types_id", ondelete="CASCADE"),
        nullable=False
    )
    vacancy_type: Mapped["VacancyTypeDB"] = relationship(back_populates="prices")


class LikedVacancy(Base):
    __tablename__ = "liked_vacancies"

    liked_vacancies_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey("vacancies.vacancy_id", ondelete="CASCADE")
    )
    applicant_id: Mapped[int] = mapped_column(
        ForeignKey("applicants.applicant_id", ondelete="CASCADE")
    )

    vacancy: Mapped["VacancyDB"] = relationship(back_populates="liked")
    applicant: Mapped["ApplicantDB"] = relationship(back_populates="liked")  # type: ignore

    __table_args__ = (
        UniqueConstraint("applicant_id", "vacancy_id", name="uq_applicant_id_vacancy"),
    )
