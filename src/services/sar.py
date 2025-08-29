from attr import attrs
from pandas import DataFrame
from talib import SAR

from src.adapters.repositories.sar import SARRepository
from src.schemas.sar import SARInputSchema, SARQueryInputSchema


@attrs(slots=True, auto_attribs=True, kw_only=True)
class SARService:

    _repository: SARRepository

    async def extract_sar(self, input_schema: SARQueryInputSchema) -> DataFrame:
        sar: DataFrame = await self._repository.query_sar(input_schema=input_schema)
        return sar.drop_duplicates()

    async def truncate_sar(self) -> None:
        await self._repository.truncate_sar()

    async def load_sar(self, sar: DataFrame) -> None:
        await self._repository.insert_sar(sar=sar)


def compute_sar(candlesticks: DataFrame, input_schema: SARInputSchema) -> DataFrame:
    column: str = f"{input_schema.prefix}_sar"
    candlesticks[column] = SAR(
        high=candlesticks[f"{input_schema.prefix}_high"],
        low=candlesticks[f"{input_schema.prefix}_low"],
        acceleration=input_schema.acceleration,
        maximum=input_schema.maximum,
    )
    return candlesticks
