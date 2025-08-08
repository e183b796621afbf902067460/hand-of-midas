from asyncio import run

from clickhouse_connect.driver.asyncclient import AsyncClient as AsyncClickHouseClient
from pandas import DataFrame
from talib._ta_lib import SMA, TEMA, TRIMA  # noqa: WPS436

from src.adapters.repositories.candlesticks import CandlesticksRepository
from src.adapters.repositories.common.clickhouse_base import get_clickhouse_client
from src.adapters.repositories.smoothing import SmoothedCandlesticksRepository
from src.schemas.binance import BinanceIntervalEnum, BinanceSectionEnum
from src.schemas.candlesticks import CandlesticksInputSchema
from src.schemas.smoothing import SmoothingInputSchema
from src.services.candlesticks import CandlesticksService
from src.services.smoothing import SmoothingService
from src.settings import settings


async def main() -> None:
    section: BinanceSectionEnum = BinanceSectionEnum(value=settings.BINANCE_SECTION_NAME)  # type: ignore[call-overload]
    interval: BinanceIntervalEnum = BinanceIntervalEnum(value=settings.INTERVAL)  # type: ignore[call-overload]
    clickhouse_client: AsyncClickHouseClient = await get_clickhouse_client()
    smoothing_service: SmoothingService = SmoothingService(
        repository=SmoothedCandlesticksRepository(client=clickhouse_client)
    )
    candlesticks_service: CandlesticksService = CandlesticksService(
        repository=CandlesticksRepository(client=clickhouse_client)
    )

    candlesticks: DataFrame = await candlesticks_service.extract_candlesticks(
        input_schema=CandlesticksInputSchema(
            ticker=settings.TICKER, exchange=settings.BINANCE_EXCHANGE_NAME, section=section, interval=interval
        )
    )

    smoothed_candlesticks: DataFrame = smoothing_service.smooth_candlesticks(
        candlesticks=candlesticks,
        input_schema=SmoothingInputSchema(prefix="global", smoothing_moving_average_method=SMA, period=2**10),
    )

    smoothed_candlesticks = smoothing_service.smooth_candlesticks(
        candlesticks=smoothed_candlesticks,
        input_schema=SmoothingInputSchema(prefix="macro", smoothing_moving_average_method=TRIMA, period=2**8),
    )
    smoothed_candlesticks = smoothing_service.smooth_candlesticks(
        candlesticks=smoothed_candlesticks,
        input_schema=SmoothingInputSchema(prefix="macro", smoothing_moving_average_method=TEMA, period=2**8),
    )

    smoothed_candlesticks = smoothing_service.smooth_candlesticks(
        candlesticks=smoothed_candlesticks,
        input_schema=SmoothingInputSchema(prefix="micro", smoothing_moving_average_method=TRIMA, period=2**4),
    )
    smoothed_candlesticks = smoothing_service.smooth_candlesticks(
        candlesticks=smoothed_candlesticks,
        input_schema=SmoothingInputSchema(prefix="micro", smoothing_moving_average_method=TEMA, period=2**4),
    )
    smoothed_candlesticks["exchange"] = settings.BINANCE_EXCHANGE_NAME
    smoothed_candlesticks["section"] = settings.BINANCE_SECTION_NAME
    smoothed_candlesticks["ticker"] = settings.TICKER
    smoothed_candlesticks["interval"] = settings.INTERVAL
    smoothed_candlesticks.drop(columns=["open", "high", "low", "close"], axis=1, inplace=True)

    await smoothing_service.truncate_smoothed_candlesticks()
    await smoothing_service.load_smoothed_candlesticks(smoothed_candlesticks=smoothed_candlesticks)


if __name__ == "__main__":
    run(main=main())
