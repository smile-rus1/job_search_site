from dataclasses import dataclass

from src.exceptions.base import BaseExceptions


class BaseBalanceException(BaseExceptions):
    ...


class PaymentException(BaseBalanceException):
    def message(self):
        return f"Exception in payments please, please try later or ask to support"


@dataclass
class NegativeBalanceException(BaseBalanceException):
    balance_id: int

    def message(self):
        return f"Exception in balance id {self.balance_id}. Balance cannot be negative"
