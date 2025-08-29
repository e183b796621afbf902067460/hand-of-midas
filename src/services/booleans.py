from attr import attrs
from pandas import DataFrame, Series

from src.adapters.repositories.booleans import BooleansRepository
from src.schemas.booleans import BooleansInputSchema, BooleansQueryInputSchema


@attrs(slots=True, auto_attribs=True, kw_only=True)
class BooleansService:

    _repository: BooleansRepository

    async def extract_booleans(self, input_schema: BooleansQueryInputSchema) -> DataFrame:
        booleans: DataFrame = await self._repository.query_booleans(input_schema=input_schema)
        return booleans.drop_duplicates()

    async def truncate_booleans(self) -> None:
        await self._repository.truncate_booleans()

    async def load_booleans(self, booleans: DataFrame) -> None:
        await self._repository.insert_booleans(booleans=booleans)


def compute_booleans(candlesticks: DataFrame, input_schema: BooleansInputSchema) -> DataFrame:
    column: str = f"is_{input_schema.first_column}_greater_than_{input_schema.second_column}"
    candlesticks[column] = Series(
        candlesticks[input_schema.first_column] > candlesticks[input_schema.second_column]
    ).astype(int)
    return candlesticks
