# pylint: disable=duplicate-code
from asyncio import run

from clickhouse_connect.driver.asyncclient import AsyncClient as AsyncClickHouseClient
from pandas import DataFrame

from src.adapters.repositories.booleans import BooleansRepository
from src.adapters.repositories.common.clickhouse_base import get_clickhouse_client
from src.adapters.repositories.smoothing import SmoothedCandlesticksRepository
from src.schemas.booleans import BooleansInputSchema
from src.schemas.common.binance_base import BinanceIntervalEnum, BinanceSectionEnum
from src.schemas.smoothing import SmoothedCandlesticksQueryInputSchema
from src.services.booleans import BooleansService
from src.services.smoothing import SmoothingService
from src.settings import settings


async def main() -> None:
    section: BinanceSectionEnum = BinanceSectionEnum(value=settings.BINANCE_SECTION_NAME)  # type: ignore[call-overload]
    interval: BinanceIntervalEnum = BinanceIntervalEnum(value=settings.INTERVAL)  # type: ignore[call-overload]
    clickhouse_client: AsyncClickHouseClient = await get_clickhouse_client()
    smoothing_service: SmoothingService = SmoothingService(
        repository=SmoothedCandlesticksRepository(client=clickhouse_client)
    )
    booleans_service: BooleansService = BooleansService(repository=BooleansRepository(client=clickhouse_client))
    # pylint: enable=duplicate-code

    smoothed_candlesticks: DataFrame = await smoothing_service.extract_smoothed_candlesticks(
        input_schema=SmoothedCandlesticksQueryInputSchema(
            ticker=settings.TICKER, exchange=settings.BINANCE_EXCHANGE_NAME, section=section, interval=interval
        )
    )
    # TODO: maybe we should also save new highest/lowest highs/lows as independent features as well
    smoothed_candlesticks.drop(
        columns=[
            "global_sma_high",
            "global_sma_low",
            "macro_trima_high",
            "macro_trima_low",
            "macro_tema_high",
            "macro_tema_low",
            "micro_trima_high",
            "micro_trima_low",
            "micro_tema_high",
            "micro_tema_low",
        ],
        axis=1,
        inplace=True,
    )

    booleans: DataFrame = booleans_service.compute_booleans(
        candlesticks=smoothed_candlesticks.copy(deep=True),
        input_schema=BooleansInputSchema(first_column="global_sma_close", second_column="global_sma_open"),
    )

    booleans = booleans_service.compute_booleans(
        candlesticks=booleans.copy(deep=True),
        input_schema=BooleansInputSchema(first_column="macro_trima_close", second_column="macro_trima_open"),
    )
    booleans = booleans_service.compute_booleans(
        candlesticks=booleans.copy(deep=True),
        input_schema=BooleansInputSchema(first_column="macro_tema_close", second_column="macro_tema_open"),
    )

    booleans = booleans_service.compute_booleans(
        candlesticks=booleans.copy(deep=True),
        input_schema=BooleansInputSchema(first_column="micro_trima_close", second_column="micro_trima_open"),
    )
    booleans = booleans_service.compute_booleans(
        candlesticks=booleans.copy(deep=True),
        input_schema=BooleansInputSchema(first_column="micro_tema_close", second_column="micro_tema_open"),
    )

    booleans.drop(
        columns=[
            "global_sma_close",
            "global_sma_open",
            "macro_trima_close",
            "macro_trima_open",
            "macro_tema_close",
            "macro_tema_open",
            "micro_trima_close",
            "micro_trima_open",
            "micro_tema_close",
            "micro_tema_open",
        ],
        axis=1,
        inplace=True,
    )
    await booleans_service.truncate_booleans()
    await booleans_service.load_booleans(booleans=booleans)


if __name__ == "__main__":
    run(main=main())
