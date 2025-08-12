from typing import Callable

from numpy import ndarray
from pydantic import BaseModel

from src.schemas.common.query_base import QueryInputBaseSchema


class SmoothingInputSchema(BaseModel):

    prefix: str
    smoothing_moving_average_method: Callable[[ndarray, int], ndarray]
    period: int
    shift: int = 0

    @property
    def smoothing_moving_average_name(self) -> str:
        return self.smoothing_moving_average_method.__name__.lower()


class SmoothedCandlesticksQueryInputSchema(QueryInputBaseSchema):
    """Input schema to get latest loaded smoothed candlesticks."""
