from attr import attrs
from pandas import DataFrame

from src.adapters.repositories.streaks import StreaksRepository
from src.schemas.streaks import StreaksQueryInputSchema


@attrs(slots=True, auto_attribs=True, kw_only=True)
class StreaksService:

    _repository: StreaksRepository

    async def extract_streaks(self, input_schema: StreaksQueryInputSchema) -> DataFrame:
        streaks: DataFrame = await self._repository.query_streaks(input_schema=input_schema)
        return streaks.drop_duplicates()

    async def truncate_streaks(self) -> None:
        await self._repository.truncate_streaks()

    async def load_streaks(self, streaks: DataFrame) -> None:
        await self._repository.insert_streaks(streaks=streaks)

    # TODO: add compute_streak() method
