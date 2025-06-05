from httpx import Response

from src.adapters.clients.common.api_base import APIClientBase
from src.schemas.binance import BinanceKlinesInputSchema, BinanceKlinesOutputSchema


class _BinanceAPIClientExceptionBase(Exception):
    """Base Binance client exception to inherit from."""


class _BinanceAPIClientInvalidMethod(_BinanceAPIClientExceptionBase):
    """Raises only and only if invalid method was passed."""


class BinanceSpotAPIClient(APIClientBase):

    _ping_endpoint: str = "/api/v3/ping"
    _klines_endpoint: str = "/api/v3/klines"

    async def ping(self) -> None:
        ping: Response | None = await self._get(endpoint=self._ping_endpoint)

        if ping is None:
            raise _BinanceAPIClientInvalidMethod(f"Invalid method was passed to `{self._ping_endpoint}` endpoint.")

    async def klines(self, input_schema: BinanceKlinesInputSchema) -> list[BinanceKlinesOutputSchema]:
        klines: Response | None = await self._get(
            endpoint=self._klines_endpoint, parameters=input_schema.model_dump(by_alias=True)
        )

        if klines is None:
            raise _BinanceAPIClientInvalidMethod(f"Invalid method was passed to `{self._klines_endpoint}` endpoint.")

        return [
            BinanceKlinesOutputSchema.from_kline(kline=kline, symbol=input_schema.symbol) for kline in klines.json()
        ]
