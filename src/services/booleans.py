from attr import attrs
from pandas import DataFrame

from src.adapters.repositories.booleans import BooleansRepository
from src.schemas.booleans import BooleansInputSchema, BooleansQueryInputSchema


def _is_first_number_greater_than_second_number(first_number: int | float, second_number: int | float) -> int:
    return int(first_number > second_number)


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

    @staticmethod
    def compute_booleans(candlesticks: DataFrame, input_schema: BooleansInputSchema) -> DataFrame:
        candlesticks[f"is_{input_schema.first_column}_greater_than_{input_schema.second_column}"] = candlesticks.apply(
            lambda row: _is_first_number_greater_than_second_number(
                first_number=row[input_schema.first_column], second_number=row[input_schema.second_column]
            ),
            axis=1,
        )
        return candlesticks
