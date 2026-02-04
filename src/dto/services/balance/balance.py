from dataclasses import dataclass
from decimal import Decimal

from src.core.enums import TransactionStatus
from src.dto.base_dto import BaseDTO


@dataclass
class CreateIntentBalanceDTO(BaseDTO):
    user_id: int
    amount: int  # get in cent's
    currency: str


@dataclass
class HandlePaymentBalanceDTO(BaseDTO):
    user_id: int
    transaction_id: int
    provider_event_id: int
    amount: Decimal
    from_currency: str
    status: TransactionStatus | None = None
