import abc
from decimal import Decimal


class ICurrencyConverter(abc.ABC):
    @abc.abstractmethod
    async def update_rates(self, base: str) -> None:
        ...

    @abc.abstractmethod
    async def get_rate(
            self,
            from_currency: str,
            to_currency: str,
    ) -> Decimal:
        return NotImplemented
