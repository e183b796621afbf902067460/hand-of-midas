# pylint: disable=duplicate-code
from asyncio import run

from backtesting import Backtest
from clickhouse_connect.driver.asyncclient import AsyncClient as AsyncClickHouseClient
from pandas import DataFrame, Series, to_datetime  # noqa: WPS347

from src.adapters.repositories.booleans import BooleansRepository
from src.adapters.repositories.candlesticks import CandlesticksRepository
from src.adapters.repositories.common.clickhouse_base import get_clickhouse_client
from src.adapters.repositories.rsi import RSIRepository
from src.adapters.repositories.sar import SARRepository
from src.adapters.repositories.smoothing import SmoothedCandlesticksRepository
from src.adapters.repositories.streaks import StreaksRepository
from src.backtests.common.base import CASH, COMMISSION, SPREAD
from src.schemas.booleans import BooleansQueryInputSchema
from src.schemas.candlesticks import CandlesticksQueryInputSchema
from src.schemas.common.binance_base import BinanceIntervalEnum, BinanceSectionEnum
from src.schemas.rsi import RSIQueryInputSchema
from src.schemas.sar import SARQueryInputSchema
from src.schemas.smoothing import SmoothedCandlesticksQueryInputSchema
from src.schemas.streaks import StreaksQueryInputSchema
from src.services.booleans import BooleansService
from src.services.candlesticks import CandlesticksService
from src.services.rsi import RSIService
from src.services.sar import SARService
from src.services.smoothing import SmoothingService
from src.services.streaks import StreaksService
from src.settings import settings
from src.strategies.sar import MixinSARStrategy


# pylint: disable=too-many-locals,too-many-statements
async def main(cash: int | float, commission: float, spread: float) -> None:
    section: BinanceSectionEnum = BinanceSectionEnum(value=settings.BINANCE_SECTION_NAME)  # type: ignore[call-overload]
    interval: BinanceIntervalEnum = BinanceIntervalEnum(value=settings.INTERVAL)  # type: ignore[call-overload]
    clickhouse_client: AsyncClickHouseClient = await get_clickhouse_client()

    booleans_service: BooleansService = BooleansService(repository=BooleansRepository(client=clickhouse_client))
    candlesticks_service: CandlesticksService = CandlesticksService(
        repository=CandlesticksRepository(client=clickhouse_client)
    )
    rsi_service: RSIService = RSIService(repository=RSIRepository(client=clickhouse_client))
    sar_service: SARService = SARService(repository=SARRepository(client=clickhouse_client))
    smoothing_service: SmoothingService = SmoothingService(
        repository=SmoothedCandlesticksRepository(client=clickhouse_client)
    )
    streaks_service: StreaksService = StreaksService(repository=StreaksRepository(client=clickhouse_client))

    booleans: DataFrame = await booleans_service.extract_booleans(
        input_schema=BooleansQueryInputSchema(
            ticker=settings.TICKER, exchange=settings.BINANCE_EXCHANGE_NAME, section=section, interval=interval
        )
    )
    candlesticks: DataFrame = await candlesticks_service.extract_candlesticks(
        input_schema=CandlesticksQueryInputSchema(
            ticker=settings.TICKER, exchange=settings.BINANCE_EXCHANGE_NAME, section=section, interval=interval
        )
    )
    candlesticks.rename(mapper={"open": "Open", "high": "High", "low": "Low", "close": "Close"}, axis=1, inplace=True)
    rsi: DataFrame = await rsi_service.extract_rsi(
        input_schema=RSIQueryInputSchema(
            ticker=settings.TICKER, exchange=settings.BINANCE_EXCHANGE_NAME, section=section, interval=interval
        )
    )
    sar: DataFrame = await sar_service.extract_sar(
        input_schema=SARQueryInputSchema(
            ticker=settings.TICKER, exchange=settings.BINANCE_EXCHANGE_NAME, section=section, interval=interval
        )
    )
    smoothed_candlesticks: DataFrame = await smoothing_service.extract_smoothed_candlesticks(
        input_schema=SmoothedCandlesticksQueryInputSchema(
            ticker=settings.TICKER, exchange=settings.BINANCE_EXCHANGE_NAME, section=section, interval=interval
        )
    )
    streaks: DataFrame = await streaks_service.extract_streaks(
        input_schema=StreaksQueryInputSchema(
            ticker=settings.TICKER, exchange=settings.BINANCE_EXCHANGE_NAME, section=section, interval=interval
        )
    )

    merge_on: list[str] = ["exchange", "section", "ticker", "interval", "datetime"]
    candlesticks = candlesticks.merge(right=booleans, how="left", on=merge_on)
    candlesticks = candlesticks.merge(right=rsi, how="left", on=merge_on)
    candlesticks = candlesticks.merge(right=sar, how="left", on=merge_on)
    candlesticks = candlesticks.merge(right=smoothed_candlesticks, how="left", on=merge_on)
    candlesticks = candlesticks.merge(right=streaks, how="left", on=merge_on)

    candlesticks["datetime"] = to_datetime(candlesticks["datetime"])
    candlesticks.set_index(keys="datetime", inplace=True)
    candlesticks.dropna(inplace=True)

    backtest: Backtest = Backtest(
        data=candlesticks,
        strategy=MixinSARStrategy,
        cash=cash,
        commission=commission,
        spread=spread,
        trade_on_close=False,
        hedging=False,
        finalize_trades=True,
    )
    statistics: Series = backtest.run(sar_on_long="micro_tema", sar_on_short="micro_tema")
    statistics.to_csv("statistics.csv")
    trades: DataFrame = statistics["_trades"]
    trades.to_csv("trades.csv")

    backtest.plot(resample="W", filename="SARStrategy.html")


# pylint: enable=too-many-locals,too-many-statements,duplicate-code

if __name__ == "__main__":
    run(main=main(cash=CASH, commission=COMMISSION, spread=SPREAD))
