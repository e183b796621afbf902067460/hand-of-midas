from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_serializer

from src.settings import settings


class BinanceKlinesIntervalEnum(str, Enum):

    ONE_SECOND = "1s"
    ONE_MINUTE = "1m"
    THREE_MINUTES = "3m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    THIRTY_MINUTES = "30m"

    ONE_HOUR = "1h"
    TWO_HOURS = "2h"
    FOUR_HOURS = "4h"
    SIX_HOURS = "6h"
    EIGHT_HOURS = "8h"
    TWELVE_HOURS = "12h"

    ONE_DAY = "1d"
    THREE_DAYS = "3d"

    ONE_WEEK = "1w"

    ONE_MONTH = "1M"


class BinanceKlinesInputSchema(BaseModel):

    symbol: str

    interval: BinanceKlinesIntervalEnum = Field(default=BinanceKlinesIntervalEnum.ONE_SECOND)

    start_time: int | datetime | None = Field(serialization_alias="startTime")
    end_time: int | datetime | None = Field(serialization_alias="endTime")

    limit: int | None = Field(default=1_000)

    @field_serializer("start_time")
    def serialize_start_time_to_milliseconds(self, start_time: int | datetime | None) -> int | None:
        if isinstance(start_time, datetime):
            return int(start_time.timestamp() * settings.MILLISECONDS_IN_SECOND)
        return start_time

    @field_serializer("end_time")
    def serialize_end_time_to_milliseconds(self, end_time: int | datetime | None) -> int | None:
        if isinstance(end_time, datetime):
            return int(end_time.timestamp() * settings.MILLISECONDS_IN_SECOND)
        return end_time

    class Config:
        use_enum_values: bool = True


class BinanceKlinesOutputSchema(BaseModel):

    symbol: str

    timestamp: datetime = Field(serialization_alias="datetime")

    open: float = Field(serialization_alias="open")
    high: float = Field(serialization_alias="high")
    low: float = Field(serialization_alias="low")
    close: float = Field(serialization_alias="close")

    @staticmethod
    def from_kline(kline: list, symbol: str) -> "BinanceKlinesOutputSchema":
        return BinanceKlinesOutputSchema(
            symbol=symbol,
            timestamp=datetime.fromtimestamp(kline[0] / settings.MILLISECONDS_IN_SECOND),
            open=kline[1],
            high=kline[2],
            low=kline[3],
            close=kline[4],
        )
