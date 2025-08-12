from datetime import datetime, timedelta

from attr import attrs
from numpy import floor
from pandas import DataFrame

from src.adapters.clients.binance import BinanceSpotAPIClient, BinanceUsdtmAPIClient
from src.schemas.binance import BinanceKlinesInputSchema, BinanceKlinesOutputSchema
from src.schemas.common.binance_base import BinanceIntervalEnum


@attrs(slots=True, auto_attribs=True, kw_only=True)
class BinanceService:

    _client: BinanceSpotAPIClient | BinanceUsdtmAPIClient

    async def get_klines(self, input_schema: BinanceKlinesInputSchema) -> DataFrame:
        klines: list[BinanceKlinesOutputSchema] = []

        number_of_batches: int = int(
            floor(
                input_schema.delta.total_seconds() / BinanceIntervalEnum.total_seconds(interval=input_schema.interval)
            )
        )
        for _ in range(number_of_batches):
            batch: list[BinanceKlinesOutputSchema] = await self._client.klines(input_schema=input_schema)
            if not batch:
                break

            next_start_time: datetime = batch[-1].close_time + timedelta(milliseconds=1)
            input_schema = BinanceKlinesInputSchema(
                symbol=input_schema.symbol,
                section=input_schema.section,
                interval=input_schema.interval,
                start_time=next_start_time,
                end_time=input_schema.end_time,
            )

            klines.extend(batch)
        return DataFrame([kline.model_dump() for kline in klines])
