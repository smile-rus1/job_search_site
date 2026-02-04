from dataclasses import dataclass
from decimal import Decimal

from src.core.enums import TransactionStatus, Currency
from src.dto.base_dto import BaseDTO


@dataclass
class BaseBalanceDTODAO(BaseDTO):
    balance_id: int | None
    transaction_id: int | None
    user_id: int | None
    amount: Decimal | None
    currency: Currency | None = None
    provider_event_id: int = None
    status: TransactionStatus | None = None
