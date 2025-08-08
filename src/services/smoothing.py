from attr import attrs
from pandas import DataFrame, Series

from src.adapters.repositories.smoothing import SmoothedCandlesticksRepository
from src.schemas.smoothing import SmoothedCandlesticksInputSchema, SmoothingInputSchema


@attrs(slots=True, auto_attribs=True, kw_only=True)
class SmoothingService:

    _repository: SmoothedCandlesticksRepository

    async def extract_smoothed_candlesticks(self, input_schema: SmoothedCandlesticksInputSchema) -> DataFrame:
        return await self._repository.query_smoothed_candlesticks(input_schema=input_schema)

    async def truncate_smoothed_candlesticks(self) -> None:
        await self._repository.truncate_smoothed_candlesticks()

    async def load_smoothed_candlesticks(self, smoothed_candlesticks: DataFrame) -> None:
        await self._repository.insert_smoothed_candlesticks(smoothed_candlesticks=smoothed_candlesticks)

    @staticmethod
    def smooth_candlesticks(candlesticks: DataFrame, input_schema: SmoothingInputSchema) -> DataFrame:
        prefix: str = f"{input_schema.prefix}_{input_schema.smoothing_moving_average_name}"

        candlesticks[f"{prefix}_open"] = Series(
            input_schema.smoothing_moving_average_method(candlesticks.open.values, input_schema.period)
        ).shift(periods=input_schema.shift)
        candlesticks[f"{prefix}_high"] = Series(
            input_schema.smoothing_moving_average_method(candlesticks.high.values, input_schema.period)
        ).shift(periods=input_schema.shift)
        candlesticks[f"{prefix}_low"] = Series(
            input_schema.smoothing_moving_average_method(candlesticks.low.values, input_schema.period)
        ).shift(periods=input_schema.shift)
        candlesticks[f"{prefix}_close"] = Series(
            input_schema.smoothing_moving_average_method(candlesticks.close.values, input_schema.period)
        ).shift(periods=input_schema.shift)
        return candlesticks
