# pylint: disable=duplicate-code
from asyncio import run

from clickhouse_connect.driver.asyncclient import AsyncClient as AsyncClickHouseClient
from pandas import DataFrame

from src.adapters.repositories.common.clickhouse_base import get_clickhouse_client
from src.adapters.repositories.rsi import RSIRepository
from src.adapters.repositories.sar import SARRepository
from src.adapters.repositories.smoothing import SmoothedCandlesticksRepository
from src.entrypoints.common.base import MICRO_PERIOD
from src.schemas.common.binance_base import BinanceIntervalEnum, BinanceSectionEnum
from src.schemas.rsi import RSIInputSchema
from src.schemas.sar import SARQueryInputSchema
from src.schemas.smoothing import SmoothedCandlesticksQueryInputSchema
from src.services.rsi import RSIService, compute_rsi
from src.services.sar import SARService
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
    rsi_service: RSIService = RSIService(repository=RSIRepository(client=clickhouse_client))

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
    sar: DataFrame = await sar_service.extract_sar(
        input_schema=SARQueryInputSchema(
            ticker=settings.TICKER, exchange=settings.BINANCE_EXCHANGE_NAME, section=section, interval=interval
        )
    )
    candlesticks: DataFrame = smoothed_candlesticks.merge(
        right=sar, how="left", on=["exchange", "section", "ticker", "interval", "datetime"]
    )
    # pylint: enable=duplicate-code

    # `Globals`
    rsi: DataFrame = compute_rsi(
        candlesticks=candlesticks,
        input_schema=RSIInputSchema(column="global_sma_high", period=MICRO_PERIOD),
    )
    rsi = compute_rsi(
        candlesticks=rsi,
        input_schema=RSIInputSchema(column="global_sma_low", period=MICRO_PERIOD),
    )
    rsi = compute_rsi(
        candlesticks=rsi,
        input_schema=RSIInputSchema(column="global_sma_sar", period=MICRO_PERIOD),
    )

    # `Macro TRIMA`
    rsi = compute_rsi(
        candlesticks=rsi,
        input_schema=RSIInputSchema(column="macro_trima_high", period=MICRO_PERIOD),
    )
    rsi = compute_rsi(
        candlesticks=rsi,
        input_schema=RSIInputSchema(column="macro_trima_low", period=MICRO_PERIOD),
    )
    rsi = compute_rsi(
        candlesticks=rsi,
        input_schema=RSIInputSchema(column="macro_trima_sar", period=MICRO_PERIOD),
    )

    # `Macro TEMA`
    rsi = compute_rsi(
        candlesticks=rsi,
        input_schema=RSIInputSchema(column="macro_tema_high", period=MICRO_PERIOD),
    )
    rsi = compute_rsi(
        candlesticks=rsi,
        input_schema=RSIInputSchema(column="macro_tema_low", period=MICRO_PERIOD),
    )
    rsi = compute_rsi(
        candlesticks=rsi,
        input_schema=RSIInputSchema(column="macro_tema_sar", period=MICRO_PERIOD),
    )

    # `Micro TRIMA`
    rsi = compute_rsi(
        candlesticks=rsi,
        input_schema=RSIInputSchema(column="micro_trima_high", period=MICRO_PERIOD),
    )
    rsi = compute_rsi(
        candlesticks=rsi,
        input_schema=RSIInputSchema(column="micro_trima_low", period=MICRO_PERIOD),
    )
    rsi = compute_rsi(
        candlesticks=rsi,
        input_schema=RSIInputSchema(column="micro_trima_sar", period=MICRO_PERIOD),
    )

    # `Micro TEMA`
    rsi = compute_rsi(
        candlesticks=rsi,
        input_schema=RSIInputSchema(column="micro_tema_high", period=MICRO_PERIOD),
    )
    rsi = compute_rsi(
        candlesticks=rsi,
        input_schema=RSIInputSchema(column="micro_tema_low", period=MICRO_PERIOD),
    )
    rsi = compute_rsi(
        candlesticks=rsi,
        input_schema=RSIInputSchema(column="micro_tema_sar", period=MICRO_PERIOD),
    )

    rsi.drop(
        columns=[
            "global_sma_high",
            "global_sma_low",
            "global_sma_sar",
            "macro_trima_high",
            "macro_trima_low",
            "macro_trima_sar",
            "macro_tema_high",
            "macro_tema_low",
            "macro_tema_sar",
            "micro_trima_high",
            "micro_trima_low",
            "micro_trima_sar",
            "micro_tema_high",
            "micro_tema_low",
            "micro_tema_sar",
        ],
        axis=1,
        inplace=True,
    )
    await rsi_service.truncate_rsi()
    await rsi_service.load_rsi(rsi=rsi)


if __name__ == "__main__":
    run(main=main())
