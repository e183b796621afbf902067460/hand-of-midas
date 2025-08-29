# pylint: disable=duplicate-code
from asyncio import run

from clickhouse_connect.driver.asyncclient import AsyncClient as AsyncClickHouseClient
from pandas import DataFrame

from src.adapters.repositories.booleans import BooleansRepository
from src.adapters.repositories.common.clickhouse_base import get_clickhouse_client
from src.adapters.repositories.streaks import StreaksRepository
from src.schemas.booleans import BooleansQueryInputSchema
from src.schemas.common.binance_base import BinanceIntervalEnum, BinanceSectionEnum
from src.schemas.streaks import StreaksInputSchema
from src.services.booleans import BooleansService
from src.services.streaks import StreaksService, compute_streak
from src.settings import settings


async def main() -> None:
    section: BinanceSectionEnum = BinanceSectionEnum(value=settings.BINANCE_SECTION_NAME)  # type: ignore[call-overload]
    interval: BinanceIntervalEnum = BinanceIntervalEnum(value=settings.INTERVAL)  # type: ignore[call-overload]
    clickhouse_client: AsyncClickHouseClient = await get_clickhouse_client()
    booleans_service: BooleansService = BooleansService(repository=BooleansRepository(client=clickhouse_client))
    streaks_service: StreaksService = StreaksService(repository=StreaksRepository(client=clickhouse_client))
    # pylint: enable=duplicate-code

    booleans: DataFrame = await booleans_service.extract_booleans(
        input_schema=BooleansQueryInputSchema(
            ticker=settings.TICKER, exchange=settings.BINANCE_EXCHANGE_NAME, section=section, interval=interval
        )
    )

    # `Green Candle Streak`
    streaks: DataFrame = compute_streak(
        booleans=booleans,
        input_schema=StreaksInputSchema(boolean_column="is_global_sma_close_greater_than_global_sma_open"),
    )
    streaks = compute_streak(
        booleans=streaks,
        input_schema=StreaksInputSchema(boolean_column="is_macro_trima_close_greater_than_macro_trima_open"),
    )
    streaks = compute_streak(
        booleans=streaks,
        input_schema=StreaksInputSchema(boolean_column="is_macro_tema_close_greater_than_macro_tema_open"),
    )
    streaks = compute_streak(
        booleans=streaks,
        input_schema=StreaksInputSchema(boolean_column="is_micro_trima_close_greater_than_micro_trima_open"),
    )
    streaks = compute_streak(
        booleans=streaks,
        input_schema=StreaksInputSchema(boolean_column="is_micro_tema_close_greater_than_micro_tema_open"),
    )

    # `SAR Streak`
    streaks = compute_streak(
        booleans=streaks,
        input_schema=StreaksInputSchema(boolean_column="is_global_sma_low_greater_than_global_sma_sar"),
    )
    streaks = compute_streak(
        booleans=streaks,
        input_schema=StreaksInputSchema(boolean_column="is_macro_trima_low_greater_than_macro_trima_sar"),
    )
    streaks = compute_streak(
        booleans=streaks,
        input_schema=StreaksInputSchema(boolean_column="is_macro_tema_low_greater_than_macro_tema_sar"),
    )
    streaks = compute_streak(
        booleans=streaks,
        input_schema=StreaksInputSchema(boolean_column="is_micro_trima_low_greater_than_micro_trima_sar"),
    )
    streaks = compute_streak(
        booleans=streaks,
        input_schema=StreaksInputSchema(boolean_column="is_micro_tema_low_greater_than_micro_tema_sar"),
    )

    streaks.drop(
        columns=[
            "is_global_sma_close_greater_than_global_sma_open",
            "is_macro_trima_close_greater_than_macro_trima_open",
            "is_macro_tema_close_greater_than_macro_tema_open",
            "is_micro_trima_close_greater_than_micro_trima_open",
            "is_micro_tema_close_greater_than_micro_tema_open",
            "is_global_sma_low_greater_than_global_sma_sar",
            "is_macro_trima_low_greater_than_macro_trima_sar",
            "is_macro_tema_low_greater_than_macro_tema_sar",
            "is_micro_trima_low_greater_than_micro_trima_sar",
            "is_micro_tema_low_greater_than_micro_tema_sar",
        ],
        axis=1,
        inplace=True,
    )
    await streaks_service.truncate_streaks()
    await streaks_service.load_streaks(streaks=streaks)


if __name__ == "__main__":
    run(main=main())
