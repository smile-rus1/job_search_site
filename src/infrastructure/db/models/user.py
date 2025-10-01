from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func, Boolean

from src.infrastructure.db.models.base import Base


class UserDB(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean(), default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=func.now(), onupdate=func.now())

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    image_url: Mapped[str] = mapped_column(String(255), nullable=True)
    is_confirmed: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=True)

    type: Mapped[str] = mapped_column(String(20), nullable=False)

    applicants = relationship(
        "ApplicantDB",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    companies = relationship(
        "CompanyDB",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    # для того чтобы понимать тип наследника
    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": type,
        "with_polymorphic": "*"
    }
