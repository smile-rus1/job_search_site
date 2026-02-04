import json
from decimal import Decimal

from loguru import logger

from src.infrastructure.currency_converter.client import CurrencyConverterClient
from src.interfaces.infrastructure.currency_converter import ICurrencyConverter
from src.interfaces.infrastructure.redis_db import IRedisDB


class CurrencyConverter(ICurrencyConverter):
    TTL: int = 60 * 60 * 24  # 1 day

    def __init__(self, redis: IRedisDB, client: CurrencyConverterClient):
        self.redis = redis
        self.client = client

    async def update_rates(self, base: str) -> None:
        data = await self.client.get_latest(base)
        rates = data["conversion_rates"]

        key = f"exchange_rates:{base}"
        await self.redis.set(
            key,
            json.dumps(rates),
            expire=self.TTL,
        )

    async def get_rate(
            self,
            from_currency: str,
            to_currency: str,
    ) -> Decimal:
        key = f"exchange_rates:{from_currency}"
        raw = await self.redis.get(key)

        if not raw:
            # fallback - обновляем вручную
            await self.update_rates(from_currency)
            raw = await self.redis.get(key)

        rates = json.loads(raw)

        if to_currency not in rates:
            logger.bind(
                app_name=f"{CurrencyConverter.__name__} IN {self.get_rate.__name__}"
            ).info(f"Unknown currency: {to_currency}")
            raise ValueError(f"Unknown currency: {to_currency}")
        return Decimal(str(rates[to_currency]))
