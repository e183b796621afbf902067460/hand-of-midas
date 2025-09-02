from datetime import datetime, timedelta

from attr import attrs
from pandas import DataFrame

from src.adapters.repositories.candlesticks import CandlesticksRepository
from src.schemas.candlesticks import CandlesticksLatestTimestampQueryInputSchema, CandlesticksQueryInputSchema
from src.settings import settings


@attrs(slots=True, auto_attribs=True, kw_only=True)
class CandlesticksService:

    _repository: CandlesticksRepository

    async def extract_latest_timestamp(self, input_schema: CandlesticksLatestTimestampQueryInputSchema) -> datetime:
        latest_timestamp: datetime | None = await self._repository.query_latest_timestamp(input_schema=input_schema)
        if latest_timestamp is None:
            return settings.TRIGGER_DATE - timedelta(days=settings.DAYS_IN_YEAR * settings.YEARS_AGO)
        return latest_timestamp + timedelta(milliseconds=1)

    async def extract_candlesticks(self, input_schema: CandlesticksQueryInputSchema) -> DataFrame:
        candlesticks: DataFrame = await self._repository.query_candlesticks(input_schema=input_schema)
        return candlesticks.drop_duplicates()

    async def load_candlesticks(self, candlesticks: DataFrame) -> None:
        await self._repository.insert_candlesticks(candlesticks=candlesticks)
