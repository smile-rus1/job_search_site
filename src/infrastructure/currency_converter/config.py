from dataclasses import dataclass


@dataclass
class CurrencyConverterConfig:
    exchange_rate_key: str
    base_url: str
