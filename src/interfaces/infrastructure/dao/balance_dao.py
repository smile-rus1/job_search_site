from src.core.enums import Currency
from src.dto.db.balance.balance import BaseBalanceDTODAO


class IBalanceDAO:
    async def create_intent(self, balance: BaseBalanceDTODAO) -> BaseBalanceDTODAO:
        ...

    async def replenishment_balance(self, balance: BaseBalanceDTODAO) -> BaseBalanceDTODAO:
        ...

    async def handle_failure_payment(self, balance: BaseBalanceDTODAO) -> BaseBalanceDTODAO:
        ...

    async def get_user_balance_currency(self, user_id: int) -> Currency:
        ...

    async def check_event_exists(self, provider_event_id: str) -> bool:
        ...
