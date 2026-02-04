import httpx


class CurrencyConverterClient:
    def __init__(self, base_url: str, api_key: str):
        self._base_url = base_url
        self._api_key = api_key

    async def get_latest(self, base_currency: str) -> dict:
        url = f"{self._base_url}/{self._api_key}/latest/{base_currency}"
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()


def get_currency_converter_client(base_url: str, api_key: str):
    return CurrencyConverterClient(base_url, api_key)
