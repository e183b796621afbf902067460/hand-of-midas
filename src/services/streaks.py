from attr import attrs
from pandas import DataFrame

from src.adapters.repositories.streaks import StreaksRepository
from src.schemas.streaks import StreaksInputSchema, StreaksQueryInputSchema


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

    @staticmethod
    def compute_streak(booleans: DataFrame, input_schema: StreaksInputSchema) -> DataFrame:
        booleans["streak_start"] = booleans[input_schema.boolean_column].ne(
            other=booleans[input_schema.boolean_column].shift(1)
        )
        booleans["streak_id"] = booleans["streak_start"].cumsum()
        booleans[f"{input_schema.boolean_column}_streak"] = booleans.groupby("streak_id").cumcount() + 1

        booleans.drop(columns=["streak_start", "streak_id"], axis=1, inplace=True)
        return booleans
