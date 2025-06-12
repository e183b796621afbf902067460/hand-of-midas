from pydantic import BaseModel

from src.schemas.binance import BinanceIntervalEnum, BinanceSectionEnum


class CandlesticksLatestTimestampInputSchema(BaseModel):
    """Input schema to get latest loaded candlesticks timestamp."""

    ticker: str
    exchange: BinanceSectionEnum

    interval: BinanceIntervalEnum

    class Config:
        use_enum_values: bool = True


class CandlesticksInputSchema(BaseModel):
    """Input schema to get latest loaded candlesticks."""

    ticker: str
    exchange: BinanceSectionEnum

    interval: BinanceIntervalEnum

    class Config:
        use_enum_values: bool = True
