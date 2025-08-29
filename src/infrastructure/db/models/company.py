from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.db import models


class CompanyDB(models.UserDB):
    __tablename__ = "companies"

    company_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.user_id"),
        primary_key=True
    )
    company_name: Mapped[str] = mapped_column(String(50), nullable=False)
    description_company: Mapped[str] = mapped_column(String(500), nullable=True)
    address: Mapped[str] = mapped_column(String(100), nullable=True)
    is_confirmed: Mapped[bool] = mapped_column(Boolean(), default=False)
    # тут мб сделать, чтобы ещё были как-бы менеджеры или что-то типо такого 1:M (1 компания: Много менеджеров)
    # managers: Mapped["ManagerDB"] = relastionship()

    __mapper_args__ = {
        "polymorphic_identity": "company"
    }
