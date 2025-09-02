from pydantic import BaseModel

from src.schemas.common.binance_base import BinanceIntervalEnum, BinanceSectionEnum


class QueryInputBaseSchema(BaseModel):
    ticker: str
    exchange: str
    section: BinanceSectionEnum

    interval: BinanceIntervalEnum

    class Config:
        use_enum_values: bool = True
