from attr import attrs
from pandas import DataFrame
from talib import RSI

from src.adapters.repositories.rsi import RSIRepository
from src.schemas.rsi import RSIInputSchema, RSIQueryInputSchema


@attrs(slots=True, auto_attribs=True, kw_only=True)
class RSIService:

    _repository: RSIRepository

    async def extract_rsi(self, input_schema: RSIQueryInputSchema) -> DataFrame:
        rsi: DataFrame = await self._repository.query_rsi(input_schema=input_schema)
        return rsi.drop_duplicates()

    async def truncate_rsi(self) -> None:
        await self._repository.truncate_rsi()

    async def load_rsi(self, rsi: DataFrame) -> None:
        await self._repository.insert_rsi(rsi=rsi)


def compute_rsi(candlesticks: DataFrame, input_schema: RSIInputSchema) -> DataFrame:
    column: str = f"{input_schema.column}_rsi"
    candlesticks[column] = RSI(
        real=candlesticks[f"{input_schema.column}"],
        timeperiod=input_schema.period,
    )
    return candlesticks
