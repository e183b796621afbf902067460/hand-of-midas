# pylint: disable=duplicate-code
from asyncio import run
from typing import Final

from backtesting import Backtest
from clickhouse_connect.driver.asyncclient import AsyncClient as AsyncClickHouseClient
from pandas import DataFrame, Series, to_datetime  # noqa: WPS347

from src.adapters.repositories.booleans import BooleansRepository
from src.adapters.repositories.candlesticks import CandlesticksRepository
from src.adapters.repositories.common.clickhouse_base import get_clickhouse_client
from src.adapters.repositories.streaks import StreaksRepository
from src.schemas.booleans import BooleansQueryInputSchema
from src.schemas.candlesticks import CandlesticksQueryInputSchema
from src.schemas.common.binance_base import BinanceIntervalEnum, BinanceSectionEnum
from src.schemas.streaks import StreaksQueryInputSchema
from src.services.booleans import BooleansService
from src.services.candlesticks import CandlesticksService
from src.services.streaks import StreaksService
from src.settings import settings
from src.strategies.first import FirstStrategy


# pylint: disable=too-many-locals
async def main(cash: int | float, commission: float) -> None:
    section: BinanceSectionEnum = BinanceSectionEnum(value=settings.BINANCE_SECTION_NAME)  # type: ignore[call-overload]
    interval: BinanceIntervalEnum = BinanceIntervalEnum(value=settings.INTERVAL)  # type: ignore[call-overload]
    clickhouse_client: AsyncClickHouseClient = await get_clickhouse_client()
    candlesticks_service: CandlesticksService = CandlesticksService(
        repository=CandlesticksRepository(client=clickhouse_client)
    )
    booleans_service: BooleansService = BooleansService(repository=BooleansRepository(client=clickhouse_client))
    streaks_service: StreaksService = StreaksService(repository=StreaksRepository(client=clickhouse_client))

    candlesticks: DataFrame = await candlesticks_service.extract_candlesticks(
        input_schema=CandlesticksQueryInputSchema(
            ticker=settings.TICKER, exchange=settings.BINANCE_EXCHANGE_NAME, section=section, interval=interval
        )
    )
    candlesticks.rename(mapper={"open": "Open", "high": "High", "low": "Low", "close": "Close"}, axis=1, inplace=True)
    booleans: DataFrame = await booleans_service.extract_booleans(
        input_schema=BooleansQueryInputSchema(
            ticker=settings.TICKER, exchange=settings.BINANCE_EXCHANGE_NAME, section=section, interval=interval
        )
    )
    streaks: DataFrame = await streaks_service.extract_streaks(
        input_schema=StreaksQueryInputSchema(
            ticker=settings.TICKER, exchange=settings.BINANCE_EXCHANGE_NAME, section=section, interval=interval
        )
    )

    # pylint: enable=duplicate-code

    candlesticks = candlesticks.merge(
        right=booleans, how="left", on=["exchange", "section", "ticker", "interval", "datetime"]
    )
    candlesticks = candlesticks.merge(
        right=streaks, how="left", on=["exchange", "section", "ticker", "interval", "datetime"]
    )

    candlesticks["datetime"] = to_datetime(candlesticks["datetime"])
    candlesticks.set_index(keys="datetime", inplace=True)

    backtest: Backtest = Backtest(
        data=candlesticks,
        strategy=FirstStrategy,
        cash=cash,
        commission=commission,
        trade_on_close=False,
        hedging=False,
    )
    statistics: Series = backtest.run(candle_prefix="macro_tema")
    backtest.plot(resample="W", filename="FirstStrategy.html")

    statistics.to_csv("statistics.csv")
    statistics["_trades"].to_csv("trades.csv", index=False)


# pylint: enable=too-many-locals

if __name__ == "__main__":
    _CASH: Final[int] = 1_000_000
    _COMMISSION: Final[float] = 0.000550

    run(main=main(cash=_CASH, commission=_COMMISSION))
