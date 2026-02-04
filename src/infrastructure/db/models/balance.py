from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Numeric, CheckConstraint, Integer, func, String, DateTime

from src.core.enums import TransactionStatus, Currency
from src.infrastructure.db.models.base import Base
from src.infrastructure.enums_db import TransactionTypeEnumDB, TransactionStatusEnumDB, CurrencyEnumDB


class BalanceDB(Base):
    __tablename__ = "balances"

    balance_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    currency: Mapped[CurrencyEnumDB] = mapped_column(
        CurrencyEnumDB,
        nullable=False,
        default=Currency.BYN,
        server_default=Currency.BYN.value
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00")
    )
    transactions: Mapped[list["BalanceTransactionDB"]] = relationship(
        back_populates="balance",
        cascade="all, delete-orphan",
    )

    user: Mapped["UserDB"] = relationship(back_populates="balance")  # type: ignore

    __table_args__ = (
        CheckConstraint("amount >= 0", name="check_balance_non_negative"),
    )


class BalanceTransactionDB(Base):
    __tablename__ = "balance_transactions"

    transaction_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    balance_id: Mapped[int] = mapped_column(
        ForeignKey("balances.balance_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )
    currency: Mapped[CurrencyEnumDB] = mapped_column(
        CurrencyEnumDB,
        nullable=False,
        default=Currency.BYN,
        server_default=Currency.BYN.value
    )
    type: Mapped[TransactionTypeEnumDB] = mapped_column(
        TransactionTypeEnumDB,
        nullable=False
    )
    status: Mapped[TransactionStatusEnumDB] = mapped_column(
        TransactionStatusEnumDB,
        nullable=False,
        default=TransactionStatus.PENDING,
        index=True
    )
    provider_transaction_id: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        index=True,
    )
    provider_event_id: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    balance: Mapped["BalanceDB"] = relationship(back_populates="transactions")
