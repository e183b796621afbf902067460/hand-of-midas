# pylint: disable=duplicate-code
from asyncio import run

from clickhouse_connect.driver.asyncclient import AsyncClient as AsyncClickHouseClient
from pandas import DataFrame

from src.adapters.repositories.common.clickhouse_base import get_clickhouse_client
from src.adapters.repositories.sar import SARRepository
from src.adapters.repositories.smoothing import SmoothedCandlesticksRepository
from src.schemas.common.binance_base import BinanceIntervalEnum, BinanceSectionEnum
from src.schemas.sar import SARInputSchema
from src.schemas.smoothing import SmoothedCandlesticksQueryInputSchema
from src.services.sar import SARService, compute_sar
from src.services.smoothing import SmoothingService
from src.settings import settings


async def main() -> None:
    section: BinanceSectionEnum = BinanceSectionEnum(value=settings.BINANCE_SECTION_NAME)  # type: ignore[call-overload]
    interval: BinanceIntervalEnum = BinanceIntervalEnum(value=settings.INTERVAL)  # type: ignore[call-overload]
    clickhouse_client: AsyncClickHouseClient = await get_clickhouse_client()
    smoothing_service: SmoothingService = SmoothingService(
        repository=SmoothedCandlesticksRepository(client=clickhouse_client)
    )
    sar_service: SARService = SARService(repository=SARRepository(client=clickhouse_client))

    smoothed_candlesticks: DataFrame = await smoothing_service.extract_smoothed_candlesticks(
        input_schema=SmoothedCandlesticksQueryInputSchema(
            ticker=settings.TICKER, exchange=settings.BINANCE_EXCHANGE_NAME, section=section, interval=interval
        )
    )
    smoothed_candlesticks.drop(
        columns=[
            "global_sma_open",
            "global_sma_close",
            "macro_trima_open",
            "macro_trima_close",
            "macro_tema_open",
            "macro_tema_close",
            "micro_trima_open",
            "micro_trima_close",
            "micro_tema_open",
            "micro_tema_close",
        ],
        axis=1,
        inplace=True,
    )
    # pylint: enable=duplicate-code

    sar: DataFrame = compute_sar(
        candlesticks=smoothed_candlesticks,
        input_schema=SARInputSchema(prefix="global_sma"),
    )

    sar = compute_sar(
        candlesticks=sar,
        input_schema=SARInputSchema(prefix="macro_trima"),
    )
    sar = compute_sar(
        candlesticks=sar,
        input_schema=SARInputSchema(prefix="macro_tema"),
    )

    sar = compute_sar(
        candlesticks=sar,
        input_schema=SARInputSchema(prefix="micro_trima"),
    )
    sar = compute_sar(
        candlesticks=sar,
        input_schema=SARInputSchema(prefix="micro_tema"),
    )

    sar.drop(
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
    await sar_service.truncate_sar()
    await sar_service.load_sar(sar=sar)


if __name__ == "__main__":
    run(main=main())
