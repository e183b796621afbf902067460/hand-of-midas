# pylint: disable=duplicate-code
from asyncio import run

from src.entrypoints.common.binance_candlesticks_base import main
from src.schemas.binance import BinanceIntervalEnum, BinanceSectionEnum
from src.settings import settings

if __name__ == "__main__":
    run(main(ticker=settings.TICKER, exchange=BinanceSectionEnum.BINANCE_SPOT, interval=BinanceIntervalEnum.FOUR_HOURS))
# pylint: enable=too-many-locals
